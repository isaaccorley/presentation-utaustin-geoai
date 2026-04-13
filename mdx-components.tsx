import type { MDXComponents } from 'mdx/types';
import type React from 'react';
import { isValidElement } from 'react';
import { CodeBlock } from './components/CodeBlock';
import { Columns } from './components/Columns';
import { Diagram } from './components/Diagram';
import { Embed } from './components/Embed';
import { Img } from './components/Img';
import { Logo } from './components/Logo';
import { MapLibreEmbed } from './components/MapLibreEmbed';
import { PMTilesEmbed } from './components/PMTilesEmbed';
import { QRGrid } from './components/QRGrid';
import { SectionSlide } from './components/SectionSlide';
import { SpeakerNotes } from './components/SpeakerNotes';
import { TerminalReplay } from './components/TerminalReplay';
import { TitleSlide } from './components/TitleSlide';
import { Video } from './components/Video';
import { ZarrTemperatureMap } from './components/ZarrTemperatureMap';

/**
 * MDX component overrides for Next.js.
 * This file is required by @next/mdx to provide custom components to MDX files.
 *
 * The `hr` override is critical for slide splitting: Markdown `---` produces
 * `<hr>` elements, which we render as `<hr data-slide-separator />`. The Deck
 * component scans the rendered DOM for these markers to split content into
 * individual slides. This approach works with MDX v3's compiled output, where
 * all content renders as a single function component that can't be split
 * at the React element level.
 */
const bp = process.env.NEXT_PUBLIC_BASE_PATH || '';

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    hr: (props: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHRElement>, HTMLHRElement>) => (
      <hr {...props} data-slide-separator="" />
    ),
    img: (
      props: React.DetailedHTMLProps<React.ImgHTMLAttributes<HTMLImageElement>, HTMLImageElement>,
    ) => {
      const src = props.src?.startsWith('/') ? `${bp}${props.src}` : props.src;
      // eslint-disable-next-line @next/next/no-img-element
      return <img {...props} src={src} alt={props.alt || ''} />;
    },
    // Override <pre> to use our CodeBlock
    pre: ({
      children,
      ...props
    }: React.DetailedHTMLProps<React.HTMLAttributes<HTMLPreElement>, HTMLPreElement>) => {
      if (isValidElement(children) && children.type === 'code') {
        return (
          <CodeBlock className={children.props.className}>{children.props.children}</CodeBlock>
        );
      }
      return <pre {...props}>{children}</pre>;
    },
    // Expose custom components for MDX
    TitleSlide,
    SectionSlide,
    Embed,
    Columns,
    Logo,
    SpeakerNotes,
    Diagram,
    Img,
    Video,
    MapLibreEmbed,
    PMTilesEmbed,
    QRGrid,
    TerminalReplay,
    ZarrTemperatureMap,
  };
}
