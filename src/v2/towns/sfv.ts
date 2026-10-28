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
    prefixes: ['van-nuys-blvd-cruise-night', 'san-fernando-raceway', 'june-ellens'],
    storyIf: [{ prefix: 'june-ellens', text: 'June Ellen\'s donuts was one of the turnarounds; the CSUN Daily Sundial wrote about "the June Ellen\'s side" of the boulevard in 1973.', source: { label: 'CSUN Daily Sundial, Nov. 6, 1973, p. 3', url: 'https://digital-collections.csun.edu/digital/collection/Sundial/id/16356' } }],
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
    slug: 'shopping',
    name: 'Valley Plaza & the Discount Stores',
    short: 'Valley Plaza & the Discount Stores',
    era: '1951–1986',
    line: 'The Plaza, GEMCO, Zodys and White Front.',
    story: [
      'Valley Plaza opened at Laurel Canyon and Victory in North Hollywood on August 12, 1951, and by the mid-1950s it was called the largest shopping center on the West Coast. It declined after the 1970s, and demolition began on October 29, 2025.',
      'Out on the boulevards the Valley shopped at the discount stores. White Front opened its ninth store at 21300 Roscoe in Canoga Park in May 1963; the chain closed in 1974. Zodys opened at 8201 Topanga Canyon on September 27, 1962, under five hexagon letter boxes, and its California stores closed in March 1986. GEMCO, the members-only department store and supermarket, closed all 80 of its stores that same year.',
      'The signs are redrawn from photos and the membership card, with the lettering re-set.',
    ],
    facts: [
      { k: 'Valley Plaza opened', v: 'Aug. 12, 1951' },
      { k: 'Zodys Canoga Park', v: 'Sept. 27, 1962' },
      { k: 'White Front Canoga Park', v: 'May 1963' },
      { k: 'GEMCO and Zodys closed', v: '1986' },
    ],
    sources: [
      { label: 'Wikipedia: Valley Plaza', url: 'https://en.wikipedia.org/wiki/Valley_Plaza' },
      { label: 'KTLA, "Demolition work underway at blighted Los Angeles mall" (Oct. 30, 2025)', url: 'https://ktla.com/news/local-news/demolition-work-underway-at-blighted-los-angeles-mall/' },
      { label: 'Wikipedia: White Front', url: 'https://en.wikipedia.org/wiki/White_Front' },
      { label: 'Wikipedia: Hartfield-Zodys', url: 'https://en.wikipedia.org/wiki/Hartfield-Zodys' },
      { label: 'Wikipedia: Gemco', url: 'https://en.wikipedia.org/wiki/Gemco' },
      { label: 'D. J. Waldie, "For the vanished discounters of suburban L.A.," PBS SoCal (2014)', url: 'https://www.pbssocal.org/commentary/for-the-vanished-discounters-of-suburban-l-a-retail-nostalgia' },
    ],
    prefixes: ['valley-plaza', 'gemco', 'zodys', 'white-front'],
    tile: 'shopping', tone: '#161a20', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using the Valley Plaza, GEMCO, Zodys or White Front names.',
  },
  {
    slug: 'coffee-shops',
    name: 'Coffee Shops & Supper Spots',
    short: 'Coffee Shops & Supper Spots',
    era: '1928–2003',
    line: 'Leon\'s, Phil\'s, Don\'s, Mike\'s and more.',
    story: [
      'Phil\'s Diner, a 1926 dining car called the oldest in California, opened beside the Lankershim depot in 1928 and is now a Los Angeles Historic-Cultural Monument. Leon Grown opened Leon\'s Steak House and Coffee Shop at Victory and Vineland in 1945; it closed in July 2003. Don\'s in Burbank started as a drive-in in 1947 and closed in 2002.',
      'Mike\'s Pizza in Panorama City was "serving since 1954" until 1993. The Jolly Roger served the Sherman Oaks Fashion Square under a linocut galleon, Rusty\'s Hacienda poured margaritas on Lankershim, and Encino Bowl kept a coffee shop next to the lanes from 1962 to 1986.',
      'Each design is redrawn from the place\'s own menu or sign, with the lettering re-set.',
    ],
    facts: [
      { k: 'Phil\'s Diner', v: 'from 1928' },
      { k: 'Leon\'s', v: '1945–2003' },
      { k: 'Don\'s, Burbank', v: '1947–2002' },
      { k: 'Encino Bowl', v: '1962–1986' },
    ],
    sources: [
      { label: 'Wikipedia: Phil\'s Diner', url: 'https://en.wikipedia.org/wiki/Phil%27s_Diner' },
      { label: 'Roadside Architecture: Don\'s Restaurant sign, Burbank', url: 'https://www.roadarch.com/signs/ca6.html' },
      { label: 'The Valley Observed: Gone But Not Forgotten (Leon\'s)', url: 'https://www.americassuburb.com/gone.html' },
      { label: 'Valley Relics Museum archive: The Jolly Roger menu (Gorsky Menu Collection)', url: 'https://valleyrelicsmuseum.org/archives/items/show/566' },
      { label: 'Los Angeles Public Library Menu Collection: Rusty\'s Hacienda take-out menu, c. 1965', url: 'https://tessa2.lapl.org/digital/collection/menus/id/3082' },
    ],
    prefixes: ['phils-diner', 'leons', 'dons-restaurant', 'mikes-pizza', 'the-jolly-roger', 'rustys-hacienda', 'encino-bowl'],
    tile: 'coffee-shops', tone: '#f3ecdd', ink: '#1e1a16',
    note: 'Not affiliated with any current business using these names.',
  },
  {
    slug: 'after-dark',
    name: 'After Dark',
    short: 'After Dark',
    era: '1960s–1990s',
    line: 'FM Station, Sasch, Weber\'s, the Sugar Shack and the Pass Club.',
    story: [
      'FM Station opened in North Hollywood in 1976 and was the Valley\'s hard-rock room until 1997; Poison, Warrant, Metallica and Great White played it. Weber\'s Place on Vanowen in Reseda was a dive bar with live music and punk shows. Sasch, on Ventura in Studio City, billed itself as "L.A.\'s most sophisticated nightclub."',
      'For the under-21 crowd there was the Sugar Shack, 12458 Magnolia at Whitsett, "L.A.\'s most popular teenage night club" in the 1970s: dancing, games, snacks and a light show. Up in the Santa Susana Pass, just over the county line, the Pass Club dealt cards under four suit panels.',
      'The signs, matchbook and coupon art are redrawn, with the lettering re-set.',
    ],
    facts: [
      { k: 'FM Station', v: '1976–1997' },
      { k: 'Sugar Shack', v: '1970s, 20 and under' },
      { k: 'Pass Club photo', v: 'Oct. 1963' },
    ],
    sources: [
      { label: 'WeHo Online, "Filthy McNasty, icon of the old Sunset Strip, has died" (2016): FM Station', url: 'https://wehoonline.com/2016/04/23/filthy-mcnasty-icon-of-the-old-sunset-strip-has-died/' },
      { label: 'Valley Relics Museum (Facebook): posts on FM Station, Weber\'s Place, Sasch, the Sugar Shack and the Pass Club' },
    ],
    prefixes: ['fm-station', 'webers-place', 'sasch', 'the-sugar-shack', 'the-pass-club'],
    tile: 'after-dark', tone: '#0e0e0e', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using these names.',
  },
  {
    slug: 'records-books',
    name: 'Records & Books',
    short: 'Records & Books',
    era: '1961–2006',
    line: 'Moby Disc and Dutton\'s.',
    story: [
      'Moby Disc Records grew from a store on Victory Boulevard in the early 1970s into a small chain, with stores at 14410 Ventura in Sherman Oaks and on Topanga Canyon in Canoga Park, and closed in 2001. Its sleeves carried a whale spouting a record: "A Whale of a Store!"',
      'Bill and Thelma Dutton opened Dutton\'s Books at Laurel Canyon and Magnolia in North Hollywood on New Year\'s Day 1961, selling books and art, "New-Old & Rare, Bought & Sold," as the rooftop sign said. The North Hollywood store closed in 2006.',
    ],
    facts: [{ k: 'Dutton\'s, North Hollywood', v: '1961–2006' }, { k: 'Moby Disc', v: 'early 1970s–2001' }],
    sources: [
      { label: 'Wikipedia: Dutton\'s Books', url: 'https://en.wikipedia.org/wiki/Dutton%27s_Books' },
      { label: 'Daily Bruin, "Moby Disc runs out on lease" (2002)', url: 'https://dailybruin.com/2002/02/11/moby-disc-runs-out-on-lease-ci' },
    ],
    prefixes: ['moby-disc', 'duttons-books'],
    tile: 'records-books', tone: '#a9dff6', ink: '#0f2a44',
    note: 'Not affiliated with any current business or publisher using the Moby Disc or Dutton names.',
  },
  {
    slug: 'devonshire-downs',
    name: 'Devonshire Downs',
    short: 'Devonshire Downs',
    era: '1946–2001',
    line: 'Harness racing, the Valley fair and the summer of 1967.',
    story: [
      'Devonshire Downs opened at 18000 Devonshire Street in Northridge as a harness track in 1946. The state bought it in 1948 for the San Fernando Valley Fair, and it later became part of San Fernando Valley State College, now CSUN. Racing ended in 1971 and most of the buildings came down in 2001.',
      'The grounds hosted car shows, horse shows and festivals, among them the Fantasy Faire and Magic Music Festival of July 15–16, 1967, and Newport \'69. A 1960s rental flyer called it "the San Fernando Valley\'s only complete fair grounds and exhibit facility!"',
    ],
    facts: [{ k: 'Harness track', v: '1946' }, { k: 'Fantasy Faire', v: 'July 15–16, 1967' }, { k: 'Mostly razed', v: '2001' }],
    sources: [
      { label: 'Wikipedia: Devonshire Downs', url: 'https://en.wikipedia.org/wiki/Devonshire_Downs' },
      { label: 'CSUN Special Collections & Archives: Devonshire Downs', url: 'https://library.csun.edu/sca/peek-stacks/devonshire-downs' },
    ],
    prefixes: ['devonshire-downs', 'fantasy-faire'],
    tile: 'devonshire-downs', tone: '#f3ecdd', ink: '#1e1a16',
    note: 'Not affiliated with CSUN or any current event or business using these names.',
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
  'fm-station-north-hollywood-tee': 'Black',
  'valley-plaza-sign-tee': 'Navy',
  'mikes-pizza-menu-tee': 'Vintage White',
  'gemco-membership-card-tee': 'White',
  'zodys-canoga-park-tee': 'Black',
  'white-front-canoga-park-tee': 'White',
  'the-jolly-roger-menu-tee': 'Vintage White',
  'moby-disc-records-tee': 'Ocean Blue',
  'leons-steak-house-sign-tee': 'Vintage White',
  'devonshire-downs-tee': 'Vintage White',
  'duttons-books-sign-tee': 'Vintage White',
  'the-pass-club-tee': 'Kelly Green',
  'phils-diner-tee': 'Pink',
  'webers-place-reseda-tee': 'Vintage Black',
  'sasch-studio-city-tee': 'Black',
  'encino-bowl-sign-tee': 'Navy',
  'the-sugar-shack-tee': 'Mustard',
  'rustys-hacienda-tee': 'Vintage White',
  'dons-restaurant-burbank-tee': 'Vintage White',
  'fantasy-faire-1967-tee': 'Yellow',
  'june-ellens-donuts-tee': 'Black',
};

const BC3001 = new Set(['moby-disc-records-tee', 'the-pass-club-tee', 'phils-diner-tee', 'the-sugar-shack-tee', 'fantasy-faire-1967-tee']);

function blankFor(handle: string): Blank | null {
  if (handle.includes('ringer')) return 'ringer';
  if (BC3001.has(handle)) return 'bc3001';
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
    metaDescription: 'Tees, hats and framed prints from the San Fernando Valley we remember: Valley Plaza, GEMCO and Zodys, Moby Disc, FM Station, Phil\'s Diner, Devonshire Downs and Van Nuys cruise night, redrawn and restored from the record.',
    ogImage: '/images/sfv/og.jpg',
    placesDesc: 'The San Fernando Valley we remember, by theme: Valley Plaza and the discount stores, coffee shops and supper spots, the clubs after dark, records and books, Devonshire Downs, cruise night and more, each with its story, sources and collection.',
    shopDesc: 'Every Nostalgic San Fernando Valley tee, hat and framed print, by place and by type: Valley Plaza, GEMCO, Zodys, Moby Disc, Dutton\'s, FM Station, Leon\'s, Phil\'s Diner, Devonshire Downs, Van Nuys cruise night and more.',
    footerBlurb: 'Tees, hats and prints for the San Fernando Valley we remember, redrawn and restored from old postcards, labels, ads and signs. Made to order, one at a time.',
    footerLegalHtml: 'Nostalgic San Fernando Valley is an independent tribute shop, not affiliated with or endorsed by the businesses, schools or institutions shown. Archival images from the San Fernando Valley History Digital Library, CSUN Oviatt Library.',
    aboutDesc: 'How Nostalgic San Fernando Valley researches, restores and redraws the Valley we remember, and where every image comes from.',
    termsArtworkHtml: 'The designs on this site were researched, restored and redrawn by Nostalgic San Fernando Valley. Please don\'t copy or resell them. Archival postcards come from the San Fernando Valley History Digital Library at CSUN, which lists them as public domain.',
  },
};
