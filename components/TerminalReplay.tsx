/** @jsxImportSource theme-ui */

/**
 * Asciinema terminal replay component for pre-recorded CLI demos.
 * Auto-plays on mount, loops, and uses TG brand colors.
 */

import { useEffect, useRef } from 'react';

const bp = process.env.NEXT_PUBLIC_BASE_PATH || '';

export interface TerminalReplayProps {
  /** Path to the .cast file (relative to public/) */
  src: string;
  /** Playback speed multiplier (default: 1.5) */
  speed?: number;
  /** Terminal columns (default: 100) */
  cols?: number;
  /** Terminal rows (default: 28) */
  rows?: number;
  /** Title shown above the terminal */
  title?: string;
}

export function TerminalReplay({
  src,
  speed = 1.5,
  cols = 100,
  rows = 28,
  title,
}: TerminalReplayProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const playerRef = useRef<unknown>(null);

  const resolvedSrc = src.startsWith('/') ? `${bp}${src}` : src;

  useEffect(() => {
    if (!containerRef.current || playerRef.current) return;

    let mounted = true;

    import('asciinema-player').then((AsciinemaPlayer) => {
      if (!mounted || !containerRef.current) return;

      playerRef.current = AsciinemaPlayer.create(resolvedSrc, containerRef.current, {
        speed,
        cols,
        rows,
        autoPlay: true,
        loop: true,
        fit: 'width',
        theme: 'custom-tg',
        terminalFontFamily: '"JetBrains Mono", "Fira Code", "Cascadia Code", monospace',
        terminalFontSize: '15px',
      });
    });

    return () => {
      mounted = false;
      if (
        playerRef.current &&
        typeof (playerRef.current as { dispose?: () => void }).dispose === 'function'
      ) {
        (playerRef.current as { dispose: () => void }).dispose();
      }
      playerRef.current = null;
    };
  }, [resolvedSrc, speed, cols, rows]);

  return (
    <div
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100%',
        gap: 3,
      }}
    >
      {title && (
        <h2 sx={{ fontSize: [4, 5], fontWeight: 'bold', m: 0, textAlign: 'center' }}>{title}</h2>
      )}
      <div
        ref={containerRef}
        sx={{
          width: '90%',
          maxWidth: 960,
          borderRadius: 8,
          overflow: 'hidden',
          boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
          // Asciinema player theme overrides
          '.asciinema-player': {
            bg: '#1a0f0e !important',
          },
          '.asciinema-terminal': {
            color: '#f4f4eb',
            bg: '#1a0f0e',
          },
          // Custom TG color scheme via CSS custom properties
          '--term-color-foreground': '#f4f4eb',
          '--term-color-background': '#1a0f0e',
          '--term-color-0': '#3b1e1c', // black
          '--term-color-1': '#ff4f2c', // red (TG red)
          '--term-color-2': '#cff29e', // green (TG green)
          '--term-color-3': '#fbbf24', // yellow (TG yellow)
          '--term-color-4': '#80a0d8', // blue (TG periwinkle)
          '--term-color-5': '#a7d0dc', // magenta → light blue
          '--term-color-6': '#a7d0dc', // cyan (TG light blue)
          '--term-color-7': '#f4f4eb', // white (TG ivory)
        }}
      />
    </div>
  );
}
