import type { APIRoute } from 'astro';
import { town } from '../../config/site.config';
import { getCatalog, shareImg, storyOf, type V2Product, type V2Variant } from '../../v2/catalog';
import { HIDDEN_FROM_GRID } from '../../v2/data';

// Google Merchant Center product feed (RSS 2.0 + g: namespace), one item per variant.
// Links point at this town's own site, not the Shopify storefront (which is password-protected).
// Merchant Center fetches it on a schedule: <siteUrl>/feeds/google.xml
// Shipping per item mirrors the store's Printful flat rates (US): free at $60+.

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const abs = (u: string) => (u.startsWith('http') ? u : town.siteUrl + (u.startsWith('/') ? u : '/' + u));

// Google product taxonomy IDs.
function category(p: V2Product): { id: number; apparel: boolean } {
  const t = `${p.type} ${p.productType} ${p.title}`.toLowerCase();
  if (/\b(framed )?(print|poster|postcard)s?\b/.test(t)) return { id: 500044, apparel: false }; // Decor > Artwork > Posters, Prints & Visual Artwork
  if (/\bsocks?\b/.test(t)) return { id: 209, apparel: true };                    // Clothing > Underwear & Socks > Socks
  if (/\bhats?\b|\bcaps?\b/.test(t)) return { id: 173, apparel: true };          // Clothing Accessories > Hats
  if (/sweatshirt|hoodie|crew neck/.test(t)) return { id: 5388, apparel: true };     // Clothing > Activewear > Sweatshirts
  return { id: 212, apparel: true };                                      // Clothing > Shirts & Tops
}

// US flat rates from the Shopify shipping profiles (Printful), 10-26.
function shipRate(p: V2Product, v: V2Variant, cat: { id: number }): number {
  if (v.price >= 60) return 0;
  if (cat.id === 500044) return /16\D*20|medium/i.test(`${v.title} ${p.title}`) ? 14.49 : 10.89;
  if (cat.id === 5388) return 8.79;
  if (cat.id === 173 || cat.id === 209) return 4.69;
  return 4.95;
}

function itemXml(p: V2Product, v: V2Variant): string {
  const cat = category(p);
  const color = v.options.Color || p.colors[0]?.name;
  const size = v.options.Size;
  const q = new URLSearchParams();
  if (v.options.Color) q.set('color', v.options.Color);
  if (size) q.set('size', size);
  const link = abs(`/products/${p.handle}${q.toString() ? '?' + q : ''}`);
  // Locally fixed renders (e.g. upright socks) beat Printful's per-variant mockup.
  const fixed = p.images[0]?.url.startsWith('local:');
  const img = !fixed && v.image ? shareImg(v.image) : p.images[0] ? shareImg(p.images[0].url) : null;
  const extra = p.images.slice(1, 6).map((im) => abs(shareImg(im.url))).filter((u) => u !== (img && abs(img)));
  const desc = (storyOf(p).join(' ') || p.description).replace(/\s+/g, ' ').trim().slice(0, 4900);
  const title = `${p.baseTitle}${color && p.colors.length > 1 ? ` – ${color}` : ''}${size ? ` – ${size}` : ''}`.slice(0, 150);
  const lines = [
    `<g:id>${esc(v.numericId)}</g:id>`,
    `<g:item_group_id>${esc(p.handle)}</g:item_group_id>`,
    `<g:title>${esc(title)}</g:title>`,
    `<g:description>${esc(desc)}</g:description>`,
    `<g:link>${esc(link)}</g:link>`,
    img ? `<g:image_link>${esc(abs(img))}</g:image_link>` : '',
    ...extra.map((u) => `<g:additional_image_link>${esc(u)}</g:additional_image_link>`),
    `<g:availability>${v.available ? 'in_stock' : 'out_of_stock'}</g:availability>`,
    `<g:price>${v.price.toFixed(2)} USD</g:price>`,
    `<g:brand>${esc(town.brandName)}</g:brand>`,
    `<g:condition>new</g:condition>`,
    `<g:identifier_exists>no</g:identifier_exists>`,
    `<g:google_product_category>${cat.id}</g:google_product_category>`,
    `<g:product_type>${esc(`${p.type}${p.place ? ' > ' + p.place.name.replace(/ /g, ' ') : ''}`)}</g:product_type>`,
    color ? `<g:color>${esc(color)}</g:color>` : '',
    size ? `<g:size>${esc(size)}</g:size>` : '',
    cat.apparel ? `<g:gender>unisex</g:gender>` : '',
    cat.apparel ? `<g:age_group>adult</g:age_group>` : '',
    `<g:shipping><g:country>US</g:country><g:price>${shipRate(p, v, cat).toFixed(2)} USD</g:price></g:shipping>`,
  ].filter(Boolean);
  return `<item>\n  ${lines.join('\n  ')}\n</item>`;
}

// Held from the feed: products that quote other companies' marks (Merchant Center misrepresentation/trademark risk).
// Hub City's "FORD vs. CHEVY!" is an open call for Brad; drop this filter's match once that's resolved.
const FEED_HOLD = /\b(ford|chevy|chevrolet)\b/i;

export const GET: APIRoute = async () => {
  const catalog = await getCatalog();
  const items = catalog
    .filter((p) => !HIDDEN_FROM_GRID.has(p.handle) && p.available && !FEED_HOLD.test(`${p.title} ${p.description}`))
    .flatMap((p) => p.variants.map((v) => itemXml(p, v)));
  const body = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
<channel>
<title>${esc(town.brandName)}</title>
<link>${esc(town.siteUrl)}</link>
<description>${esc(town.brandName)} product feed</description>
${items.join('\n')}
</channel>
</rss>
`;
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
