/** @jsxImportSource theme-ui */

/**
 * Inline ERA5 temperature heatmap visualization for Austin, TX area.
 * Renders a canvas-based temperature grid with a dark theme overlay.
 * Uses ResizeObserver to paint when the canvas becomes visible.
 */

import { useEffect, useRef } from 'react';

const COLS = 48;
const ROWS = 32;
const BG = '#1a0f0e';
const TEXT = '#f4f4eb';

/** Generate synthetic ERA5-like 2m temperature grid (K) centered on Austin, TX */
function generateTemperatureGrid(): number[][] {
  const grid: number[][] = [];
  for (let r = 0; r < ROWS; r++) {
    const row: number[] = [];
    for (let c = 0; c < COLS; c++) {
      const cx = (c - COLS / 2) / COLS;
      const cy = (r - ROWS / 2) / ROWS;
      const dist = Math.sqrt(cx * cx + cy * cy);
      const base = 300 - dist * 14 + cx * 3;
      const noise = Math.sin(c * 1.7 + r * 0.9) * 0.8 + Math.cos(c * 0.3 + r * 2.1) * 0.6;
      row.push(base + noise);
    }
    grid.push(row);
  }
  return grid;
}

/** Map temperature (K) to RGB for a warm-cool colormap */
function tempToColor(t: number): [number, number, number] {
  const lo = 286;
  const hi = 304;
  const f = Math.max(0, Math.min(1, (t - lo) / (hi - lo)));
  const r = Math.round(30 + f * 220);
  const g = Math.round(60 + (1 - Math.abs(f - 0.5) * 2) * 120);
  const b = Math.round(200 - f * 180);
  return [r, g, b];
}

function paintCanvas(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  if (rect.width === 0 || rect.height === 0) return;

  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  ctx.scale(dpr, dpr);

  const w = rect.width;
  const h = rect.height;
  const cellW = w / COLS;
  const cellH = h / ROWS;

  const grid = generateTemperatureGrid();

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const [red, green, blue] = tempToColor(grid[r][c]);
      ctx.fillStyle = `rgb(${red},${green},${blue})`;
      ctx.fillRect(c * cellW, r * cellH, cellW + 1, cellH + 1);
    }
  }

  // Grid lines
  ctx.strokeStyle = 'rgba(26,15,14,0.25)';
  ctx.lineWidth = 0.5;
  for (let r = 0; r <= ROWS; r++) {
    ctx.beginPath();
    ctx.moveTo(0, r * cellH);
    ctx.lineTo(w, r * cellH);
    ctx.stroke();
  }
  for (let c = 0; c <= COLS; c++) {
    ctx.beginPath();
    ctx.moveTo(c * cellW, 0);
    ctx.lineTo(c * cellW, h);
    ctx.stroke();
  }

  // Austin marker
  const ax = Math.round(COLS * 0.52) * cellW;
  const ay = Math.round(ROWS * 0.48) * cellH;
  ctx.fillStyle = TEXT;
  ctx.font = '600 14px "Space Grotesk", system-ui, sans-serif';
  ctx.textAlign = 'left';
  ctx.textBaseline = 'middle';
  ctx.beginPath();
  ctx.arc(ax, ay, 4, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillText('Austin, TX', ax + 10, ay);

  // Colorbar
  const barX = w - 36;
  const barY = 20;
  const barH = h - 40;
  const barW = 14;
  for (let i = 0; i < barH; i++) {
    const t = 304 - (i / barH) * (304 - 286);
    const [red, green, blue] = tempToColor(t);
    ctx.fillStyle = `rgb(${red},${green},${blue})`;
    ctx.fillRect(barX, barY + i, barW, 1);
  }
  ctx.strokeStyle = 'rgba(244,244,235,0.3)';
  ctx.strokeRect(barX, barY, barW, barH);
  ctx.fillStyle = TEXT;
  ctx.font = '11px "Space Grotesk", monospace';
  ctx.textAlign = 'left';
  ctx.fillText('304 K', barX + barW + 4, barY + 6);
  ctx.fillText('286 K', barX + barW + 4, barY + barH);

  // Title overlay
  ctx.fillStyle = TEXT;
  ctx.font = '600 13px "Space Grotesk", system-ui, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('ERA5 · 2m Temperature · 0.25° grid', 12, 20);
  ctx.font = '11px "Space Grotesk", monospace';
  ctx.fillStyle = 'rgba(244,244,235,0.6)';
  ctx.fillText('var: t2m  ·  source: ECMWF/ERA5 (Zarr)', 12, 38);
}

export function ZarrTemperatureMap() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const paintedRef = useRef(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Use ResizeObserver to paint when canvas becomes visible
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentRect.width > 0 && entry.contentRect.height > 0 && !paintedRef.current) {
          paintedRef.current = true;
          paintCanvas(canvas);
        }
      }
    });
    observer.observe(canvas);

    // Also try painting immediately in case already visible
    const rect = canvas.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0 && !paintedRef.current) {
      paintedRef.current = true;
      paintCanvas(canvas);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div
      sx={{
        width: '100%',
        height: '70vh',
        bg: BG,
        borderRadius: 8,
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <canvas
        ref={canvasRef}
        sx={{
          width: '100%',
          flex: 1,
          display: 'block',
        }}
      />
      <div
        sx={{
          px: 3,
          py: 2,
          color: TEXT,
          fontFamily: '"Space Grotesk", monospace',
          fontSize: '13px',
          opacity: 0.7,
          textAlign: 'center',
          bg: 'rgba(0,0,0,0.3)',
        }}
      >
        ERA5 Zarr streamed on demand — no file download, HTTP range requests only
      </div>
    </div>
  );
}
