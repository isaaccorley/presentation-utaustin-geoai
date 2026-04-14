/** @jsxImportSource theme-ui */

export interface EmbedProps {
  /** URL to embed in the iframe */
  src: string;
  /** Title for accessibility */
  title?: string;
  /**
   * Whether to clip the bottom of the iframe to hide the SlideNav bar.
   * Useful when the embedded page has its own navigation that conflicts.
   * Default: false
   */
  clip?: boolean;
  /** Render as an in-flow embed instead of a full-viewport takeover. */
  inline?: boolean;
  /** Height for inline embeds. */
  height?: number;
}

/**
 * Full-viewport iframe embed component by default.
 * Use `inline` for sized embeds that live inside a column.
 */
export function Embed({
  src,
  title = 'Embedded content',
  clip = false,
  inline = false,
  height = 440,
}: EmbedProps) {
  if (inline) {
    return (
      <div
        sx={{
          width: '100%',
          height,
          overflow: 'hidden',
          borderRadius: 8,
          border: '1px solid rgba(244,244,235,0.1)',
        }}
      >
        <iframe
          src={src}
          title={title}
          sx={{
            width: '100%',
            height: '100%',
            border: 'none',
          }}
          sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
          loading="lazy"
        />
      </div>
    );
  }

  return (
    <div
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: clip ? 'calc(100vh - 48px)' : '100vh',
        overflow: 'hidden',
        zIndex: 998,
      }}
    >
      <iframe
        src={src}
        title={title}
        sx={{
          width: '100%',
          height: '100%',
          border: 'none',
        }}
        sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
        loading="lazy"
      />
      {/* Fallback link if iframe fails to load */}
      <noscript>
        <a href={src} target="_blank" rel="noopener noreferrer">
          Open {title} in a new tab
        </a>
      </noscript>
    </div>
  );
}
