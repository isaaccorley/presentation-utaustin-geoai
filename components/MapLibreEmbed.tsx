/** @jsxImportSource theme-ui */

/**
 * Full-viewport MapLibre GL JS embed showing Overture Maps buildings via PMTiles.
 * Dark-themed to match TG brand. Flies to UT Austin campus on load.
 * Uses ResizeObserver to initialize only when the container is visible.
 */

import { useEffect, useRef } from 'react';

const OVERTURE_BUILDINGS_URL =
  'https://overturemaps-tiles-us-west-2-beta.s3.amazonaws.com/2026-01-21/buildings.pmtiles';

const UT_AUSTIN = { lng: -97.7365, lat: 30.2849 };

let protocolRegistered = false;

export function MapLibreEmbed() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (!containerRef.current) return;

    let map: any;
    let cancelled = false;
    let observer: ResizeObserver | null = null;

    function initMap() {
      if (cancelled || !containerRef.current || mapRef.current) return;

      // Don't init if container has zero dimensions (hidden slide)
      const rect = containerRef.current.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      (async () => {
        const [maplibregl, pmtiles] = await Promise.all([
          import('maplibre-gl'),
          import('pmtiles'),
        ]);

        if (cancelled || !containerRef.current) return;

        if (!protocolRegistered) {
          const protocol = new pmtiles.Protocol();
          maplibregl.default.addProtocol('pmtiles', protocol.tile);
          protocolRegistered = true;
        }

        map = new maplibregl.default.Map({
          container: containerRef.current,
          style: {
            version: 8,
            glyphs: 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
            sources: {
              buildings: {
                type: 'vector',
                url: `pmtiles://${OVERTURE_BUILDINGS_URL}`,
              },
            },
            layers: [
              {
                id: 'background',
                type: 'background',
                paint: { 'background-color': '#1a0f0e' },
              },
              {
                id: 'buildings-fill',
                type: 'fill',
                source: 'buildings',
                'source-layer': 'building',
                paint: {
                  'fill-color': '#80a0d8',
                  'fill-opacity': ['interpolate', ['linear'], ['zoom'], 10, 0.15, 14, 0.4, 17, 0.6],
                },
              },
              {
                id: 'buildings-outline',
                type: 'line',
                source: 'buildings',
                'source-layer': 'building',
                paint: {
                  'line-color': '#a7d0dc',
                  'line-width': ['interpolate', ['linear'], ['zoom'], 13, 0.2, 17, 0.8],
                  'line-opacity': ['interpolate', ['linear'], ['zoom'], 10, 0.1, 15, 0.4],
                },
              },
            ],
          },
          center: [UT_AUSTIN.lng - 2, UT_AUSTIN.lat - 1],
          zoom: 4,
          maxZoom: 18,
          attributionControl: false,
        });

        map.addControl(new maplibregl.default.AttributionControl({ compact: true }), 'bottom-left');
        map.addControl(new maplibregl.default.NavigationControl(), 'top-right');

        map.on('load', () => {
          map.flyTo({
            center: [UT_AUSTIN.lng, UT_AUSTIN.lat],
            zoom: 15,
            duration: 4000,
            curve: 1.8,
          });
        });

        mapRef.current = map;
      })();
    }

    // Use ResizeObserver to detect when container becomes visible
    observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.contentRect.width > 0 && entry.contentRect.height > 0 && !mapRef.current) {
          initMap();
        }
      }
    });
    observer.observe(containerRef.current);

    // Try immediately in case already visible
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

  return (
    <div
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: 'calc(100vh - 48px)',
        overflow: 'hidden',
        zIndex: 998,
      }}
    >
      <div ref={containerRef} sx={{ width: '100%', height: '100%' }} />
      <div
        sx={{
          position: 'absolute',
          top: 16,
          left: 16,
          bg: 'rgba(26, 15, 14, 0.85)',
          color: '#f4f4eb',
          px: 3,
          py: 2,
          borderRadius: 6,
          fontFamily: '"Space Grotesk", system-ui, sans-serif',
          fontSize: '13px',
          zIndex: 999,
          backdropFilter: 'blur(8px)',
        }}
      >
        <strong>Overture Maps</strong> — 2.6B building footprints via PMTiles
      </div>
    </div>
  );
}
