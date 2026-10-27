// San Fernando Valley content for storefront v2 ("shop by place"). Places here are the Valley's broader themes
// (collections); every history line is sourced, and sources are listed on each place page and in /about.
// Research and IP notes: claude/SFV_BUILD.md and claude/SFV_CANDIDATES.md (HQ project docs).
import { FREE_SHIP, HOLIDAY_CUTOFF, type Place, type Pair, type Faq, type TownContent, type Blank } from '../shared';
import productImages from './sfv-product-images.json';
import opaqueImages from './sfv-opaque-images.json';

const CSUN = 'https://digital-collections.csun.edu/digital/collection/SFVH/id/';

const PLACES: Place[] = [
  {
    slug: 'orchard-valley',
    name: 'The Orchard Valley',
    short: 'The Orchard Valley',
    era: '1880s–1920s',
    line: 'Ranchos, small farms and a cannery in Burbank.',
    story: [
      'Before the tract houses, the San Fernando Valley was sold by the acre. In 1887 the Lankershim Ranch Land and Water Co. advertised 12,000 acres in lots of 2½ to 40 acres, at $35 to $165 an acre.',
      'Around 1908 the Lankershim Development Company mailed a painted bird\'s-eye postcard of the Lankershim and Van Nuys Ranchos, looking in from the Pacific over the Santa Monica Mountains. A decade later Little Farms Magazine of Los Angeles sold the same dream as "A Little Land and a Living" in California.',
      'The McKeon Canning Company opened in Burbank in 1922 and packed the Valley\'s fruit under the Burbank Brand label.',
      'Our framed prints reproduce the postcards and the label. They are cleaned of dust and enlarged, never repainted.',
    ],
    facts: [
      { k: 'Lankershim ad', v: '1887' },
      { k: 'Ranchos postcard', v: 'c. 1908' },
      { k: 'Little Farms card', v: 'c. 1919' },
      { k: 'McKeon Canning, Burbank', v: 'from 1922' },
    ],
    sources: [
      { label: 'San Fernando Valley History Digital Library, CSUN Oviatt Library: Lankershim and Van Nuys Ranchos postcard, c. 1908 (West Valley Museum)', url: CSUN + '2320' },
      { label: 'Same library: "A Little Land and a Living" small-farm postcard, c. 1919 (West Valley Museum)', url: CSUN + '2354' },
      { label: 'Same library: Lankershim Ranch Land and Water Co. advertisement, 1887', url: CSUN + '2442' },
      { label: 'Same library: Burbank Brand peach can label, McKeon Canning Company, c. 1922 (Burbank Historical Society)', url: CSUN + '1721' },
    ],
    prefixes: ['lankershim-van-nuys-ranchos', 'a-little-land-and-a-living', 'burbank-brand'],
    tile: 'orchard-valley', tone: '#e9dfc8', ink: '#1e1a16',
    note: 'Not affiliated with any current business using the McKeon or Burbank names.',
  },
  {
    slug: 'greetings',
    name: 'Greetings from the Valley',
    short: 'Greetings from the Valley',
    era: '1950s',
    line: '“The fastest growing area of Los Angeles.”',
    story: [
      'In the 1950s the Valley sold itself on postcards: "Greetings from San Fernando Valley, Calif. The fastest growing area of Los Angeles," over an aerial view and a Studio City street scene.',
      'Our tee sets that banner copy in our own lettering, after the card in the San Fernando Valley History Digital Library at CSUN.',
    ],
    facts: [{ k: 'Card', v: '1950s greetings postcard' }, { k: 'Tagline', v: '“The fastest growing area of Los Angeles”' }],
    sources: [{ label: 'San Fernando Valley History Digital Library, CSUN Oviatt Library: "Greetings from San Fernando Valley" postcard, c. 1950–59 (reference for the lettering only)', url: CSUN + '2478' }],
    prefixes: ['greetings-from-san-fernando-valley'],
    tile: 'greetings', tone: '#f6f1e6', ink: '#1e1a16',
  },
  {
    slug: 'cruise-night',
    name: 'Cruise Night & the Raceway',
    short: 'Cruise Night & the Raceway',
    era: '1950s–70s',
    line: 'Wednesdays on Van Nuys Boulevard, weekends at “the Pond.”',
    story: [
      'Van Nuys Boulevard was a cruising strip from the 1950s on. Police cracked down from 1974, and still, by the late 1970s, the Wednesday-night cruise could draw tens of thousands of cars.',
      'San Fernando Raceway, known to racers as "the Pond," opened in 1955 on a triangle of land off Glenoaks Boulevard in San Fernando. It was one of the first purpose-built drag strips in the country and ran for 15 seasons, closing in late 1969. A swap meet fills the site today.',
      'Both designs are our own lockups.',
    ],
    facts: [
      { k: 'Cruise night', v: 'Wednesdays, Van Nuys Blvd.' },
      { k: 'San Fernando Raceway', v: '1955 to late 1969' },
      { k: 'Raceway site today', v: 'A swap meet' },
    ],
    sources: [
      { label: 'NHRA, "They left their hearts in San Fernando" (2008)', url: 'https://www.nhra.com/news/2008/they-left-their-hearts-san-fernando' },
      { label: 'Wikipedia: Cruising (driving), Van Nuys Boulevard', url: 'https://en.wikipedia.org/wiki/Cruising_(driving)' },
    ],
    prefixes: ['van-nuys-blvd-cruise-night', 'san-fernando-raceway'],
    tile: 'cruise-night', tone: '#14171c', ink: '#f4ecdd',
  },
  {
    slug: 'valley-music-theatre',
    name: 'Valley Music Theatre',
    short: 'Valley Music Theatre',
    era: '1964',
    line: 'Theater in the round under a dome in Woodland Hills.',
    story: [
      'The Valley Music Theatre opened on July 6, 1964, at 20600 Ventura Boulevard in Woodland Hills: a 2,865-seat theater in the round under a concrete dome, backed by Bob Hope and Art Linkletter.',
      'The Doors, the Byrds and Buffalo Springfield shared its stage on February 22, 1967. By the 1970s it had become an assembly hall, and it was torn down in 2007.',
      'Our dome is drawn fresh and the name is set in period lettering.',
    ],
    facts: [
      { k: 'Opened', v: 'July 6, 1964' },
      { k: 'Seats', v: '2,865, in the round' },
      { k: 'Torn down', v: '2007' },
    ],
    sources: [
      { label: 'Wikipedia: Valley Music Theater', url: 'https://en.wikipedia.org/wiki/Valley_Music_Theater' },
      { label: 'CSUN Special Collections & Archives: Valley Music Theatre', url: 'https://library.csun.edu/sca/peek-stacks/valley-music-theatre' },
    ],
    prefixes: ['valley-music-theatre'],
    tile: 'valley-music-theatre', tone: '#14171c', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using the name.',
  },
  {
    slug: 'phys-ed',
    name: 'Valley Phys. Ed.',
    short: 'Valley Phys. Ed.',
    line: 'Gym-class issue, one school color each.',
    story: [
      'Our own gym-class design, one town name and one school color per shirt: crimson for Van Nuys, gold for San Fernando.',
      'Van Nuys High opened in 1914; its student paper was the Crimson and Gray. San Fernando High dates to 1896 and wears black and gold.',
    ],
    facts: [{ k: 'Van Nuys', v: 'Crimson' }, { k: 'San Fernando', v: 'Gold' }],
    sources: [
      { label: 'Online Archive of California: Van Nuys High School records (the Crimson and Gray News)', url: 'https://www.oac.cdlib.org/findaid/ark:/13030/c8xs5x4p/admin/' },
      { label: 'MaxPreps: San Fernando High School (school colors)', url: 'https://www.maxpreps.com/ca/san-fernando/san-fernando-tigers' },
    ],
    prefixes: ['van-nuys-phys-ed', 'san-fernando-phys-ed'],
    tile: 'phys-ed', tone: '#f3ecdd', ink: '#1e1a16',
    note: 'Not affiliated with Van Nuys High School, San Fernando High School or the Los Angeles Unified School District.',
  },
];

// Colour of single-colour products (their Shopify variants carry only a size).
const SINGLE_COLOR: Record<string, string> = {
  'greetings-from-san-fernando-valley-tee': 'White',
  'greetings-from-san-fernando-valley-tee-black': 'Black',
  'valley-music-theatre-tee': 'Black',
  'van-nuys-blvd-cruise-night-tee': 'Black',
  'van-nuys-blvd-cruise-night-hat': 'Black',
  'san-fernando-raceway-tee': 'Vintage White',
  'san-fernando-phys-ed-tee': 'Black',
  'van-nuys-phys-ed-ringer-tee': 'Natural / Black',
};

function blankFor(handle: string): Blank | null {
  if (handle.includes('ringer')) return 'ringer';
  if (handle.endsWith('-hat') || handle.includes('framed-print')) return null;
  return 'mc1082';
}

const START_HERE = [
  'greetings-from-san-fernando-valley-tee',
  'lankershim-van-nuys-ranchos-postcard-framed-print',
  'van-nuys-blvd-cruise-night-tee',
  'valley-music-theatre-tee',
  'van-nuys-phys-ed-ringer-tee',
  'van-nuys-blvd-cruise-night-hat',
  'san-fernando-raceway-tee',
  'burbank-brand-peaches-label-framed-print',
];

const NOTE_BY_PREFIX: Record<string, string> = {
  'van-nuys-phys-ed': 'Not affiliated with Van Nuys High School or the Los Angeles Unified School District.',
  'san-fernando-phys-ed': 'Not affiliated with San Fernando High School or the Los Angeles Unified School District.',
};

// Gift pairs: tee + hat clears the free-shipping line ($34 + $32).
const PAIRS: Pair[] = [
  { title: 'Cruise Night', items: [{ h: 'van-nuys-blvd-cruise-night-tee' }, { h: 'van-nuys-blvd-cruise-night-hat' }], note: 'The tee and the hat for a Wednesday on the boulevard.' },
  { title: 'The Weekend', items: [{ h: 'san-fernando-raceway-tee' }, { h: 'van-nuys-blvd-cruise-night-hat' }], note: 'Saturday at the Pond, Wednesday on Van Nuys.' },
];

const FAMILIES: string[][] = [
  ['greetings-from-san-fernando-valley-tee', 'greetings-from-san-fernando-valley-tee-black'],
];
const MEMBER_LABEL: Record<string, string> = {};

const TITLE_OVERRIDE: Record<string, string> = {};
const FRAME_SIZE: Record<string, string> = {
  'lankershim-van-nuys-ranchos-postcard-framed-print': '16×12 in, black wood frame',
  'a-little-land-and-a-living-postcard-framed-print': '16×12 in, black wood frame',
  'burbank-brand-peaches-label-framed-print': '16×12 in, black wood frame',
};

const FAQ: Faq[] = [
  { q: 'Are you affiliated with these businesses?', a: 'No. Nostalgic San Fernando Valley is an independent tribute shop. We research each place from archives, old ads and photos, and restore or redraw the art ourselves. We are not affiliated with or endorsed by the businesses, schools or institutions shown.' },
  { q: 'How do the sizes run?', a: 'Our tees fit like a classic unisex tee. Each product page has a size chart with flat measurements; lay a favorite shirt flat and compare. Between sizes? Size up for a relaxed fit. Hats are one size with an adjustable strap.' },
  { q: 'When will my order arrive?', a: 'Everything is made to order. Most orders ship in 2–5 business days, then take 3–4 business days to reach most US addresses. For Christmas delivery, order by ' + HOLIDAY_CUTOFF + ' with standard shipping.' },
  { q: 'What if something is wrong with my order?', a: 'If your item arrives misprinted, damaged or wrong, email us a photo within 30 days of delivery and we will send a replacement or refund at no cost.' },
  { q: 'Can I return it if it doesn\'t fit?', a: 'Because each piece is printed just for you, we can\'t take back items for fit or a change of mind. Check the size chart first, and email us if you\'re unsure; we\'ll help you pick.' },
  { q: 'Do you ship outside the US?', a: 'Right now we ship within the United States only.' },
  { q: 'Is shipping free?', a: 'US shipping is free on orders of $' + FREE_SHIP + ' or more.' },
];

export const sfv: TownContent = {
  PLACES, FALLBACK_PLACE: null, HIDE_EMPTY_PLACES: true,
  HELD_PREFIXES: [], SINGLE_COLOR, TYPE_OVERRIDE: {}, blankFor,
  START_HERE, AUTO_START: true,
  NOTE_BY_PREFIX, DESC_OVERRIDE: {}, PAIRS, FAMILIES, MEMBER_LABEL, TITLE_OVERRIDE, FRAME_SIZE, FAQ,
  CATALOG_QUERY: "tag:'town:sfv'",
  includeTags: () => true,
  PRODUCT_IMAGES: productImages as Record<string, string>,
  OPAQUE_IMAGES: opaqueImages,
  DETAIL: [], DETAIL_DIR: '/images/sfv/detail',
  SOCK_FIX: [], SOCK_DIR: '/images/sfv/socks',
  STALE_IMAGE: null,
  PLACE_DIR: '/images/sfv/places',
  ADD_ONS: ['van-nuys-blvd-cruise-night-hat', 'van-nuys-blvd-cruise-night-tee', 'greetings-from-san-fernando-valley-tee', 'lankershim-van-nuys-ranchos-postcard-framed-print'],
  MATE_FALLBACK: { Tee: 'van-nuys-blvd-cruise-night-hat', Hat: 'van-nuys-blvd-cruise-night-tee', 'Framed print': 'greetings-from-san-fernando-valley-tee' },
  TYPE_IMG: { Tee: 'greetings-from-san-fernando-valley-tee', Hat: 'van-nuys-blvd-cruise-night-hat', 'Framed print': 'lankershim-van-nuys-ranchos-postcard-framed-print' },
  COPY: {
    homeTitle: 'San Fernando Valley tees, hats & prints from the places we remember',
    metaDescription: 'Tees, hats and framed prints from the San Fernando Valley we remember: Van Nuys cruise night, San Fernando Raceway, the Valley Music Theatre and the old orchard Valley, redrawn and restored from the record.',
    ogImage: '/images/sfv/og.jpg',
    placesDesc: 'The San Fernando Valley we remember, by theme: the orchard Valley, cruise night and the raceway, the Valley Music Theatre and more, each with its story, sources and collection.',
    shopDesc: 'Every Nostalgic San Fernando Valley tee, hat and framed print, by place and by type: Van Nuys cruise night, San Fernando Raceway, the Valley Music Theatre and more.',
    footerBlurb: 'Tees, hats and prints for the San Fernando Valley we remember, redrawn and restored from old postcards, labels, ads and signs. Made to order, one at a time.',
    footerLegalHtml: 'Nostalgic San Fernando Valley is an independent tribute shop, not affiliated with or endorsed by the businesses, schools or institutions shown. Archival images from the San Fernando Valley History Digital Library, CSUN Oviatt Library.',
    aboutDesc: 'How Nostalgic San Fernando Valley researches, restores and redraws the Valley we remember, and where every image comes from.',
    termsArtworkHtml: 'The designs on this site were researched, restored and redrawn by Nostalgic San Fernando Valley. Please don\'t copy or resell them. Archival postcards come from the San Fernando Valley History Digital Library at CSUN, which lists them as public domain.',
  },
};
