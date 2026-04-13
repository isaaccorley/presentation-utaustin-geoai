/** @jsxImportSource theme-ui */

/**
 * Full-viewport PMTiles embed showing Overture Maps buildings.
 * Uses protomaps PMTiles viewer with a preset Overture buildings archive.
 */

const PMTILES_VIEWER = 'https://protomaps.github.io/PMTiles/';
const OVERTURE_BUILDINGS_URL =
  'https://overturemaps-tiles-us-west-2.s3.amazonaws.com/2025-03-19.0/buildings.pmtiles';

export function PMTilesEmbed() {
  const src = `${PMTILES_VIEWER}?url=${encodeURIComponent(OVERTURE_BUILDINGS_URL)}`;

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
      <iframe
        src={src}
        title="PMTiles — Overture Maps Buildings"
        sx={{
          width: '100%',
          height: '100%',
          border: 'none',
        }}
        sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
        loading="lazy"
      />
      <noscript>
        <a href={src} target="_blank" rel="noopener noreferrer">
          Open PMTiles viewer in a new tab
        </a>
      </noscript>
    </div>
  );
}
