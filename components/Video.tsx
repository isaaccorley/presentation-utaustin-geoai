/** @jsxImportSource theme-ui */

export interface VideoProps {
  src: string;
  poster?: string;
  autoPlay?: boolean;
  loop?: boolean;
  title?: string;
}

export function Video({
  src,
  poster,
  autoPlay = false,
  loop = false,
  title,
}: VideoProps) {
  return (
    <div
      sx={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        overflow: 'hidden',
        bg: 'black',
      }}
    >
      <video
        src={src}
        poster={poster}
        autoPlay={autoPlay}
        loop={loop}
        muted
        controls
        playsInline
        title={title}
        sx={{
          width: '100%',
          height: '100%',
          objectFit: 'contain',
        }}
      />
    </div>
  );
}
