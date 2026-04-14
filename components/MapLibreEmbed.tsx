/** @jsxImportSource theme-ui */

/**
 * Full-viewport MapLibre GL JS embed showing Overture Maps via PMTiles.
 * Dark basemap + buildings colored by subtype + water/roads context layers.
 * Hover popup with building details. Flies to UT Austin campus on load.
 */

import type { DataDrivenPropertyValueSpecification } from '@maplibre/maplibre-gl-style-spec';
import type { MapGeoJSONFeature, MapLayerMouseEvent, Map as MapLibreMap, Popup } from 'maplibre-gl';
import { useEffect, useRef } from 'react';

const OVERTURE_BASE = 'https://overturemaps-tiles-us-west-2-beta.s3.amazonaws.com/2026-01-21';
const BUILDINGS_URL = `${OVERTURE_BASE}/buildings.pmtiles`;
const BASE_URL = `${OVERTURE_BASE}/base.pmtiles`;
const TRANSPORT_URL = `${OVERTURE_BASE}/transportation.pmtiles`;

const UT_AUSTIN = { lng: -97.7365, lat: 30.2849 };

// Building subtype → fill color
const SUBTYPE_COLORS: [string, string][] = [
  ['education', '#f59e0b'],
  ['civic', '#a78bfa'],
  ['commercial', '#60a5fa'],
  ['residential', '#6ee7b7'],
  ['industrial', '#f87171'],
  ['medical', '#fb923c'],
  ['religious', '#e879f9'],
  ['entertainment', '#fbbf24'],
  ['transportation', '#94a3b8'],
  ['military', '#78716c'],
  ['agricultural', '#86efac'],
  ['service', '#67e8f9'],
];

let protocolRegistered = false;

export function MapLibreEmbed() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MapLibreMap | null>(null);
  const popupRef = useRef<Popup | null>(null);

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
        const [maplibregl, pmtiles] = await Promise.all([import('maplibre-gl'), import('pmtiles')]);

        if (cancelled || !containerRef.current) return;

        if (!protocolRegistered) {
          const protocol = new pmtiles.Protocol();
          maplibregl.default.addProtocol('pmtiles', protocol.tile);
          protocolRegistered = true;
        }

        // Build match expression for subtype colors
        const colorMatch = ['match', ['get', 'subtype']] as Array<string | number | string[]>;
        for (const [subtype, color] of SUBTYPE_COLORS) {
          colorMatch.push(subtype, color);
        }
        colorMatch.push('#80a0d8');

        map = new maplibregl.default.Map({
          container: containerRef.current,
          style: {
            version: 8,
            glyphs: 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
            sources: {
              'carto-dark': {
                type: 'raster',
                tiles: [
                  'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
                  'https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
                  'https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
                ],
                tileSize: 256,
                attribution: '&copy; CARTO &copy; OSM',
              },
              base: {
                type: 'vector',
                url: `pmtiles://${BASE_URL}`,
              },
              transportation: {
                type: 'vector',
                url: `pmtiles://${TRANSPORT_URL}`,
              },
              buildings: {
                type: 'vector',
                url: `pmtiles://${BUILDINGS_URL}`,
              },
            },
            layers: [
              // Dark basemap
              {
                id: 'basemap',
                type: 'raster',
                source: 'carto-dark',
                paint: { 'raster-opacity': 0.7 },
              },
              // Water
              {
                id: 'water-fill',
                type: 'fill',
                source: 'base',
                'source-layer': 'water',
                paint: {
                  'fill-color': '#1a3a5c',
                  'fill-opacity': 0.6,
                },
              },
              // Roads — major
              {
                id: 'roads-major',
                type: 'line',
                source: 'transportation',
                'source-layer': 'segment',
                filter: ['in', 'class', 'motorway', 'trunk', 'primary'],
                paint: {
                  'line-color': '#4a4540',
                  'line-width': ['interpolate', ['linear'], ['zoom'], 10, 0.5, 14, 2, 17, 4],
                  'line-opacity': 0.6,
                },
              },
              // Roads — secondary
              {
                id: 'roads-secondary',
                type: 'line',
                source: 'transportation',
                'source-layer': 'segment',
                filter: ['in', 'class', 'secondary', 'tertiary'],
                minzoom: 12,
                paint: {
                  'line-color': '#3a3530',
                  'line-width': ['interpolate', ['linear'], ['zoom'], 12, 0.3, 17, 2],
                  'line-opacity': 0.4,
                },
              },
              // Buildings — fill colored by subtype
              {
                id: 'buildings-fill',
                type: 'fill',
                source: 'buildings',
                'source-layer': 'building',
                paint: {
                  'fill-color': colorMatch as DataDrivenPropertyValueSpecification<string>,
                  'fill-opacity': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    10,
                    0.15,
                    14,
                    0.35,
                    17,
                    0.55,
                  ],
                },
              },
              // Buildings — outline
              {
                id: 'buildings-outline',
                type: 'line',
                source: 'buildings',
                'source-layer': 'building',
                minzoom: 14,
                paint: {
                  'line-color': 'rgba(244, 244, 235, 0.15)',
                  'line-width': ['interpolate', ['linear'], ['zoom'], 14, 0.2, 17, 0.6],
                },
              },
              // Buildings — hover highlight (filtered to nothing by default)
              {
                id: 'buildings-highlight',
                type: 'fill',
                source: 'buildings',
                'source-layer': 'building',
                filter: ['==', 'id', ''],
                paint: {
                  'fill-color': '#ffffff',
                  'fill-opacity': 0.3,
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

        // Popup for hover
        const popup = new maplibregl.default.Popup({
          closeButton: false,
          closeOnClick: false,
          maxWidth: '280px',
          offset: 12,
        });
        popupRef.current = popup;
        const mapInstance = map;
        if (!mapInstance) return;

        // Hover interaction
        mapInstance.on('mousemove', 'buildings-fill', (e: MapLayerMouseEvent) => {
          const feature = e.features?.[0] as MapGeoJSONFeature | undefined;
          if (!feature) return;
          mapInstance.getCanvas().style.cursor = 'pointer';

          const p = feature.properties as {
            '@name'?: string;
            class?: string;
            subtype?: string;
            height?: string | number;
            num_floors?: string | number;
            roof_shape?: string;
            facade_material?: string;
          };

          // Highlight building
          mapInstance.setFilter('buildings-highlight', ['==', 'id', feature.id ?? '']);

          // Build popup HTML
          const name = p['@name'] || p.class || 'Building';
          const rows: string[] = [];

          if (p.subtype) rows.push(`<b>Type:</b> ${p.subtype}${p.class ? ` / ${p.class}` : ''}`);
          if (p.height) rows.push(`<b>Height:</b> ${Number(p.height).toFixed(1)}m`);
          if (p.num_floors) rows.push(`<b>Floors:</b> ${p.num_floors}`);
          if (p.roof_shape) rows.push(`<b>Roof:</b> ${p.roof_shape}`);
          if (p.facade_material) rows.push(`<b>Facade:</b> ${p.facade_material}`);

          const html = `
            <div style="font-family:'Space Grotesk',system-ui,sans-serif;font-size:13px;line-height:1.5;color:#f4f4eb">
              <div style="font-weight:700;font-size:14px;margin-bottom:4px;color:#fff">${name}</div>
              ${rows.length ? rows.join('<br/>') : '<span style="opacity:0.5">No metadata</span>'}
            </div>
          `;

          popup.setLngLat(e.lngLat).setHTML(html).addTo(mapInstance);
        });

        mapInstance.on('mouseleave', 'buildings-fill', () => {
          mapInstance.getCanvas().style.cursor = '';
          mapInstance.setFilter('buildings-highlight', ['==', 'id', '']);
          popup.remove();
        });

        mapInstance.on('load', () => {
          mapInstance.flyTo({
            center: [UT_AUSTIN.lng, UT_AUSTIN.lat],
            zoom: 15,
            duration: 4000,
            curve: 1.8,
          });
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
      popupRef.current?.remove();
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

      {/* Title badge */}
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

      {/* Legend */}
      <div
        sx={{
          position: 'absolute',
          bottom: 40,
          right: 16,
          bg: 'rgba(26, 15, 14, 0.85)',
          backdropFilter: 'blur(8px)',
          color: '#f4f4eb',
          px: 3,
          py: 2,
          borderRadius: 6,
          fontFamily: '"Space Grotesk", system-ui, sans-serif',
          fontSize: '11px',
          zIndex: 999,
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '3px 12px',
          lineHeight: 1.6,
        }}
      >
        {SUBTYPE_COLORS.slice(0, 8).map(([label, color]) => (
          <div key={label} sx={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span sx={{ width: 8, height: 8, borderRadius: 2, bg: color, flexShrink: 0 }} />
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}
