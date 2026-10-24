// v2 catalog: one Storefront API call at build time, enriched with place, type and colours.
import { siteConfig, townSlug } from '../config/site.config';
import { PLACES, HELD_PREFIXES, TYPE_LABEL, COLOR_HEX, SINGLE_COLOR, FAMILIES, MEMBER_LABEL, TITLE_OVERRIDE, HIDDEN_FROM_GRID, DESC_OVERRIDE, TOWN, FALLBACK_PLACE, TYPE_OVERRIDE, PRODUCT_IMAGES, OPAQUE_IMAGES, type Place } from './data';

export type V2Variant = { id: string; numericId: string; title: string; available: boolean; price: number; options: Record<string, string>; image?: string };
// cut: a transparent cut-out (gets the .hb-cut drop-shadow); false for opaque photos (Printful's lifestyle view).
// color: the colour option a view shows on a multi-colour product; null = shared by every colour.
export type V2Image = { url: string; width: number; height: number; alt: string; cut: boolean; color: string | null };
export type FamilyOpt = { handle: string; color: string; hex: string; label: string; image?: string };
export type V2Product = {
  handle: string; title: string; baseTitle: string; shopifyTitle: string; description: string; descriptionHtml: string;
  family: FamilyOpt[];   // every colour of this design across sibling products (incl. this one)
  lead: boolean;         // shown in grids (false for sibling colourways)
  type: string; productType: string; place: Place | null;
  price: number; images: V2Image[]; detail: string | null;
  colors: { name: string; hex: string }[]; sizes: string[];
  variants: V2Variant[]; available: boolean; tags: string[];
};

// One Storefront API search per page of 250. Towns that select by tag in code (Hammond keeps untagged products)
// fetch the whole store and filter with TOWN.includeTags.
const Q = (after: string | null) => `{ products(first: 250${after ? `, after: "${after}"` : ''}${TOWN.CATALOG_QUERY ? `, query: ${JSON.stringify(TOWN.CATALOG_QUERY)}` : ''}) { pageInfo { hasNextPage endCursor } nodes {
  handle title productType description descriptionHtml tags availableForSale
  options { name optionValues { name } }
  priceRange { minVariantPrice { amount } }
  images(first: 30) { nodes { url width height altText } }
  variants(first: 60) { nodes { id title availableForSale price { amount } selectedOptions { name value } image { url } } }
} } }`;

let cache: V2Product[] | null = null;
const SIZE_ORDER = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'];

export function placeFor(handle: string): Place | null {
  return PLACES.find((p) => p.prefixes.some((pre) => handle.startsWith(pre)))
    || (FALLBACK_PLACE ? PLACES.find((p) => p.slug === FALLBACK_PLACE) || null : null);
}

// Second image for cards/galleries (print close-ups), upright sock renders and stale mockups: per town.
const DETAIL = new Set(TOWN.DETAIL);
const SOCK_FIX = new Set(TOWN.SOCK_FIX);
const STALE_IMAGE = TOWN.STALE_IMAGE;

export async function getCatalog(): Promise<V2Product[]> {
  if (cache) return cache;
  const nodes: any[] = [];
  let after: string | null = null;
  do {
    const res = await fetch(`https://${siteConfig.shopifyStoreDomain}/api/2025-01/graphql.json`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Shopify-Storefront-Access-Token': siteConfig.shopifyStorefrontToken },
      body: JSON.stringify({ query: Q(after) }),
    });
    const json = await res.json();
    if (!json.data) throw new Error('[v2 catalog] Storefront API error: ' + JSON.stringify(json.errors || json).slice(0, 400));
    nodes.push(...json.data.products.nodes);
    after = json.data.products.pageInfo.hasNextPage ? json.data.products.pageInfo.endCursor : null;
  } while (after);
  const out: V2Product[] = [];
  for (const n of nodes) {
    if (!TOWN.includeTags(n.tags || [])) continue;
    if (HELD_PREFIXES.some((p) => n.handle.startsWith(p))) continue;
    const variants: V2Variant[] = n.variants.nodes.map((v: any) => ({
      id: v.id, numericId: v.id.split('/').pop(), title: v.title, available: v.availableForSale,
      price: parseFloat(v.price.amount),
      options: Object.fromEntries(v.selectedOptions.map((o: any) => [o.name, o.value])),
      image: v.image?.url,
    }));
    const colorOpt = n.options.find((o: any) => o.name === 'Color');
    const sizeOpt = n.options.find((o: any) => o.name === 'Size');
    const colorNames: string[] = colorOpt ? colorOpt.optionValues.map((o: any) => o.name) : (SINGLE_COLOR[n.handle] ? [SINGLE_COLOR[n.handle]] : []);
    const type = TYPE_OVERRIDE[n.handle] || TYPE_LABEL[n.productType] || 'Other';
    const title = TITLE_OVERRIDE[n.handle] || n.title.replace(/\s+—\s+Framed Poster.*$/, ' Framed Print');
    const goodAlt = (a: string | null) => (a && !/mockup/i.test(a) ? a : null);
    const colorFor = imageColors(colorNames, variants);
    let images: V2Image[] = n.images.nodes.filter((im: any) => !STALE_IMAGE?.test(im.url)).map((im: any, i: number) => ({ url: im.url, width: im.width, height: im.height, alt: goodAlt(im.altText) || `${title}${i ? `, view ${i + 1}` : ''}`, cut: isCut(im.url), color: colorFor(im.url) }));
    // The first photo is the card image and sets the product page's default colour. Printful lists a multi-view
    // product colour by colour with the 3/4 view first (hats), so lead with the main colour's variant photo (its front).
    const leadColor = TOWN.MAIN_COLOR?.[n.handle] || images[0]?.color || null;
    const leadUrl = (variants.find((v) => v.image && (!leadColor || v.options.Color === leadColor)) || variants.find((v) => v.image))?.image?.split('?')[0];
    const lead = leadUrl ? images.findIndex((im) => im.url.split('?')[0] === leadUrl) : -1;
    if (lead > 0) images.unshift(...images.splice(lead, 1));
    if (SOCK_FIX.has(n.handle)) images = [{ url: `local:${TOWN.SOCK_DIR}/${n.handle}`, width: 1080, height: 1080, alt: `${title}, front and back`, cut: true, color: null }];
    out.push({
      handle: n.handle, title, baseTitle: title.replace(/\s*\((Black|Natural|Dark)\)$/, ''), shopifyTitle: n.title, family: [], lead: true,
      description: (DESC_OVERRIDE[n.handle] || n.description).replace(/Postcard from the 1910s/, 'Postcard from about 1915–20').replace(/(\d)—(\d)/g, '$1–$2'), descriptionHtml: n.descriptionHtml,
      type, productType: n.productType, place: placeFor(n.handle),
      price: parseFloat(n.priceRange.minVariantPrice.amount), images,
      detail: DETAIL.has(n.handle) ? `${TOWN.DETAIL_DIR}/${n.handle}` : null,
      colors: colorNames.map((c) => ({ name: c, hex: COLOR_HEX[c] || '#cccccc' })),
      sizes: sizeOpt ? sizeOpt.optionValues.map((o: any) => o.name).sort((a: string, b: string) => SIZE_ORDER.indexOf(a) - SIZE_ORDER.indexOf(b)) : [],
      variants, available: n.availableForSale, tags: n.tags,
    });
  }
  // colour families
  for (const fam of FAMILIES) {
    const members = fam.map((h) => out.find((p) => p.handle === h)).filter(Boolean) as V2Product[];
    if (members.length < 2) continue;
    const opts: FamilyOpt[] = members.flatMap((m) => (m.colors.length ? m.colors : [{ name: 'Default', hex: '#cccccc' }]).map((c) => ({
      handle: m.handle, color: c.name, hex: c.hex, label: MEMBER_LABEL[m.handle] || c.name,
      image: m.variants.find((v) => v.options.Color === c.name)?.image || m.images[0]?.url,
    })));
    const base = members[0].baseTitle.replace(/ Ringer Tee$/, ' Tee');
    members.forEach((m, i) => { m.family = opts; m.lead = i === 0; m.baseTitle = base; });
  }
  for (const p of out) if (HIDDEN_FROM_GRID.has(p.handle)) p.lead = false;
  cache = out;
  return out;
}

// Which colour each view shows, for multi-colour products (Printful publishes every view for every colour).
// Printful file names carry the colour slug ("...-tee-vintage-white-front-3-<id>.png"); the longest slug is tried
// first so "white" doesn't claim "vintage-white". A file name without a colour falls back to the variant that uses
// the image; anything else is shared by all colours.
const slugify = (s: string) => s.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
function imageColors(colorNames: string[], variants: V2Variant[]): (url: string) => string | null {
  if (colorNames.length < 2) return () => null;
  const slugs = colorNames.map((c) => ({ c, s: slugify(c) })).filter((x) => x.s).sort((a, b) => b.s.length - a.s.length);
  const byVariant = new Map<string, Set<string>>();
  for (const v of variants) if (v.image && v.options.Color) {
    const b = baseName(v.image);
    byVariant.set(b, (byVariant.get(b) || new Set()).add(v.options.Color));
  }
  return (url) => {
    const b = baseName(url);
    const padded = `-${b.toLowerCase()}-`;
    const hit = slugs.find((x) => padded.includes(`-${x.s}-`));
    if (hit) return hit.c;
    const vc = byVariant.get(b);
    return vc && vc.size === 1 ? [...vc][0] : null;
  };
}

// Shopify CDN resize (it negotiates WebP/AVIF from the Accept header).
const LOCAL_W = [360, 540, 800, 1080];
// Shopify mockups with the background knocked out (transparent WebP), keyed by the image's file name (per town).
const KNOCKOUT = PRODUCT_IMAGES;
const baseName = (url: string) => url.split('?')[0].split('/').pop()!.replace(/\.[a-z]+$/i, '');
export function localFor(url: string): string | null {
  if (url.startsWith('local:')) return url.slice(6);
  return KNOCKOUT[baseName(url)] || null;
}
// Opaque photos on Shopify (the lifestyle view has a studio background), by file name, per town; written by
// scripts/opaque_images.py. They don't get the cut-out drop-shadow. A local knock-out above is transparent, so it wins.
const OPAQUE = new Set<string>(OPAQUE_IMAGES);
export const isCut = (url: string) => !!localFor(url) || !OPAQUE.has(baseName(url));
export function cdn(url: string, w: number): string {
  const loc = localFor(url);
  if (loc) return `${loc}-${LOCAL_W.find((x) => x >= w) || 1080}.webp`;
  return url + (url.includes('?') ? '&' : '?') + 'width=' + w;
}
export function srcset(url: string, widths = [360, 540, 720, 1080]): string {
  const loc = localFor(url);
  if (loc) return LOCAL_W.map((w) => `${loc}-${w}.webp ${w}w`).join(', ');
  return widths.map((w) => `${cdn(url, w)} ${w}w`).join(', ');
}
export const absImg = (url: string) => { const loc = localFor(url); return loc ? `${loc}-1080.webp` : url; };
// Share/structured-data image: an opaque JPG on the site's tile colour. Shopify now holds transparent PNG mockups,
// and transparent images render on black or white unpredictably in link previews.
export const shareImg = (url: string) => { const loc = localFor(url); return loc ? `${loc}-og.jpg` : url + (url.includes('?') ? '&' : '?') + 'width=1200'; };
export function money(n: number): string {
  return '$' + (Number.isInteger(n) ? n.toFixed(0) : n.toFixed(2));
}
// Short description: the story paragraph before the garment spec bullets.
export function storyOf(p: V2Product): string[] {
  const text = p.description.split('•')[0].trim();
  return text.split(/\n\s*\n|(?<=\.)\s{2,}/).map((s) => s.trim()).filter(Boolean);
}
export function specsOf(p: V2Product): string[] {
  const parts = p.description.split('•').slice(1).map((s) => s.trim().replace(/\s+/g, ' ').replace(/\s*Disclaimer:.*$/i, '')).filter(Boolean);
  return parts.filter((s) => !/^Disclaimer/i.test(s) && !/Green Camo/i.test(s) && !/^\d sizes:/i.test(s));
}
