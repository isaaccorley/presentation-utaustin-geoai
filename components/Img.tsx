/** @jsxImportSource theme-ui */

const bp = process.env.NEXT_PUBLIC_BASE_PATH || '';

export interface ImgProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src: string;
}

export function Img({ src, alt = '', ...props }: ImgProps) {
  const resolved = src.startsWith('/') ? `${bp}${src}` : src;
  // biome-ignore lint/a11y/useAltText: alt is passed via props by callers
  return <img src={resolved} alt={alt} {...props} />;
}
