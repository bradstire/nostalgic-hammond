// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.nostalgichammond.com',
  integrations: [tailwind(), sitemap()],
  image: {
    // Disable image optimization - serve original PNGs with transparency
    service: {
      entrypoint: 'astro/assets/services/noop'
    }
  },
  vite: {
    build: {
      assetsInlineLimit: 0
    }
  }
});
