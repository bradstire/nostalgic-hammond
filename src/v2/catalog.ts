// v2 catalog: one Storefront API call at build time, enriched with place, type and colours.
import { siteConfig, townSlug } from '../config/site.config';
import { PLACES, HELD_PREFIXES, TYPE_LABEL, COLOR_HEX, SINGLE_COLOR, FAMILIES, MEMBER_LABEL, TITLE_OVERRIDE, HIDDEN_FROM_GRID, DESC_OVERRIDE, type Place } from './data';

export type V2Variant = { id: string; numericId: string; title: string; available: boolean; price: number; options: Record<string, string>; image?: string };
export type V2Image = { url: string; width: number; height: number; alt: string };
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

const Q = `{ products(first: 250, query: "tag:'town:${townSlug}'") { nodes {
  handle title productType description descriptionHtml tags availableForSale
  options { name optionValues { name } }
  priceRange { minVariantPrice { amount } }
  images(first: 10) { nodes { url width height altText } }
  variants(first: 60) { nodes { id title availableForSale price { amount } selectedOptions { name value } image { url } } }
} } }`;

let cache: V2Product[] | null = null;
const SIZE_ORDER = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'];

export function placeFor(handle: string): Place | null {
  return PLACES.find((p) => p.prefixes.some((pre) => handle.startsWith(pre))) || null;
}

// Second image for cards/galleries: a close-up of the actual print art (generated from the print files).
// Sock mockups re-rendered upright (Printful shows the front sock toe-up).
const SOCK_FIX = new Set(['old-english-h-gym-socks', 'camelot-music-socks', 'hub-city-drag-raceway-socks', 'albert-speeds-socks']);
// Mockups left on a Shopify product after its print was repositioned (10-23); they show the old, too-high placement.
// Safe to delete from this list once the image is removed from the product in Shopify.
const STALE_IMAGE = /\/4e4a54369e0ab7a00dbff1761aa63849_l\./;

const DETAIL = new Set([
  'beverly-drive-in-theatre-tee', 'beverly-drive-in-theatre-tee-natural', 'hub-city-drag-raceway-tee',
  'camelot-music-1974-bag-tee', 'camelot-music-cloverleaf-sign-tee', 'camelot-music-cloverleaf-sign-tee-black',
  'camelot-music-tri-stripe-tee', 'culpepper-body-paint-tee', 'culpepper-body-paint-tee-black',
  'albert-speeds-restaurant-sign-tee', 'albert-speeds-restaurant-sign-tee-black', 'albert-speeds-pylon-tee',
  'mississippi-britches-tee', 'old-english-h-phys-ed-tee-black', 'old-english-h-hattiesburg-physical-education-tee-black',
  'old-english-h-pocket-tee', 'old-english-h-pocket-tee-black', 'old-english-h-phys-ed-ringer-tee',
  'old-english-h-hattiesburg-physical-education-ringer-tee', 'hub-city-drag-raceway-framed-poster-12-12',
  'main-street-hattiesburg-framed-poster-18-12', 'greetings-from-hattiesburg-framed-poster-12-18',
]);

export async function getCatalog(): Promise<V2Product[]> {
  if (cache) return cache;
  const res = await fetch(`https://${siteConfig.shopifyStoreDomain}/api/2025-01/graphql.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Shopify-Storefront-Access-Token': siteConfig.shopifyStorefrontToken },
    body: JSON.stringify({ query: Q }),
  });
  const json = await res.json();
  if (!json.data) throw new Error('[v2 catalog] Storefront API error: ' + JSON.stringify(json.errors || json).slice(0, 400));
  const out: V2Product[] = [];
  for (const n of json.data.products.nodes) {
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
    const type = TYPE_LABEL[n.productType] || 'Other';
    const title = TITLE_OVERRIDE[n.handle] || n.title.replace(/\s+—\s+Framed Poster.*$/, ' Framed Print');
    const goodAlt = (a: string | null) => (a && !/mockup/i.test(a) ? a : null);
    let images: V2Image[] = n.images.nodes.filter((im: any) => !STALE_IMAGE.test(im.url)).map((im: any, i: number) => ({ url: im.url, width: im.width, height: im.height, alt: goodAlt(im.altText) || `${title}${i ? `, view ${i + 1}` : ''}` }));
    if (SOCK_FIX.has(n.handle)) images = [{ url: `local:/images/hb/socks/${n.handle}`, width: 1080, height: 1080, alt: `${title}, front and back` }];
    out.push({
      handle: n.handle, title, baseTitle: title.replace(/\s*\((Black|Natural|Dark)\)$/, ''), shopifyTitle: n.title, family: [], lead: true,
      description: (DESC_OVERRIDE[n.handle] || n.description).replace(/Postcard from the 1910s/, 'Postcard from about 1915–20').replace(/(\d)—(\d)/g, '$1–$2'), descriptionHtml: n.descriptionHtml,
      type, productType: n.productType, place: placeFor(n.handle),
      price: parseFloat(n.priceRange.minVariantPrice.amount), images,
      detail: DETAIL.has(n.handle) ? `/images/hb/detail/${n.handle}` : null,
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

// Shopify CDN resize (it negotiates WebP/AVIF from the Accept header).
const LOCAL_W = [360, 540, 800, 1080];
// Shopify mockups with the background knocked out (transparent WebP), keyed by the image's file name.
import productImages from './product-images.json';
const KNOCKOUT = productImages as Record<string, string>;
export function localFor(url: string): string | null {
  if (url.startsWith('local:')) return url.slice(6);
  const base = url.split('?')[0].split('/').pop()!.replace(/\.[a-z]+$/i, '');
  return KNOCKOUT[base] || null;
}
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
