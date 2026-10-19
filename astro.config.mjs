// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import { towns, resolveTownSlug } from './src/config/towns.mjs';

// One codebase, many towns. The town for this build comes from PUBLIC_TOWN (set per Vercel project),
// or from a git branch named `town/<slug>` (so pushing that branch yields a private Vercel preview).
// Unset = hammond.
const branchTown = (process.env.VERCEL_GIT_COMMIT_REF || '').match(/^town\/([a-z0-9-]+)$/)?.[1];
const townSlug = resolveTownSlug(process.env.PUBLIC_TOWN || branchTown);
const town = towns[townSlug];

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
    // One resolved value for server and client code (src/config/site.config.ts reads it).
    define: {
      'import.meta.env.PUBLIC_TOWN': JSON.stringify(townSlug),
    },
    build: {
      assetsInlineLimit: 0
    }
  }
});
