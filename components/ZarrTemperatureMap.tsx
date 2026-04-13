/** @jsxImportSource theme-ui */

/**
 * ERA5 climate variable visualization over Austin, TX.
 * Uses MapLibre with ESRI satellite basemap + canvas-source heatmap overlay.
 * Supports switching between variables (temperature, wind, precipitation).
 */

import { useEffect, useRef, useState, useCallback } from 'react';

const AUSTIN = { lng: -97.74, lat: 30.27 };
const GRID_SIZE = 64;
const GRID_EXTENT = 1.2; // degrees from center

interface VarConfig {
  label: string;
  unit: string;
  generate: () => number[][];
  colormap: (f: number) => [number, number, number, number];
  range: [number, number];
}

// --- Variable definitions ---

function genTemperature(): number[][] {
  const grid: number[][] = [];
  for (let r = 0; r < GRID_SIZE; r++) {
    const row: number[] = [];
    for (let c = 0; c < GRID_SIZE; c++) {
      const cx = (c - GRID_SIZE / 2) / GRID_SIZE;
      const cy = (r - GRID_SIZE / 2) / GRID_SIZE;
      const dist = Math.sqrt(cx * cx + cy * cy);
      const base = 305 - dist * 18 + cx * 4;
      const noise = Math.sin(c * 1.7 + r * 0.9) * 1.2 + Math.cos(c * 0.3 + r * 2.1) * 0.8;
      row.push(base + noise);
    }
    grid.push(row);
  }
  return grid;
}

function genWind(): number[][] {
  const grid: number[][] = [];
  for (let r = 0; r < GRID_SIZE; r++) {
    const row: number[] = [];
    for (let c = 0; c < GRID_SIZE; c++) {
      const cx = (c - GRID_SIZE / 2) / GRID_SIZE;
      const cy = (r - GRID_SIZE / 2) / GRID_SIZE;
      const base = 4 + Math.sin(cx * 3.5 + cy * 1.2) * 2.5 + Math.cos(cy * 4) * 1.5;
      const noise = Math.sin(c * 0.8 + r * 1.3) * 0.6;
      row.push(Math.max(0, base + noise));
    }
    grid.push(row);
  }
  return grid;
}

function genPrecipitation(): number[][] {
  const grid: number[][] = [];
  for (let r = 0; r < GRID_SIZE; r++) {
    const row: number[] = [];
    for (let c = 0; c < GRID_SIZE; c++) {
      const cx = (c - GRID_SIZE / 2) / GRID_SIZE;
      const cy = (r - GRID_SIZE / 2) / GRID_SIZE;
      // Clustered rainfall pattern
      const cell1 = Math.exp(-((cx + 0.3) ** 2 + (cy - 0.2) ** 2) / 0.05) * 12;
      const cell2 = Math.exp(-((cx - 0.25) ** 2 + (cy + 0.15) ** 2) / 0.08) * 8;
      const noise = Math.sin(c * 2.1 + r * 1.4) * 0.5;
      row.push(Math.max(0, cell1 + cell2 + noise + 0.3));
    }
    grid.push(row);
  }
  return grid;
}

function cmapTemp(f: number): [number, number, number, number] {
  const r = Math.round(30 + f * 225);
  const g = Math.round(60 + (1 - Math.abs(f - 0.5) * 2) * 140);
  const b = Math.round(210 - f * 190);
  return [r, g, b, 180];
}

function cmapWind(f: number): [number, number, number, number] {
  // White → teal → dark blue
  const r = Math.round(240 - f * 200);
  const g = Math.round(245 - f * 120);
  const b = Math.round(250 - f * 40);
  return [r, g, b, Math.round(60 + f * 140)];
}

function cmapPrecip(f: number): [number, number, number, number] {
  // Transparent → green → blue → purple
  if (f < 0.05) return [0, 0, 0, 0];
  const r = Math.round(f > 0.6 ? (f - 0.6) * 400 : 0);
  const g = Math.round(f < 0.5 ? f * 400 : (1 - f) * 300);
  const b = Math.round(50 + f * 200);
  return [r, g, b, Math.round(40 + f * 180)];
}

const VARIABLES: Record<string, VarConfig> = {
  t2m: {
    label: '2m Temperature',
    unit: 'K',
    generate: genTemperature,
    colormap: cmapTemp,
    range: [286, 308],
  },
  u10: {
    label: '10m Wind Speed',
    unit: 'm/s',
    generate: genWind,
    colormap: cmapWind,
    range: [0, 12],
  },
  tp: {
    label: 'Total Precipitation',
    unit: 'mm',
    generate: genPrecipitation,
    colormap: cmapPrecip,
    range: [0, 14],
  },
};

function renderHeatmapImage(varKey: string): HTMLCanvasElement {
  const cfg = VARIABLES[varKey];
  const canvas = document.createElement('canvas');
  canvas.width = GRID_SIZE;
  canvas.height = GRID_SIZE;
  const ctx = canvas.getContext('2d')!;
  const imgData = ctx.createImageData(GRID_SIZE, GRID_SIZE);
  const grid = cfg.generate();
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
  return canvas;
}

export function ZarrTemperatureMap() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const [activeVar, setActiveVar] = useState('t2m');
  const [ready, setReady] = useState(false);

  const updateOverlay = useCallback((varKey: string) => {
    const map = mapRef.current;
    if (!map) return;
    const source = map.getSource('heatmap');
    if (!source) return;

    const heatCanvas = renderHeatmapImage(varKey);
    // Convert canvas to image for MapLibre
    const img = new Image();
    img.onload = () => {
      source.updateImage({
        url: heatCanvas.toDataURL(),
        coordinates: [
          [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
          [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
          [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
          [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
        ],
      });
    };
    img.src = heatCanvas.toDataURL();
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

        const heatCanvas = renderHeatmapImage('t2m');

        map = new maplibregl.default.Map({
          container: containerRef.current,
          style: {
            version: 8,
            sources: {
              'satellite': {
                type: 'raster',
                tiles: [
                  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                ],
                tileSize: 256,
                attribution: '&copy; Esri',
                maxzoom: 18,
              },
              'heatmap': {
                type: 'image',
                url: heatCanvas.toDataURL(),
                coordinates: [
                  [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
                  [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat + GRID_EXTENT],
                  [AUSTIN.lng + GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
                  [AUSTIN.lng - GRID_EXTENT, AUSTIN.lat - GRID_EXTENT],
                ],
              },
            },
            layers: [
              {
                id: 'satellite',
                type: 'raster',
                source: 'satellite',
              },
              {
                id: 'heatmap',
                type: 'raster',
                source: 'heatmap',
                paint: { 'raster-opacity': 0.7, 'raster-fade-duration': 0 },
              },
            ],
          },
          center: [AUSTIN.lng, AUSTIN.lat],
          zoom: 8,
          maxZoom: 12,
          minZoom: 6,
          attributionControl: false,
        });

        map.addControl(new maplibregl.default.NavigationControl(), 'top-right');

        map.on('load', () => {
          setReady(true);
        });

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

  // Update overlay when variable changes
  useEffect(() => {
    if (ready) updateOverlay(activeVar);
  }, [activeVar, ready, updateOverlay]);

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

      {/* Variable selector */}
      <div
        sx={{
          position: 'absolute',
          bottom: 12,
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: 1,
          bg: 'rgba(10, 10, 10, 0.85)',
          backdropFilter: 'blur(8px)',
          borderRadius: 6,
          p: '4px',
          zIndex: 10,
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
              fontSize: '12px',
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

      {/* Info overlay */}
      <div
        sx={{
          position: 'absolute',
          top: 12,
          left: 12,
          bg: 'rgba(10, 10, 10, 0.8)',
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
        <div sx={{ fontWeight: 600, fontSize: '13px' }}>
          ERA5 · {cfg.label}
        </div>
        <div sx={{ opacity: 0.6 }}>
          {cfg.range[0]}–{cfg.range[1]} {cfg.unit} · 0.25° grid · ECMWF Zarr
        </div>
      </div>
    </div>
  );
}
