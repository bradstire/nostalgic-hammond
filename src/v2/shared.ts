// Storefront v2 constants and types shared by every town. Town content lives in src/v2/towns/<slug>.ts.

export const FREE_SHIP = 60;
export const HOLIDAY_CUTOFF = 'Dec 11'; // Printful 2026 holiday guide: US standard shipping, US-fulfilled apparel
// Printful: fulfillment 2–5 business days; US standard shipping 3–4 business days after fulfillment.
export const SHIP_MAKE = '2–5'; export const SHIP_TRANSIT = '3–4';

export type Place = {
  slug: string;
  name: string;          // display name
  short: string;         // tile label
  era?: string;          // optional: left off where no date is on the record
  line: string;          // one-line hook for tiles
  story: string[];       // paragraphs on the place page
  // Paragraphs (and their sources) shown only once a product with this handle prefix is in the store.
  storyIf?: { prefix: string; text: string; source?: { label: string; url?: string } }[];
  facts: { k: string; v: string }[];
  sources: { label: string; url?: string }[];
  prefixes: string[];    // product handle prefixes that belong here
  tile: string;          // <placeDir>/<tile>-(600|900).(webp|avif), -900.jpg for sharing
  tileTall?: boolean;    // place-page image is square (900×900) rather than 4:3
  tone: string;          // tile background
  ink: string;           // tile text colour
  note?: string;         // not-affiliated line, shown on place + product pages
  locality?: string;     // town the place was in, when it isn't the site's town (structured data)
  catchAll?: boolean;    // "Around <town>": not counted as a story in headings
};

// color pins a variant of a multi-colour product; label only names the colour of a single-colour product.
export type PairItem = { h: string; color?: string; label?: string };
export type Pair = { title: string; items: PairItem[]; note: string };
export type Faq = { q: string; a: string };

export const TYPE_LABEL: Record<string, string> = {
  'T-SHIRT': 'Tee', EMBROIDERY: 'Hat', SUBLIMATION: 'Socks', 'FRAMED-POSTER': 'Framed print',
};
export const TYPE_ORDER = ['Tee', 'Sweatshirt', 'Hat', 'Socks', 'Framed print'];
export const TYPE_SLUG: Record<string, string> = { Tee: 'tees', Sweatshirt: 'sweatshirts', Hat: 'hats', Socks: 'socks', 'Framed print': 'prints' };
// Plural label for filters and links ("Framed prints", "Socks").
export const typePlural = (t: string) => (t === 'Framed print' ? 'Framed prints' : t === 'Socks' ? 'Socks' : t + 's');
// "tees, hats, socks and prints" for the types a town actually stocks.
export function typePhrase(types: string[]): string {
  const w = TYPE_ORDER.filter((t) => types.includes(t)).map((t) => (t === 'Framed print' ? 'prints' : typePlural(t).toLowerCase()));
  return w.length > 1 ? `${w.slice(0, -1).join(', ')} and ${w[w.length - 1]}` : w.join('');
}
const NUM = ['No', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve'];
export const numWord = (n: number) => NUM[n] || String(n);

export const COLOR_HEX: Record<string, string> = {
  White: '#ffffff', 'Vintage White': '#f1e8d2', Black: '#151515', Maroon: '#6b1e2a', Navy: '#1f2a44',
  'Military Green': '#4b5a3a', Stone: '#cfc6b4', Khaki: '#b9a57e', Cranberry: '#9e2235',
  'Natural / Black': '#f1e8d2',
  Cream: '#f1e8d2', Forest: '#23402f', 'White / Black': '#ffffff',
};

// Size charts from Printful (flat measurements in inches). Towns map each tee to a blank.
export const SIZE_CHART = {
  mc1082: { name: 'Cotton Heritage MC1082 premium tee · 100% combed ring-spun cotton, 5.5 oz', sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL'], width: [18, 20, 22, 24, 26, 28], length: [28, 29, 30, 31, 32, 33] },
  ringer: { name: 'Unisex ringer tee · 100% combed ring-spun cotton, 4.3 oz', sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL'], width: [19, 20.5, 22, 24, 26, 28], length: [28, 29, 30, 31, 32, 33] },
  bc3001: { name: 'Bella+Canvas 3001 unisex tee · airlume cotton', sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL'], width: [18, 20, 22, 24, 26, 28], length: [28, 29, 30, 31, 32, 33] },
};
export type Blank = keyof typeof SIZE_CHART;

// Printful sock sizes (from the product spec).
export const SOCK_CHART = [
  { s: 'S', w: '6–8', m: '5–6.5' },
  { s: 'M', w: '8.5–11', m: '7–9.5' },
  { s: 'L', w: '11.5–13', m: '10–13' },
];

// Everything a town supplies to the v2 storefront.
export type TownContent = {
  PLACES: Place[];
  // A product that matches no place lands here (slug), or nowhere when null.
  FALLBACK_PLACE: string | null;
  // Places with no products are left out of grids, nav and routes.
  HIDE_EMPTY_PLACES: boolean;
  HELD_PREFIXES: string[];
  SINGLE_COLOR: Record<string, string>;
  TYPE_OVERRIDE: Record<string, string>;
  blankFor: (handle: string, imageUrl?: string) => Blank | null;  // size chart for a tee, or none
  START_HERE: string[];
  // Also add the first piece of any place the START_HERE list doesn't cover yet.
  AUTO_START: boolean;
  NOTE_BY_PREFIX: Record<string, string>;
  DESC_OVERRIDE: Record<string, string>;
  PAIRS: Pair[];
  FAMILIES: string[][];
  MEMBER_LABEL: Record<string, string>;
  TITLE_OVERRIDE: Record<string, string>;
  FRAME_SIZE: Record<string, string>;
  FAQ: Faq[];
  // Catalog selection: a Storefront search query, plus a tag filter applied in code.
  CATALOG_QUERY: string | null;
  includeTags: (tags: string[]) => boolean;
  PRODUCT_IMAGES: Record<string, string>;   // Shopify image basename -> local cut-out base path
  DETAIL: string[]; DETAIL_DIR: string;      // print close-ups: <DETAIL_DIR>/<handle>-(360|540|800).webp
  SOCK_FIX: string[]; SOCK_DIR: string;
  STALE_IMAGE: RegExp | null;
  PLACE_DIR: string;
  ADD_ONS: string[];                         // cart drawer: items offered to close the free-shipping gap
  MATE_FALLBACK: Record<string, string | null>;  // product page "complete the pair" defaults by type
  TYPE_IMG: Record<string, string>;          // home "shop by type" images
  COPY: {
    homeTitle: string;          // home page <title>, after "<brand>: "
    metaDescription: string;    // default meta description
    ogImage: string;            // default share image
    placesDesc: string;         // /places meta description
    shopDesc: string;           // /shop meta description
    footerBlurb: string;
    footerLegalHtml: string;    // raw HTML
    aboutDesc: string;          // /about meta description
    termsArtworkHtml: string;   // "Our artwork" paragraph on /terms (raw HTML)
  };
};
