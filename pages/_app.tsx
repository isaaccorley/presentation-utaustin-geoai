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
 * Wraps the root deck page with ThemeUIProvider and the Deck engine.
 *
 * Custom MDX components are provided via mdx-components.tsx at the project root.
 */
export default function App({ Component, pageProps }: AppProps) {
  const router = useRouter();

  const isDeckPage = router.pathname === '/';

  if (isDeckPage) {
    return (
      <ThemeUIProvider theme={theme}>
        <Deck>
          <Component {...pageProps} />
        </Deck>
      </ThemeUIProvider>
    );
  }

  return (
    <ThemeUIProvider theme={theme}>
      <Component {...pageProps} />
    </ThemeUIProvider>
  );
}
