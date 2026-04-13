/** @jsxImportSource theme-ui */
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
 *
 * Critical: `hr` → `<hr data-slide-separator />` for slide splitting.
 *
 * We apply theme-aware sx styles to all prose elements here because
 * Theme-UI's `styles.*` config only affects `Styled.*` components, not
 * native HTML elements. Without these overrides, MDX renders at browser
 * default sizes (16px) regardless of the theme.
 */
const bp = process.env.NEXT_PUBLIC_BASE_PATH || '';

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,

    // --- Slide separator ---
    hr: (props: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHRElement>, HTMLHRElement>) => (
      <hr {...props} data-slide-separator="" />
    ),

    // --- Prose elements with theme-ui font sizes ---
    h1: (props) => (
      <h1
        sx={{
          fontFamily: 'heading',
          fontWeight: 'bold',
          fontSize: 6,
          lineHeight: 'tight',
          mt: 0,
          mb: 4,
          letterSpacing: '-0.02em',
          color: 'text',
        }}
        {...props}
      />
    ),
    h2: (props) => (
      <h2
        sx={{
          fontFamily: 'heading',
          fontWeight: 'bold',
          fontSize: 5,
          lineHeight: 'tight',
          mt: 0,
          mb: 3,
          letterSpacing: '-0.01em',
          color: 'text',
        }}
        {...props}
      />
    ),
    h3: (props) => (
      <h3
        sx={{
          fontFamily: 'heading',
          fontWeight: 'medium',
          fontSize: 4,
          lineHeight: 'snug',
          mt: 0,
          mb: 3,
          color: 'text',
        }}
        {...props}
      />
    ),
    h4: (props) => (
      <h4
        sx={{
          fontFamily: 'heading',
          fontWeight: 'medium',
          fontSize: 3,
          lineHeight: 'snug',
          mt: 0,
          mb: 2,
          color: 'text',
        }}
        {...props}
      />
    ),
    p: (props) => (
      <p
        sx={{
          fontSize: 3,
          lineHeight: 'normal',
          mt: 0,
          mb: 3,
          color: 'text',
        }}
        {...props}
      />
    ),
    ul: (props) => (
      <ul
        sx={{
          fontSize: 3,
          lineHeight: 'relaxed',
          pl: 5,
          mt: 0,
          mb: 3,
          listStyleType: 'none',
          '& > li': {
            position: 'relative',
            pl: 4,
            '&::before': {
              content: '""',
              position: 'absolute',
              left: 0,
              top: '0.65em',
              width: '6px',
              height: '1.5px',
              bg: 'textMuted',
              borderRadius: 'full',
            },
          },
        }}
        {...props}
      />
    ),
    ol: (props) => (
      <ol
        sx={{
          fontSize: 3,
          lineHeight: 'relaxed',
          pl: 5,
          mt: 0,
          mb: 3,
          counterReset: 'ol-counter',
          listStyleType: 'none',
          '& > li': {
            position: 'relative',
            pl: 5,
            counterIncrement: 'ol-counter',
            '&::before': {
              content: 'counter(ol-counter) "."',
              position: 'absolute',
              left: 0,
              top: 0,
              fontFamily: 'monospace',
              fontSize: '0.85em',
              fontWeight: 'medium',
              color: 'textMuted',
            },
          },
        }}
        {...props}
      />
    ),
    li: (props) => <li sx={{ mb: 2 }} {...props} />,
    blockquote: (props) => (
      <blockquote
        sx={{
          borderLeft: '3px solid var(--theme-ui-colors-accent)',
          pl: 4,
          py: 3,
          ml: 0,
          my: 4,
          bg: 'surface',
          borderRadius: 'sm',
          color: 'textSecondary',
          fontStyle: 'italic',
          fontSize: 3,
          '& p': { m: 0, fontSize: 'inherit' },
        }}
        {...props}
      />
    ),
    strong: (props) => <strong sx={{ fontWeight: 'bold', color: 'text' }} {...props} />,
    a: (props) => (
      <a
        sx={{
          color: 'accent',
          textDecoration: 'none',
          '&:hover': { textDecoration: 'underline' },
        }}
        {...props}
      />
    ),
    code: (props) => (
      <code
        sx={{
          fontFamily: 'monospace',
          fontSize: '0.9em',
          bg: 'surface',
          color: 'accent',
          px: 1,
          py: '2px',
          borderRadius: 'sm',
        }}
        {...props}
      />
    ),
    table: (props) => (
      <table
        sx={{
          borderCollapse: 'collapse',
          fontSize: [3, 4],
          mb: 3,
          width: '100%',
          border: '2px solid var(--theme-ui-colors-border)',
          borderRadius: 'md',
          overflow: 'hidden',
        }}
        {...props}
      />
    ),
    th: (props) => (
      <th
        sx={{
          border: '1px solid var(--theme-ui-colors-border)',
          p: 3,
          textAlign: 'left',
          fontWeight: 'bold',
          fontSize: [2, 3],
          color: 'text',
          bg: 'surface',
        }}
        {...props}
      />
    ),
    td: (props) => (
      <td
        sx={{
          border: '1px solid var(--theme-ui-colors-border)',
          p: 3,
        }}
        {...props}
      />
    ),
    tr: (props) => (
      <tr
        sx={{
          '&:nth-of-type(even)': {
            bg: 'surface',
          },
        }}
        {...props}
      />
    ),

    // --- Code block (fenced) ---
    pre: ({
      children,
      ...props
    }: React.DetailedHTMLProps<React.HTMLAttributes<HTMLPreElement>, HTMLPreElement>) => {
      if (isValidElement(children) && children.type === 'code') {
        return (
          <CodeBlock className={children.props.className}>{children.props.children}</CodeBlock>
        );
      }
      if (isValidElement(children)) {
        const { className, children: codeContent } = children.props as {
          className?: string;
          children?: string;
        };
        if (typeof codeContent === 'string') {
          return <CodeBlock className={className}>{codeContent}</CodeBlock>;
        }
      }
      return <pre {...props}>{children}</pre>;
    },

    img: (
      props: React.DetailedHTMLProps<React.ImgHTMLAttributes<HTMLImageElement>, HTMLImageElement>,
    ) => {
      const src = props.src?.startsWith('/') ? `${bp}${props.src}` : props.src;
      // eslint-disable-next-line @next/next/no-img-element
      return <img {...props} src={src} alt={props.alt || ''} />;
    },

    // --- Custom slide components ---
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
