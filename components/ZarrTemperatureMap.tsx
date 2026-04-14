/** @jsxImportSource theme-ui */

/**
 * HRRR streaming visualization over Austin, TX.
 * Streams 24 hourly analysis chunks from hrrrzarr (S3) via zarrita.
 * Variables: 2m temp, 2m RH, 10m wind, surface precip rate.
 */

import type { Map as MapLibreMap } from 'maplibre-gl';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { FetchStore, get, open, root, slice } from 'zarrita';

const AUSTIN = { lng: -97.74, lat: 30.27 };

// HRRR Lambert Conformal grid window around Austin (80x80 ≈ 240km square)
const Y0 = 183;
const Y1 = 263;
const X0 = 851;
const X1 = 931;
const WIN_H = Y1 - Y0;
const WIN_W = X1 - X0;

// Four corners of window, reprojected to lat/lon. Order: TL, TR, BR, BL.
const CORNERS: [[number, number], [number, number], [number, number], [number, number]] = [
  [-99.0105, 31.3287],
  [-96.5028, 31.3347],
  [-96.5292, 29.1981],
  [-98.9704, 29.1923],
];

const DATE = '20260412';
const HRRR_BASE = `https://hrrrzarr.s3.amazonaws.com/sfc/${DATE}`;

type VarKey = 'tmp' | 'rh' | 'wind';

interface VarConfig {
  label: string;
  unit: string;
  range: [number, number];
  colormap: (f: number) => [number, number, number, number];
  fetch: (hour: number) => Promise<Float32Array>;
  transform: (v: number) => number;
}

function cmapTemp(f: number): [number, number, number, number] {
  const r = Math.round(30 + f * 225);
  const g = Math.round(60 + (1 - Math.abs(f - 0.5) * 2) * 140);
  const b = Math.round(210 - f * 190);
  return [r, g, b, 200];
}

function cmapRH(f: number): [number, number, number, number] {
  // Dry (brown) → moist (teal/blue)
  const r = Math.round(200 - f * 160);
  const g = Math.round(160 + f * 30);
  const b = Math.round(120 + f * 110);
  return [r, g, b, 200];
}

function cmapWind(f: number): [number, number, number, number] {
  // Bright cyan (calm) → saturated royal blue (windy): high contrast, colorblind-safe.
  const r = Math.round(140 - f * 110);
  const g = Math.round(220 - f * 140);
  const b = Math.round(245 - f * 55);
  return [r, g, b, Math.round(150 + f * 100)];
}

async function fetchHRRRArray(hour: number, path: string): Promise<Float32Array> {
  const hh = String(hour).padStart(2, '0');
  const url = `${HRRR_BASE}/${DATE}_${hh}z_anl.zarr`;
  const store = new FetchStore(url);
  const arr = await open(root(store).resolve(path), { kind: 'array' });
  const result = await get(arr, [slice(Y0, Y1), slice(X0, X1)]);
  return result.data as Float32Array;
}

async function fetchWindSpeed(hour: number): Promise<Float32Array> {
  const [u, v] = await Promise.all([
    fetchHRRRArray(hour, '10m_above_ground/UGRD/10m_above_ground/UGRD'),
    fetchHRRRArray(hour, '10m_above_ground/VGRD/10m_above_ground/VGRD'),
  ]);
  const out = new Float32Array(u.length);
  for (let i = 0; i < u.length; i++) {
    out[i] = Math.sqrt(u[i] * u[i] + v[i] * v[i]);
  }
  return out;
}

const VARIABLES: Record<VarKey, VarConfig> = {
  tmp: {
    label: '2m Temperature',
    unit: '°F',
    range: [50, 95],
    colormap: cmapTemp,
    fetch: (h) => fetchHRRRArray(h, '2m_above_ground/TMP/2m_above_ground/TMP'),
    transform: (k) => (k - 273.15) * 1.8 + 32,
  },
  rh: {
    label: '2m Humidity',
    unit: '%',
    range: [50, 100],
    colormap: cmapRH,
    fetch: (h) => fetchHRRRArray(h, '2m_above_ground/RH/2m_above_ground/RH'),
    transform: (v) => v,
  },
  wind: {
    label: '10m Wind',
    unit: 'm/s',
    range: [0, 15],
    colormap: cmapWind,
    fetch: fetchWindSpeed,
    transform: (v) => v,
  },
};

// Austin pixel within 80x80 window: (73, 141) computed via pyproj.
const AUSTIN_Y = 73;
const AUSTIN_X = 141;

function renderHeatmap(grid: Float32Array | null, cfg: VarConfig): string {
  const canvas = document.createElement('canvas');
  canvas.width = WIN_W;
  canvas.height = WIN_H;
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('no 2d ctx');
  const img = ctx.createImageData(WIN_W, WIN_H);
  const [lo, hi] = cfg.range;
  if (grid) {
    // HRRR y axis is bottom-up; canvas is top-down → flip vertically.
    for (let r = 0; r < WIN_H; r++) {
      const srcRow = WIN_H - 1 - r;
      for (let c = 0; c < WIN_W; c++) {
        const raw = grid[srcRow * WIN_W + c];
        const v = cfg.transform(raw);
        const f = Math.max(0, Math.min(1, (v - lo) / (hi - lo)));
        const [R, G, B, A] = cfg.colormap(f);
        const i = (r * WIN_W + c) * 4;
        img.data[i] = R;
        img.data[i + 1] = G;
        img.data[i + 2] = B;
        img.data[i + 3] = A;
      }
    }
  }
  ctx.putImageData(img, 0, 0);
  return canvas.toDataURL();
}

export function ZarrTemperatureMap() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const [activeVar, setActiveVar] = useState<VarKey>('tmp');
  const [hour, setHour] = useState(0);
  const [ready, setReady] = useState(false);
  const [playing, setPlaying] = useState(true);
  const playRef = useRef(false);
  const [cache, setCache] = useState<Map<string, Float32Array>>(() => new Map());
  const cacheRef = useRef(cache);
  cacheRef.current = cache;

  const cfg = VARIABLES[activeVar];

  // Background stream 24 hours for the active variable (skip already cached).
  useEffect(() => {
    let cancelled = false;
    (async () => {
      for (let h = 0; h < 24; h++) {
        if (cancelled) return;
        const key = `${activeVar}-${h}`;
        if (cacheRef.current.has(key)) continue;
        try {
          const data = await VARIABLES[activeVar].fetch(h);
          if (cancelled) return;
          setCache((prev) => {
            const next = new Map(prev);
            next.set(key, data);
            return next;
          });
        } catch (e) {
          console.error(`HRRR ${activeVar} hour ${h} failed:`, e);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [activeVar]);

  const loadedCount = useMemo(() => {
    let n = 0;
    for (let h = 0; h < 24; h++) if (cache.has(`${activeVar}-${h}`)) n++;
    return n;
  }, [cache, activeVar]);

  const updateOverlay = useCallback(
    (varKey: VarKey, h: number) => {
      const map = mapRef.current;
      if (!map) return;
      const source = map.getSource('heatmap') as
        | {
            updateImage: (options: {
              url: string;
              coordinates: [[number, number], [number, number], [number, number], [number, number]];
            }) => void;
          }
        | undefined;
      if (!source) return;
      const grid = cache.get(`${varKey}-${h}`) ?? null;
      source.updateImage({ url: renderHeatmap(grid, VARIABLES[varKey]), coordinates: CORNERS });
    },
    [cache],
  );

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (!containerRef.current) return;

    let map: MapLibreMap | null = null;
    let cancelled = false;
    let observer: ResizeObserver | null = null;

    function initMap() {
      if (cancelled || !containerRef.current || mapRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      (async () => {
        const maplibregl = await import('maplibre-gl');
        if (cancelled || !containerRef.current) return;

        map = new maplibregl.default.Map({
          container: containerRef.current,
          style: {
            version: 8,
            glyphs: 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
            sources: {
              satellite: {
                type: 'raster',
                tiles: [
                  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                ],
                tileSize: 256,
                maxzoom: 18,
              },
              'carto-labels': {
                type: 'raster',
                tiles: [
                  'https://a.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}@2x.png',
                  'https://b.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}@2x.png',
                ],
                tileSize: 256,
              },
              heatmap: {
                type: 'image',
                url: renderHeatmap(null, VARIABLES.tmp),
                coordinates: CORNERS,
              },
            },
            layers: [
              { id: 'satellite', type: 'raster', source: 'satellite' },
              {
                id: 'heatmap',
                type: 'raster',
                source: 'heatmap',
                paint: { 'raster-opacity': 0.7, 'raster-fade-duration': 0 },
              },
              {
                id: 'labels',
                type: 'raster',
                source: 'carto-labels',
                paint: { 'raster-opacity': 0.9 },
              },
            ],
          },
          center: [AUSTIN.lng, AUSTIN.lat],
          zoom: 7.2,
          maxZoom: 11,
          minZoom: 5,
          attributionControl: false,
        });

        map.addControl(new maplibregl.default.NavigationControl(), 'top-right');
        map.on('load', () => setReady(true));
        mapRef.current = map;
      })();
    }

    observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentRect.width > 0 && entry.contentRect.height > 0 && !mapRef.current) {
          initMap();
        }
      }
    });
    observer.observe(containerRef.current);
    initMap();

    return () => {
      cancelled = true;
      observer?.disconnect();
      if (map) {
        map.remove();
        mapRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (ready) updateOverlay(activeVar, hour);
  }, [activeVar, hour, ready, updateOverlay]);

  useEffect(() => {
    playRef.current = playing;
    if (!playing) return;
    let frame: number;
    let lastTime = 0;
    const animate = (time: number) => {
      if (!playRef.current) return;
      if (time - lastTime > 800) {
        setHour((h) => {
          const next = (h + 1) % 24;
          return cache.has(`${activeVar}-${next}`) ? next : h;
        });
        lastTime = time;
      }
      frame = requestAnimationFrame(animate);
    };
    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [playing, cache, activeVar]);

  const currentHourStr = `${String(hour).padStart(2, '0')}:00 UTC`;
  const hourCached = cache.has(`${activeVar}-${hour}`);
  const prettyDate = `${DATE.slice(0, 4)}-${DATE.slice(4, 6)}-${DATE.slice(6, 8)}`;
  const austinVal = (() => {
    const g = cache.get(`${activeVar}-${hour}`);
    if (!g) return null;
    return cfg.transform(g[AUSTIN_Y * WIN_W + AUSTIN_X]);
  })();

  return (
    <div
      sx={{
        width: '100%',
        height: '70vh',
        borderRadius: 8,
        overflow: 'hidden',
        position: 'relative',
        bg: '#0a0a0a',
      }}
    >
      <div ref={containerRef} sx={{ width: '100%', height: '100%' }} />

      {/* Info overlay */}
      <div
        sx={{
          position: 'absolute',
          top: 10,
          left: 10,
          bg: 'rgba(10, 10, 10, 0.82)',
          backdropFilter: 'blur(8px)',
          color: '#f4f4eb',
          px: 3,
          py: 2,
          borderRadius: 6,
          fontFamily: '"Space Grotesk", system-ui, sans-serif',
          fontSize: '12px',
          zIndex: 10,
          lineHeight: 1.5,
        }}
      >
        <div sx={{ fontWeight: 600, fontSize: '13px' }}>HRRR · {cfg.label}</div>
        <div sx={{ opacity: 0.6, fontSize: '11px' }}>
          3km · {prettyDate} · {currentHourStr}
          {austinVal !== null && (
            <div sx={{ fontSize: '10px', marginTop: 4 }}>
              Austin: {austinVal.toFixed(1)}
              {cfg.unit}
            </div>
          )}
          <div sx={{ fontSize: '10px', marginTop: 4, opacity: 0.7 }}>
            hrrrzarr · zarrita · {loadedCount}/24 hrs streamed
          </div>
        </div>
      </div>

      {/* Colorbar */}
      <div
        sx={{
          position: 'absolute',
          top: 10,
          right: 44,
          bg: 'rgba(10, 10, 10, 0.82)',
          backdropFilter: 'blur(8px)',
          borderRadius: 6,
          px: '10px',
          py: 2,
          zIndex: 10,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '2px',
        }}
      >
        <span sx={{ fontFamily: 'monospace', fontSize: '10px', color: '#f4f4eb', opacity: 0.7 }}>
          {cfg.range[1]}
          {cfg.unit}
        </span>
        <div
          sx={{
            width: 14,
            height: 120,
            borderRadius: 2,
            overflow: 'hidden',
            border: '1px solid rgba(244,244,235,0.15)',
          }}
        >
          {Array.from({ length: 40 }).map((_, idx) => {
            const f = 1 - idx / 39;
            const [r, g, b, a] = cfg.colormap(f);
            return (
              <div
                key={`color-stop-${Math.round(f * 1000)}`}
                sx={{
                  width: '100%',
                  height: '2.5%',
                  bg: `rgba(${r},${g},${b},${a / 255})`,
                }}
              />
            );
          })}
        </div>
        <span sx={{ fontFamily: 'monospace', fontSize: '10px', color: '#f4f4eb', opacity: 0.7 }}>
          {cfg.range[0]}
          {cfg.unit}
        </span>
      </div>

      {/* Bottom controls */}
      <div
        sx={{
          position: 'absolute',
          bottom: 10,
          left: 10,
          right: 10,
          display: 'flex',
          flexDirection: 'column',
          gap: '6px',
          zIndex: 10,
        }}
      >
        {/* Time slider */}
        <div
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 2,
            bg: 'rgba(10, 10, 10, 0.82)',
            backdropFilter: 'blur(8px)',
            borderRadius: 6,
            px: 2,
            py: '6px',
          }}
        >
          <button
            type="button"
            onClick={() => setPlaying((p) => !p)}
            sx={{
              border: 'none',
              bg: 'transparent',
              color: '#f4f4eb',
              cursor: 'pointer',
              fontSize: '14px',
              fontFamily: 'monospace',
              px: 1,
              flexShrink: 0,
            }}
          >
            {playing ? '⏸' : '▶'}
          </button>
          <input
            type="range"
            min={0}
            max={23}
            value={hour}
            onChange={(e) => {
              setPlaying(false);
              setHour(Number(e.target.value));
            }}
            sx={{
              flex: 1,
              height: '4px',
              appearance: 'none',
              bg: 'rgba(244,244,235,0.2)',
              borderRadius: 2,
              outline: 'none',
              cursor: 'pointer',
              '&::-webkit-slider-thumb': {
                appearance: 'none',
                width: 14,
                height: 14,
                borderRadius: '50%',
                bg: hourCached ? '#80a0d8' : '#555',
                cursor: 'pointer',
              },
            }}
          />
          <span
            sx={{
              fontFamily: 'monospace',
              fontSize: '11px',
              color: '#f4f4eb',
              opacity: 0.7,
              minWidth: '90px',
              textAlign: 'right',
              flexShrink: 0,
            }}
          >
            {currentHourStr}
            {!hourCached && ' …'}
          </span>
        </div>

        {/* Variable selector */}
        <div
          sx={{
            display: 'flex',
            gap: 1,
            bg: 'rgba(10, 10, 10, 0.82)',
            backdropFilter: 'blur(8px)',
            borderRadius: 6,
            p: '4px',
            justifyContent: 'center',
          }}
        >
          {(Object.entries(VARIABLES) as [VarKey, VarConfig][]).map(([key, v]) => (
            <button
              key={key}
              type="button"
              onClick={() => setActiveVar(key)}
              sx={{
                border: 'none',
                borderRadius: 4,
                px: 2,
                py: 1,
                fontSize: '11px',
                fontFamily: '"Space Grotesk", system-ui, sans-serif',
                fontWeight: activeVar === key ? 600 : 400,
                cursor: 'pointer',
                transition: 'all 0.15s',
                bg: activeVar === key ? 'rgba(128, 160, 216, 0.3)' : 'transparent',
                color: activeVar === key ? '#f4f4eb' : 'rgba(244, 244, 235, 0.5)',
                '&:hover': {
                  bg: activeVar === key ? 'rgba(128, 160, 216, 0.3)' : 'rgba(255,255,255,0.08)',
                },
              }}
            >
              {v.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
