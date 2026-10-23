// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';
import { towns, resolveTownSlug } from './src/config/towns.mjs';
import hiddenProducts from './src/v2/hidden.json';

// One codebase, many towns. The town for this build comes from PUBLIC_TOWN (set per Vercel project),
// or from a git branch named `town/<slug>` (so pushing that branch yields a private Vercel preview).
// Unset = hammond.
const branchTown = (process.env.VERCEL_GIT_COMMIT_REF || '').match(/^town\/([a-z0-9-]+)$/)?.[1];
const townSlug = resolveTownSlug(process.env.PUBLIC_TOWN || branchTown);
const town = towns[townSlug];
// Each town picks a storefront layout: 'v2' (shop by place, src/v2/site) or the original (src/legacy/site).
const siteDir = town.layout === 'v2' ? './src/v2/site' : './src/legacy/site';
// v2 builds its 404 at /404/ (a param route); publish it as /404.html for Vercel. No-op for other layouts.
const v2NotFound = {
  name: 'v2-404',
  hooks: {
    'astro:build:done': async ({ dir }) => {
      if (town.layout !== 'v2') return;
      const src = new URL('404/index.html', dir);
      if (fs.existsSync(src)) fs.copyFileSync(src, new URL('404.html', dir));
    },
  },
};

// https://astro.build/config
export default defineConfig({
  // v2 towns inline their stylesheet (removes a render-blocking request); the original layout is unchanged.
  build: { inlineStylesheets: town.layout === 'v2' ? 'always' : 'auto' },
  site: town.siteUrl,
  integrations: [tailwind({ applyBaseStyles: false }), sitemap({ filter: (page) => !page.includes('/404') && !hiddenProducts.some((h) => page.endsWith(`/products/${h}/`)) }), v2NotFound],
  image: {
    // Disable image optimization - serve original PNGs with transparency
    service: {
      entrypoint: 'astro/assets/services/noop'
    }
  },
  vite: {
    resolve: { alias: { '@site': fileURLToPath(new URL(siteDir, import.meta.url)) } },
    // One resolved value for server and client code (src/config/site.config.ts reads it).
    define: {
      'import.meta.env.PUBLIC_TOWN': JSON.stringify(townSlug),
    },
    build: {
      assetsInlineLimit: 0
    }
  }
});
