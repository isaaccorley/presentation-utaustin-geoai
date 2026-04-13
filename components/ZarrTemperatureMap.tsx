/** @jsxImportSource theme-ui */

/**
 * ERA5 climate variable visualization over Austin, TX.
 * MapLibre with ESRI satellite basemap + Carto labels + heatmap overlay.
 * Supports switching variables and scrubbing time via slider.
 */

import { useEffect, useRef, useState, useCallback } from 'react';

const AUSTIN = { lng: -97.74, lat: 30.27 };
const GRID_SIZE = 64;
const GRID_EXTENT = 1.2;

// 24 hourly timesteps
const HOURS = Array.from({ length: 24 }, (_, i) => `${String(i).padStart(2, '0')}:00 UTC`);

interface VarConfig {
  label: string;
  unit: string;
  generate: (hour: number) => number[][];
  colormap: (f: number) => [number, number, number, number];
  range: [number, number];
}

function genTemperature(hour: number): number[][] {
  // Diurnal cycle: coolest at 06, warmest at 15
  const diurnal = -3 * Math.cos(((hour - 15) / 24) * 2 * Math.PI);
  const grid: number[][] = [];
  for (let r = 0; r < GRID_SIZE; r++) {
    const row: number[] = [];
    for (let c = 0; c < GRID_SIZE; c++) {
      const cx = (c - GRID_SIZE / 2) / GRID_SIZE;
      const cy = (r - GRID_SIZE / 2) / GRID_SIZE;
      const dist = Math.sqrt(cx * cx + cy * cy);
      // Urban heat island effect in center
      const uhi = Math.exp(-dist * dist / 0.08) * 2;
      const base = 300 + diurnal + uhi - dist * 14 + cx * 4;
      const noise = Math.sin(c * 1.7 + r * 0.9 + hour * 0.3) * 1.0;
      row.push(base + noise);
    }
    grid.push(row);
  }
  return grid;
}

function genWind(hour: number): number[][] {
  const timeShift = hour * 0.4;
  const grid: number[][] = [];
  for (let r = 0; r < GRID_SIZE; r++) {
    const row: number[] = [];
    for (let c = 0; c < GRID_SIZE; c++) {
      const cx = (c - GRID_SIZE / 2) / GRID_SIZE;
      const cy = (r - GRID_SIZE / 2) / GRID_SIZE;
      const base = 4 + Math.sin(cx * 3.5 + cy * 1.2 + timeShift) * 2.5 + Math.cos(cy * 4 + timeShift * 0.7) * 1.5;
      const noise = Math.sin(c * 0.8 + r * 1.3 + hour * 0.2) * 0.6;
      row.push(Math.max(0, base + noise));
    }
    grid.push(row);
  }
  return grid;
}

function genPrecipitation(hour: number): number[][] {
  // Storm cell moves across area over time
  const stormX = -0.3 + (hour / 24) * 0.8;
  const stormY = 0.2 - (hour / 24) * 0.3;
  const grid: number[][] = [];
  for (let r = 0; r < GRID_SIZE; r++) {
    const row: number[] = [];
    for (let c = 0; c < GRID_SIZE; c++) {
      const cx = (c - GRID_SIZE / 2) / GRID_SIZE;
      const cy = (r - GRID_SIZE / 2) / GRID_SIZE;
      const cell1 = Math.exp(-((cx - stormX) ** 2 + (cy - stormY) ** 2) / 0.04) * 14;
      const cell2 = Math.exp(-((cx + 0.1) ** 2 + (cy + 0.25 - hour * 0.01) ** 2) / 0.06) * 6;
      const noise = Math.sin(c * 2.1 + r * 1.4 + hour * 0.5) * 0.5;
      row.push(Math.max(0, cell1 + cell2 + noise));
    }
    grid.push(row);
  }
  return grid;
}

function cmapTemp(f: number): [number, number, number, number] {
  const r = Math.round(30 + f * 225);
  const g = Math.round(60 + (1 - Math.abs(f - 0.5) * 2) * 140);
  const b = Math.round(210 - f * 190);
  return [r, g, b, 170];
}

function cmapWind(f: number): [number, number, number, number] {
  const r = Math.round(240 - f * 200);
  const g = Math.round(245 - f * 120);
  const b = Math.round(250 - f * 40);
  return [r, g, b, Math.round(50 + f * 150)];
}

function cmapPrecip(f: number): [number, number, number, number] {
  if (f < 0.03) return [0, 0, 0, 0];
  const r = Math.round(f > 0.6 ? (f - 0.6) * 400 : 0);
  const g = Math.round(f < 0.5 ? f * 400 : (1 - f) * 300);
  const b = Math.round(50 + f * 200);
  return [r, g, b, Math.round(40 + f * 180)];
}

const VARIABLES: Record<string, VarConfig> = {
  t2m: { label: '2m Temperature', unit: 'K', generate: genTemperature, colormap: cmapTemp, range: [286, 308] },
  u10: { label: '10m Wind Speed', unit: 'm/s', generate: genWind, colormap: cmapWind, range: [0, 12] },
  tp: { label: 'Total Precipitation', unit: 'mm', generate: genPrecipitation, colormap: cmapPrecip, range: [0, 14] },
};

function renderHeatmapImage(varKey: string, hour: number): string {
  const cfg = VARIABLES[varKey];
  const canvas = document.createElement('canvas');
  canvas.width = GRID_SIZE;
  canvas.height = GRID_SIZE;
  const ctx = canvas.getContext('2d')!;
  const imgData = ctx.createImageData(GRID_SIZE, GRID_SIZE);
  const grid = cfg.generate(hour);
  const [lo, hi] = cfg.range;
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      const f = Math.max(0, Math.min(1, (grid[r][c] - lo) / (hi - lo)));
      const [red, green, blue, alpha] = cfg.colormap(f);
      const idx = (r * GRID_SIZE + c) * 4;
      imgData.data[idx] = red;
      imgData.data[idx + 1] = green;
      imgData.data[idx + 2] = blue;
      imgData.data[idx + 3] = alpha;
    }
  }
  ctx.putImageData(imgData, 0, 0);
  return canvas.toDataURL();
}

export function ZarrTemperatureMap() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const [activeVar, setActiveVar] = useState('t2m');
  const [hour, setHour] = useState(12);
  const [ready, setReady] = useState(false);
  const [playing, setPlaying] = useState(true);
  const playRef = useRef(false);

  const updateOverlay = useCallback((varKey: string, h: number) => {
    const map = mapRef.current;
    if (!map) return;
    const source = map.getSource('heatmap');
    if (!source) return;
    const dataUrl = renderHeatmapImage(varKey, h);
    source.updateImage({
      url: dataUrl,
      coordinates: [
        [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
        [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
        [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
        [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
      ],
    });
  }, []);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (!containerRef.current) return;

    let map: any;
    let cancelled = false;
    let observer: ResizeObserver | null = null;

    function initMap() {
      if (cancelled || !containerRef.current || mapRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      (async () => {
        const maplibregl = await import('maplibre-gl');
        if (cancelled || !containerRef.current) return;

        const initialImage = renderHeatmapImage('t2m', 12);

        map = new maplibregl.default.Map({
          container: containerRef.current,
          style: {
            version: 8,
            glyphs: 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
            sources: {
              satellite: {
                type: 'raster',
                tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
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
                url: initialImage,
                coordinates: [
                  [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
                  [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
                  [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
                  [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
                ],
              },
            },
            layers: [
              { id: 'satellite', type: 'raster', source: 'satellite' },
              { id: 'heatmap', type: 'raster', source: 'heatmap', paint: { 'raster-opacity': 0.7, 'raster-fade-duration': 0 } },
              { id: 'labels', type: 'raster', source: 'carto-labels', paint: { 'raster-opacity': 0.9 } },
            ],
          },
          center: [AUSTIN.lng, AUSTIN.lat],
          zoom: 8,
          maxZoom: 12,
          minZoom: 6,
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
      if (map) { map.remove(); mapRef.current = null; }
    };
  }, []);

  // Update overlay on var/hour change
  useEffect(() => {
    if (ready) updateOverlay(activeVar, hour);
  }, [activeVar, hour, ready, updateOverlay]);

  // Play animation
  useEffect(() => {
    playRef.current = playing;
    if (!playing) return;
    let frame: number;
    let lastTime = 0;
    const animate = (time: number) => {
      if (!playRef.current) return;
      if (time - lastTime > 1000) {
        setHour(h => (h + 1) % 24);
        lastTime = time;
      }
      frame = requestAnimationFrame(animate);
    };
    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [playing]);

  const cfg = VARIABLES[activeVar];

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
        <div sx={{ fontWeight: 600, fontSize: '13px' }}>ERA5 · {cfg.label}</div>
        <div sx={{ opacity: 0.6, fontSize: '11px' }}>
          {cfg.range[0]}–{cfg.range[1]} {cfg.unit} · 0.25° · {HOURS[hour]}
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
          {cfg.range[1]} {cfg.unit}
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
          {Array.from({ length: 40 }, (_, i) => {
            const f = 1 - i / 39;
            const [r, g, b, a] = cfg.colormap(f);
            return (
              <div
                key={i}
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
          {cfg.range[0]} {cfg.unit}
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
            onClick={() => setPlaying(p => !p)}
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
            onChange={e => { setPlaying(false); setHour(Number(e.target.value)); }}
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
                bg: '#80a0d8',
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
              minWidth: '60px',
              textAlign: 'right',
              flexShrink: 0,
            }}
          >
            {HOURS[hour]}
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
          {Object.entries(VARIABLES).map(([key, v]) => (
            <button
              key={key}
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
                '&:hover': { bg: activeVar === key ? 'rgba(128, 160, 216, 0.3)' : 'rgba(255,255,255,0.08)' },
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
