/** @jsxImportSource theme-ui */
import type { ReactNode } from 'react';

export interface SectionSlideProps {
  /** The big text to display */
  children: ReactNode;
  /** Optional background image URL. A dark scrim is applied for readability. */
  backgroundImage?: string;
  /** Optional background video URL. Loops muted behind a dark scrim. */
  backgroundVideo?: string;
  /** Optional kicker text above the heading (e.g. section number) */
  kicker?: string;
}

/**
 * Big centered text section divider.
 * Use for dramatic statements or topic transitions.
 * Supports an optional satellite/background image with a dark overlay.
 */
export function SectionSlide({
  children,
  backgroundImage,
  backgroundVideo,
  kicker,
}: SectionSlideProps) {
  const bp = process.env.NEXT_PUBLIC_BASE_PATH || '';
  const bgUrl = backgroundImage?.startsWith('/') ? `${bp}${backgroundImage}` : backgroundImage;
  const vidUrl = backgroundVideo?.startsWith('/') ? `${bp}${backgroundVideo}` : backgroundVideo;
  const hasBackground = !!backgroundImage || !!backgroundVideo;

  return (
    <div
      data-slide-type="section"
      sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        height: '100%',
        position: 'relative',
        '& > *:not([aria-hidden]):not([data-kicker])': {
          fontSize: 8,
          lineHeight: 'tight',
          fontWeight: 'bold',
          maxWidth: '80%',
          position: 'relative',
          zIndex: 2,
          ...(hasBackground && { color: '#f4f4eb' }),
        },
      }}
    >
      {bgUrl && (
        <div
          aria-hidden="true"
          sx={{
            position: 'absolute',
            inset: 0,
            backgroundImage: `url(${bgUrl})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            zIndex: 0,
            '&::after': {
              content: '""',
              position: 'absolute',
              inset: 0,
              bg: 'rgba(26, 15, 14, 0.55)',
            },
          }}
        />
      )}
      {vidUrl && (
        <div
          aria-hidden="true"
          sx={{
            position: 'absolute',
            inset: 0,
            overflow: 'hidden',
            zIndex: 0,
            '&::after': {
              content: '""',
              position: 'absolute',
              inset: 0,
              bg: 'rgba(26, 15, 14, 0.55)',
              zIndex: 1,
            },
          }}
        >
          <video
            src={vidUrl}
            autoPlay
            loop
            muted
            playsInline
            sx={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
            }}
          />
        </div>
      )}
      {kicker && (
        <span
          data-kicker="true"
          sx={{
            fontSize: 1,
            fontWeight: 'medium',
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
            color: hasBackground ? 'rgba(244, 244, 235, 0.6)' : 'textMuted',
            position: 'relative',
            zIndex: 2,
            mb: 3,
          }}
        >
          {kicker}
        </span>
      )}
      {children}
    </div>
  );
}
