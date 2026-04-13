/** @jsxImportSource theme-ui */
import type { AppProps } from 'next/app';
import { useRouter } from 'next/router';
import { ThemeUIProvider } from 'theme-ui';
import { Deck } from '../components/Deck';
import theme from '../theme';
import 'maplibre-gl/dist/maplibre-gl.css';
import '../styles/globals.css';

/**
 * Custom App component.
 * Wraps all pages with ThemeUIProvider.
 *
 * Pages under /decks/ are wrapped in the Deck component for slide
 * functionality. All other pages (e.g. the library splash page at /)
 * render without the Deck wrapper.
 *
 * Custom MDX components are provided via mdx-components.tsx at the project root.
 */
export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();

  // Only wrap pages under /decks/ with the slide Deck engine.
  // Match both /decks/slug and exactly /decks to avoid false positives
  // like a hypothetical /decks-archive page.
  const isDeckPage = router.pathname === '/' || router.pathname === '/decks' || router.pathname.startsWith('/decks/');

  if (isDeckPage) {
    return (
      <ThemeUIProvider theme={theme}>
        <Deck>
          <Component {...pageProps} />
        </Deck>
      </ThemeUIProvider>
    );
  }

  // Non-deck pages (library, etc.) render without the Deck wrapper
  return (
    <ThemeUIProvider theme={theme}>
      <Component {...pageProps} />
    </ThemeUIProvider>
  );
}
