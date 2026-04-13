/** @jsxImportSource theme-ui */

const bp = process.env.NEXT_PUBLIC_BASE_PATH || '';

export interface VideoProps {
  src: string;
  poster?: string;
  autoPlay?: boolean;
  loop?: boolean;
  title?: string;
}

export function Video({ src, poster, autoPlay = true, loop = true, title }: VideoProps) {
  const resolvedSrc = src.startsWith('/') ? `${bp}${src}` : src;
  const resolvedPoster = poster?.startsWith('/') ? `${bp}${poster}` : poster;

  return (
    <video
      src={resolvedSrc}
      poster={resolvedPoster}
      autoPlay={autoPlay}
      loop={loop}
      muted
      controls
      playsInline
      title={title}
      sx={{
        width: '100%',
        height: 'auto',
        maxHeight: '72vh',
        borderRadius: 6,
        objectFit: 'contain',
        bg: 'background',
      }}
    />
  );
}
