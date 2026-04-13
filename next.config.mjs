import createMDX from '@next/mdx';
import remarkGfm from 'remark-gfm';

// When deploying to GitHub Pages, PAGES_BASE_PATH is set to the repo name
// (e.g. '/tg-slides-template'). During local dev, it's unset so everything
// serves from the root.
const basePath = process.env.PAGES_BASE_PATH || '';

/** @type {import('next').NextConfig} */
const nextConfig = {
  pageExtensions: ['ts', 'tsx', 'md', 'mdx'],
  reactStrictMode: false,
  output: 'export',
  basePath: basePath || undefined,
  assetPrefix: basePath || undefined,
  images: { unoptimized: true },
  env: { NEXT_PUBLIC_BASE_PATH: basePath },
};

const withMDX = createMDX({
  // MDX options
  options: {
    // Remark plugins
    remarkPlugins: [remarkGfm],
    // Rehype plugins (none needed for Phase 1)
    rehypePlugins: [],
  },
});

export default withMDX(nextConfig);
