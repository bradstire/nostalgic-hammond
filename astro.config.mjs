// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import { towns, resolveTownSlug } from './src/config/towns.mjs';

// One codebase, many towns: PUBLIC_TOWN picks the town for this build (unset = hammond).
const town = towns[resolveTownSlug(process.env.PUBLIC_TOWN)];

// https://astro.build/config
export default defineConfig({
  site: town.siteUrl,
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
