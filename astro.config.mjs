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
// Town-specific v2 components (hero, story band, about page body): src/v2/towns/<slug>/.
const townDir = `./src/v2/towns/${townSlug}`;
// Image folders under public/ that belong to one town only; other towns' builds leave them out of dist.
const TOWN_ONLY_ASSETS = { hammond: 'images/hm', sfv: 'images/sfv' };
// v2 builds its 404 at /404/ (a param route); publish it as /404.html for Vercel. No-op for other layouts.
const v2NotFound = {
  name: 'v2-404',
  hooks: {
    'astro:build:done': async ({ dir }) => {
      for (const [slug, rel] of Object.entries(TOWN_ONLY_ASSETS)) {
        if (slug !== townSlug) fs.rmSync(new URL(rel, dir), { recursive: true, force: true });
      }
      // strictAssets towns: keep only their own image folder, swap in their favicon, drop other sites' verification files.
      if (town.strictAssets && TOWN_ONLY_ASSETS[townSlug]) {
        const imgs = new URL('images/', dir), own = TOWN_ONLY_ASSETS[townSlug].split('/')[1];
        for (const e of fs.readdirSync(imgs)) if (e !== own) fs.rmSync(new URL(e, imgs), { recursive: true, force: true });
        for (const e of fs.readdirSync(dir)) if (/^google[0-9a-f]+\.html$/.test(e) || e === 'favicon.svg') fs.rmSync(new URL(e, dir), { force: true });
        const ico = new URL(TOWN_ONLY_ASSETS[townSlug] + '/favicon.ico', dir);
        if (fs.existsSync(ico)) fs.copyFileSync(ico, new URL('favicon.ico', dir));
      }
      // A town's own Search Console verification file (URL-prefix property), written into its dist only.
      if (town.gscFile) fs.writeFileSync(new URL(town.gscFile, dir), `google-site-verification: ${town.gscFile}`);
      if (town.bingAuth) fs.writeFileSync(new URL('BingSiteAuth.xml', dir), `<?xml version="1.0"?>\n<users>\n\t<user>${town.bingAuth}</user>\n</users>\n`);
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
  // Old URLs a town's earlier layout published, sent to their v2 pages (src/config/towns.mjs).
  redirects: town.redirects || {},
  integrations: [tailwind({ applyBaseStyles: false }), sitemap({ filter: (page) => !page.includes('/404') && !hiddenProducts.some((h) => page.endsWith(`/products/${h}/`)) }), v2NotFound],
  image: {
    // Disable image optimization - serve original PNGs with transparency
    service: {
      entrypoint: 'astro/assets/services/noop'
    }
  },
  vite: {
    resolve: { alias: { '@site': fileURLToPath(new URL(siteDir, import.meta.url)), '@town': fileURLToPath(new URL(townDir, import.meta.url)) } },
    // One resolved value for server and client code (src/config/site.config.ts reads it).
    define: {
      'import.meta.env.PUBLIC_TOWN': JSON.stringify(townSlug),
      // Email signup (src/v2/signup.ts): the town's Klaviyo list and the source label on new profiles.
      'import.meta.env.PUBLIC_KLAVIYO_LIST': JSON.stringify(town.klaviyoList || ''),
      'import.meta.env.PUBLIC_KLAVIYO_COMPANY': JSON.stringify(town.klaviyoCompany || 'X6vHTB'),
      'import.meta.env.PUBLIC_SIGNUP_SOURCE': JSON.stringify(`${town.brandName} site`),
    },
    build: {
      assetsInlineLimit: 0
    }
  }
});
