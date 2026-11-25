// Hattiesburg content for storefront v2 ("shop by place"). Moved verbatim from src/v2/data.ts.
// Every history line here is sourced; sources are listed on each place page and in /about.
import { FREE_SHIP, HOLIDAY_CUTOFF, type Place, type Pair, type Faq, type TownContent, type Blank } from '../shared';
import productImages from '../product-images.json';
import opaqueImages from '../opaque-images.json';

const PLACES: Place[] = [
  {
    slug: 'beverly-drive-in',
    name: 'Beverly Drive-In Theatre',
    short: 'Beverly Drive-In',
    era: '1948–2005',
    line: 'Double features under the pines on Highway 49.',
    story: [
      'The Beverly Drive-In Theatre opened on May\u00a029, 1948, and ran until 1987. It reopened in 2001; Hurricane Katrina badly damaged it in 2005 and it never recovered.',
      'The Beverly was listed on the National Register of Historic Places in 2008. A fire destroyed what was left in 2010, and the site is now the Village at the Beverly apartments.',
      'Our lettering is redrawn from the theatre\'s marquee script.',
    ],
    facts: [
      { k: 'Opened', v: 'May 29, 1948' },
      { k: 'National Register', v: '2008' },
      { k: 'Today', v: 'Village at the Beverly apartments' },
    ],
    sources: [
      { label: 'Wikipedia: Beverly Drive-In Theatre', url: 'https://en.wikipedia.org/wiki/Beverly_Drive-In_Theatre' },
      { label: 'Mississippi Dept. of Archives and History, historic resources database' },
      { label: 'National Park Service, National Register record 08000761 (5320 U.S. Hwy 49 S.)', url: 'https://npgallery.nps.gov/AssetDetail/NRIS/08000761' },
      { label: 'MultifamilyBiz, May 25, 2016: the Village at the Beverly apartments open on the site', url: 'https://www.multifamilybiz.com/news/6946/site_of_former_drivein_theater_becomes_apartment_c' },
    ],
    prefixes: ['beverly-drive-in'],
    tile: 'beverly-drive-in', tileTall: true, tone: '#14171c', ink: '#f4ecdd',
  },
  {
    slug: 'cloverleaf-mall',
    name: 'Cloverleaf Mall',
    short: 'Cloverleaf Mall',
    era: 'Opened 1974',
    line: 'Records at Camelot, jeans at Britches.',
    story: [
      'Camelot Music opened at Cloverleaf Mall in 1974 and appears in the mall\'s grand-opening tenant list. Our Camelot pieces follow the 1974 storefront sign and the chain\'s 1970s paper bag, with its red-and-blue rainbow arch.',
      'Mississippi Britches was the mall\'s jeans and clothing store. Its logotype is redrawn from the store\'s 1987 newspaper ad.',
    ],
    facts: [
      { k: 'Camelot Music opened', v: '1974' },
      { k: 'Camelot address, 1995', v: '999 Broadway (Cloverleaf Mall)' },
      { k: 'Britches ad', v: '1987' },
    ],
    sources: [
      { label: 'Cloverleaf Mall grand-opening ad, Hattiesburg American, Aug. 27, 1974, p. 25 (Camelot Music in the tenant list)' },
      { label: 'Camelot Music corporate store list, Mar. 15, 1995: store #38, Cloverleaf Mall, 999 Broadway' },
      { label: 'Mississippi Britches newspaper ad, 1987 (clipping)' },
      { label: 'Mississippi Secretary of State, bicentennial timeline: Cloverleaf Mall opened in 1974', url: 'https://sos.ms.gov/PTV/Bicentennial/inc/html/197.html' },
    ],
    prefixes: ['camelot-music', 'mississippi-britches'],
    tile: 'cloverleaf-mall', tone: '#f6f1e6', ink: '#1e1a16',
    note: 'Not affiliated with any current owner of the Camelot Music or Mississippi Britches names.',
  },
  {
    slug: 'hub-city-drag-raceway',
    name: 'Hub City Drag Raceway',
    short: 'Hub City Drag Raceway',
    era: '1960s',
    line: '“FORD vs. CHEVY!” three miles north on I-59.',
    story: [
      'Hub City Drag Raceway sat three miles north of town on I-59 at the Eatonville exit. Our design is restored from its 1966 newspaper ad, which promised “FORD vs. CHEVY!”',
      'We kept the newsprint grain on purpose. It is part of the look.',
      'Hattiesburg has been called the Hub City since a 1912 newspaper contest, a name earned from the railroads that met here.',
    ],
    facts: [
      { k: 'Location', v: 'I-59 at the Eatonville exit' },
      { k: 'Ad restored from', v: '1966' },
    ],
    sources: [
      { label: 'Newspaper ad for the Sunday, May 22, 1966 match races (clipping)' },
      { label: 'Wikipedia: Hattiesburg, Mississippi (the Hub City nickname, 1912)', url: 'https://en.wikipedia.org/wiki/Hattiesburg,_Mississippi' },
    ],
    prefixes: ['hub-city-drag-raceway'],
    tile: 'hub-city-drag-raceway', tone: '#ece2cb', ink: '#1e1a16',
  },
  {
    slug: 'albert-speeds',
    name: 'Albert Speed\'s Restaurant',
    short: 'Albert Speed\'s',
    era: '1960s',
    line: 'Fresh seafood and steaks on U.S. 11.',
    story: [
      'Albert Speed\'s Restaurant stood at 304 Broadway Drive on U.S. 11, serving fresh seafood and steaks. The building later housed Chez Paul, then Austin\'s, and has since been torn down.',
      'The sign on our tees follows a 1966 postcard photograph: cream block capitals on brick-red panels, and the tall roadside pylon.',
    ],
    facts: [
      { k: 'Address', v: '304 Broadway Dr. (U.S. 11)' },
      { k: 'Sign redrawn from', v: '1966 postcard' },
    ],
    sources: [
      { label: 'Postcard photograph of the restaurant and its sign, 1966' },
      { label: 'Later history of the site: Hattiesburg Memory, a local-history community' },
      { label: 'Sam Miller, Hattiesburg repeat-photography project: Albert Speed\'s Restaurant, 304 Broadway Drive (Highway 11)', url: 'https://motosambo.wordpress.com/' },
    ],
    prefixes: ['albert-speeds'],
    tile: 'albert-speeds', tone: '#efe5cf', ink: '#1e1a16',
  },
  {
    slug: 'culpepper-body-paint',
    name: 'Culpepper Body & Paint Shop',
    short: 'Culpepper Body & Paint',
    era: '1960s',
    line: '“The king of body & paint work.”',
    story: [
      'Culpepper Body & Paint Shop billed itself as “the king of body & paint work.” The duck with the spray gun comes from the shop\'s 1968 newspaper ad.',
      'We redrew the duck\'s face on the original 1968 outline so it prints cleanly at full size.',
    ],
    facts: [{ k: 'Address', v: '113 N. Tipton St.' }, { k: 'Ad restored from', v: '1968' }],
    sources: [{ label: 'Culpepper Body & Paint Shop newspaper ad, 1968 (clipping)' }],
    prefixes: ['culpepper-body-paint'],
    tile: 'culpepper-body-paint', tone: '#f6f1e6', ink: '#1e1a16',
  },
  {
    slug: 'phys-ed',
    name: 'The Old English H',
    short: 'The Old English H',
    era: '1980s',
    line: 'Purple and gold, gym-class issue.',
    story: [
      'Our Old English H is drawn after the letter on Hattiesburg\'s 1983 basketball jerseys, set in purple and gold.',
      'The Phys. Ed. ringer is our own gym-class design.',
    ],
    facts: [{ k: 'Letter after', v: '1983 jerseys' }],
    sources: [{ label: '1983 Hattiesburg basketball team photograph (letter reference only)' }],
    prefixes: ['old-english-h', 'hattiesburg-phys-ed'],
    tile: 'phys-ed', tone: '#f3ecdd', ink: '#1e1a16',
    note: 'Not affiliated with Hattiesburg High School or the Hattiesburg Public School District.',
  },
  {
    slug: 'postcards',
    name: 'Hattiesburg Postcards',
    short: 'Hattiesburg Postcards',
    era: '1900s–1920s',
    line: 'Main Street and the Hub City, from the postcard rack.',
    story: [
      'Our framed prints come from early-1900s postcards in the Cooper Postcard Collection at the Mississippi Department of Archives and History, which states that the collection\'s postcards are in the public domain.',
      'We cleaned up dust and foxing and left the original color and paper alone.',
    ],
    facts: [
      { k: 'Collection', v: 'MDAH Cooper Postcard Collection' },
      { k: 'Main Street card', v: '1910s (archive date: 19xx)' },
    ],
    sources: [
      { label: 'MDAH Cooper Postcard Collection, PI/1992.0001 (system IDs 90128, 90199)', url: 'https://www.flickr.com/people/mississippi-dept-of-archives-and-history/' },
      { label: 'MDAH record: Main Street, Hattiesburg, Miss. (item 1468)', url: 'https://da.mdah.ms.gov/series/cooper/detail/16985' },
      { label: 'MDAH record: Greetings from Hattiesburg, Miss. (item 1445)', url: 'https://da.mdah.ms.gov/series/cooper/detail/17978' },
      { label: 'MDAH, Cooper Postcard Collection: rights statement', url: 'https://da.mdah.ms.gov/series/cooper/gentech' },
    ],
    prefixes: ['greetings-from-hattiesburg', 'main-street-hattiesburg'],
    tile: 'postcards', tone: '#e9dfc8', ink: '#1e1a16',
  },
];

// One page per business inside a shared place (/places/<slug>). Products keep their place (Cloverleaf Mall).
const NAMES: Place[] = [
  {
    slug: 'camelot-music',
    name: 'Camelot Music',
    short: 'Camelot Music',
    era: 'From 1974',
    line: 'Records, tapes and the rainbow bag at Cloverleaf Mall.',
    story: [
      'Camelot Music opened at Cloverleaf Mall in 1974 and appears in the mall\'s grand-opening tenant list. A 1995 company store list still carried it as store #38, at 999 Broadway.',
      'The chain began in Ohio in 1956, when Paul David started a service that stocked record racks in other people\'s stores. The first shop under the Camelot Music name opened in 1965, and by May 1998 the company ran 455 stores in 37 states. Trans World Entertainment bought it later that year and went on to rename its mall stores FYE.',
      'People who shopped the Cloverleaf store remember the $2 cut-out bin, and paying for tapes with paper-route money.',
      'Our Camelot pieces follow the 1974 storefront sign and the chain\'s 1970s paper bag, with its red-and-blue rainbow arch.',
    ],
    facts: [
      { k: 'Opened at Cloverleaf Mall', v: '1974' },
      { k: 'Store number', v: '#38' },
      { k: 'Chain founded', v: '1956, Ohio' },
    ],
    sources: [
      { label: 'Cloverleaf Mall grand-opening ad, Hattiesburg American, Aug. 27, 1974, p. 25 (Camelot Music in the tenant list)' },
      { label: 'Camelot Music corporate store list, Mar. 15, 1995: store #38, Cloverleaf Mall, 999 Broadway' },
      { label: 'Wikipedia: Camelot Music', url: 'https://en.wikipedia.org/wiki/Camelot_Music' },
      { label: 'Memories shared by people who shopped there (Hattiesburg local-history group, Nov. 2026)' },
    ],
    prefixes: ['camelot-music'],
    parent: 'cloverleaf-mall',
    tile: 'camelot-music', tone: '#f6f1e6', ink: '#1e1a16',
    note: 'Not affiliated with any current owner of the Camelot Music name.',
  },
  {
    slug: 'mississippi-britches',
    name: 'Mississippi Britches',
    short: 'Mississippi Britches',
    era: 'Advertised 1987',
    line: 'The jeans store at Cloverleaf Mall.',
    story: [
      'Mississippi Britches was the jeans and clothing store at Cloverleaf Mall, the shopping center at 999 Broadway that held its grand opening in August 1974.',
      'The record we have is thin: the store\'s 1987 newspaper ad, which set the name in plain lowercase letters. We have not found the year it opened or the year it closed.',
      'If you shopped or worked there, tell us what you remember. What can be confirmed gets added to this page.',
      'Our tee carries that lowercase logotype, redrawn from the ad, over the line "Cloverleaf Mall · Hattiesburg, Miss." The hat has the name embroidered in white.',
    ],
    facts: [
      { k: 'Where', v: 'Cloverleaf Mall, 999 Broadway' },
      { k: 'Sold', v: 'Jeans and clothing' },
      { k: 'Ad we drew from', v: '1987' },
    ],
    sources: [
      { label: 'Mississippi Britches newspaper ad, 1987 (clipping)' },
      { label: 'Cloverleaf Mall grand-opening ad, Hattiesburg American, Aug. 27, 1974, p. 25' },
    ],
    prefixes: ['mississippi-britches'],
    parent: 'cloverleaf-mall',
    tile: 'mississippi-britches', tone: '#262b45', ink: '#f4ecdd',
    note: 'Not affiliated with Mississippi Britches or any current owner of its name.',
  },
];


// Held from the storefront pending an owner decision (live business with a related name).
const HELD_PREFIXES = ['sacks-army-store'];

// Colour of single-colour products (their Shopify variants carry only a size).
const SINGLE_COLOR: Record<string, string> = {
  'beverly-drive-in-theatre-tee': 'Black',
  'beverly-drive-in-theatre-tee-natural': 'Vintage White',
  'hub-city-drag-raceway-tee': 'White',
  'camelot-music-1974-bag-tee': 'White',
  'camelot-music-cloverleaf-sign-tee': 'White',
  'camelot-music-cloverleaf-sign-tee-black': 'Black',
  'camelot-music-tri-stripe-tee': 'White',
  'culpepper-body-paint-tee-black': 'Black',
  'albert-speeds-restaurant-sign-tee-black': 'Black',
  'albert-speeds-pylon-tee': 'Vintage White',
  'old-english-h-phys-ed-tee-black': 'Black',
  'old-english-h-hattiesburg-physical-education-tee-black': 'Black',
  'old-english-h-pocket-tee': 'White',
  'old-english-h-pocket-tee-black': 'Black',
  'old-english-h-phys-ed-ringer-tee': 'Natural / Black',
  'old-english-h-hattiesburg-physical-education-ringer-tee': 'Natural / Black',
  'hattiesburg-phys-ed-ringer-tee': 'Natural / Black',
  'old-english-h-hat-black': 'Black',
};

// Which blank each tee uses (size charts from Printful; flat measurements in inches).
function blankFor(handle: string): Blank | null {
  if (handle.includes('ringer')) return 'ringer';
  if (handle === 'mississippi-britches-tee' || handle === 'sacks-army-store-tee') return 'bc3001';
  return 'mc1082';
}

// Homepage "Start here" picks, in order (one per story, mixed product types).
const START_HERE = [
  'beverly-drive-in-theatre-tee',
  'camelot-music-1974-bag-tee',
  'old-english-h-phys-ed-ringer-tee',
  'main-street-hattiesburg-framed-poster-18-12',
  'hub-city-drag-raceway-tee',
  'camelot-music-hat',
  'albert-speeds-restaurant-sign-tee-black',
  'culpepper-body-paint-tee',
];
// Not-affiliated line for a product, when it differs from its place's line.
const NOTE_BY_PREFIX: Record<string, string> = {
  'camelot-music': 'Not affiliated with any current owner of the Camelot Music name.',
  'mississippi-britches': 'Not affiliated with Mississippi Britches or any current owner of its name.',
};
// Site copy where the store description needs a correction.
const DESC_OVERRIDE: Record<string, string> = {
  'hattiesburg-phys-ed-ringer-tee': 'Our own gym-class design: HATTIESBURG arched over a blank name banner and PHYSICAL ED., in purple on a natural ringer with black trim. • 100% combed ring-spun cotton • Contrast ringer collar and sleeve cuffs',
  'greetings-from-hattiesburg-framed-poster-12-18': 'A "Greetings from Hattiesburg, Miss." postcard from the early 1900s: a portrait and five scenes of the town\'s industries (lumber, cotton, a cement-block factory and truck farms) set in the petals of a pansy. From the Cooper Postcard Collection, Mississippi Department of Archives and History. Printed on thick enhanced-matte paper in a black wood frame, 12×18 in.',
};

// Gift pairs: a tee + a hat, each pair clears the free-shipping line ($34 + $32).
// `color` pins the variant that is pictured, so what you see is what goes in the cart.
const PAIRS: Pair[] = [
  { title: 'The Weekend', items: [{ h: 'beverly-drive-in-theatre-tee' }, { h: 'hub-city-drag-raceway-hat', color: 'Stone' }], note: 'A night at the Beverly, then Sunday at the drag strip.' },
  { title: 'The Mall Rat', items: [{ h: 'camelot-music-1974-bag-tee' }, { h: 'camelot-music-hat', color: 'White' }], note: 'Saturday at Cloverleaf Mall, record bag in hand.' },
  { title: 'The Supper Club', items: [{ h: 'albert-speeds-restaurant-sign-tee', color: 'White' }, { h: 'albert-speeds-hat', color: 'Stone' }], note: 'Seafood, steaks and a sign you could see from U.S. 11.' },
];

// Same design in other colours lives in separate Shopify products. On the site they are one
// "family": one card in grids, linked colour swatches on the product page. First handle leads.
const FAMILIES: string[][] = [
  ['beverly-drive-in-theatre-tee', 'beverly-drive-in-theatre-tee-natural'],
  // Black leads these two so their cards differ from the white/natural tee beside them (Brad 10-24).
  ['camelot-music-cloverleaf-sign-tee-black', 'camelot-music-cloverleaf-sign-tee'],
  ['culpepper-body-paint-tee', 'culpepper-body-paint-tee-black'],
  ['albert-speeds-restaurant-sign-tee-black', 'albert-speeds-restaurant-sign-tee'],
  ['old-english-h-pocket-tee', 'old-english-h-pocket-tee-black'],
  ['camelot-music-hat', 'camelot-music-hat-dark'],
  ['old-english-h-hat', 'old-english-h-hat-black'],
  ['old-english-h-phys-ed-ringer-tee', 'old-english-h-phys-ed-tee-black'],
  ['old-english-h-hattiesburg-physical-education-ringer-tee', 'old-english-h-hattiesburg-physical-education-tee-black'],
];
// Option label for a family member when its colour alone doesn't describe it.
const MEMBER_LABEL: Record<string, string> = {
  'old-english-h-phys-ed-ringer-tee': 'Ringer', 'old-english-h-phys-ed-tee-black': 'Black tee',
  'old-english-h-hattiesburg-physical-education-ringer-tee': 'Ringer', 'old-english-h-hattiesburg-physical-education-tee-black': 'Black tee',
};

// Display names (Shopify titles carry the frame size and colour; the site shows those as options).
const TITLE_OVERRIDE: Record<string, string> = {
  'greetings-from-hattiesburg-framed-poster-12-18': 'Pansy “Greetings from Hattiesburg” Postcard Framed Print',
  'camelot-music-1974-bag-tee': 'Camelot Music Rainbow Bag Tee',
  'main-street-hattiesburg-framed-poster-18-12': 'Main Street Postcard Framed Print',
  'hub-city-drag-raceway-framed-poster-12-12': 'Hub City Drag Raceway Framed Print',
  'hattiesburg-phys-ed-ringer-tee': 'Hattiesburg Phys. Ed. Ringer Tee',
  'old-english-h-hattiesburg-physical-education-ringer-tee': 'Old English H Physical Education Ringer Tee',
  'old-english-h-hattiesburg-physical-education-tee-black': 'Old English H Physical Education Tee (Black)',
};
const FRAME_SIZE: Record<string, string> = {
  'greetings-from-hattiesburg-framed-poster-12-18': '12×18 in, black wood frame',
  'main-street-hattiesburg-framed-poster-18-12': '18×12 in, black wood frame',
  'hub-city-drag-raceway-framed-poster-12-12': '12×12 in, black wood frame',
};

const FAQ: Faq[] = [
  { q: 'Are you affiliated with these businesses?', a: 'No. Nostalgic Hattiesburg is an independent tribute shop. We research each place from archives, old ads and photos, and restore or redraw the art ourselves. We are not affiliated with or endorsed by the businesses, schools or institutions shown.' },
  { q: 'How do the sizes run?', a: 'Our tees fit like a classic unisex tee. Each product page has a size chart with flat measurements; lay a favorite shirt flat and compare. Between sizes? Size up for a relaxed fit. Hats are one size with an adjustable strap, and socks come in S, M and L by shoe size.' },
  { q: 'When will my order arrive?', a: 'Everything is made to order. Most orders ship in 2–5 business days, then take 3–4 business days to reach most US addresses. For Christmas delivery, order by ' + HOLIDAY_CUTOFF + ' with standard shipping.' },
  { q: 'What if something is wrong with my order?', a: 'If your item arrives misprinted, damaged or wrong, email us a photo within 30 days of delivery and we will send a replacement or refund at no cost.' },
  { q: 'Can I return it if it doesn\'t fit?', a: 'Because each piece is printed just for you, we can\'t take back items for fit or a change of mind. Check the size chart first, and email us if you\'re unsure; we\'ll help you pick.' },
  { q: 'Do you ship outside the US?', a: 'Right now we ship within the United States only.' },
  { q: 'Does the welcome discount still get free shipping?', a: 'Free shipping applies when your order total is $' + FREE_SHIP + ' or more after any discount code.' },
];

// Second image for cards/galleries: a close-up of the actual print art (generated from the print files).
const DETAIL = [
  'beverly-drive-in-theatre-tee', 'beverly-drive-in-theatre-tee-natural', 'hub-city-drag-raceway-tee',
  'camelot-music-1974-bag-tee', 'camelot-music-cloverleaf-sign-tee', 'camelot-music-cloverleaf-sign-tee-black',
  'camelot-music-tri-stripe-tee', 'culpepper-body-paint-tee', 'culpepper-body-paint-tee-black',
  'albert-speeds-restaurant-sign-tee', 'albert-speeds-restaurant-sign-tee-black', 'albert-speeds-pylon-tee',
  'mississippi-britches-tee', 'old-english-h-phys-ed-tee-black', 'old-english-h-hattiesburg-physical-education-tee-black',
  'old-english-h-pocket-tee', 'old-english-h-pocket-tee-black', 'old-english-h-phys-ed-ringer-tee',
  'old-english-h-hattiesburg-physical-education-ringer-tee', 'hub-city-drag-raceway-framed-poster-12-12',
  'main-street-hattiesburg-framed-poster-18-12', 'greetings-from-hattiesburg-framed-poster-12-18',
];

export const hattiesburg: TownContent = {
  PLACES, NAMES, FALLBACK_PLACE: null, HIDE_EMPTY_PLACES: false,
  HELD_PREFIXES, SINGLE_COLOR, TYPE_OVERRIDE: {}, blankFor,
  START_HERE, AUTO_START: false,
  NOTE_BY_PREFIX, DESC_OVERRIDE, PAIRS, FAMILIES, MEMBER_LABEL, TITLE_OVERRIDE, FRAME_SIZE, FAQ,
  CATALOG_QUERY: "tag:'town:hattiesburg'",
  includeTags: () => true,
  PRODUCT_IMAGES: productImages as Record<string, string>,
  OPAQUE_IMAGES: opaqueImages,
  // Old English H hat on-model shots, kept local so the thread colour matches the corrected product views.
  PHOTO_IMAGES: ['classic-dad-hat-stone-right-6adc6f66ccea8', 'classic-dad-hat-white-right-6adc6f66ccced'],
  DETAIL, DETAIL_DIR: '/images/hb/detail',
  // Sock mockups re-rendered upright (Printful shows the front sock toe-up).
  SOCK_FIX: ['old-english-h-gym-socks', 'camelot-music-socks', 'hub-city-drag-raceway-socks', 'albert-speeds-socks'], SOCK_DIR: '/images/hb/socks',
  // Mockups left on a Shopify product after its print was repositioned (10-23); they show the old, too-high placement.
  // Safe to delete once the image is removed from the product in Shopify.
  STALE_IMAGE: /\/4e4a54369e0ab7a00dbff1761aa63849_l\./,
  // Hats keep the colour they launched with as the lead photo (Printful now lists another colour's 3/4 view first).
  MAIN_COLOR: {
    'hub-city-drag-raceway-hat': 'Stone', 'camelot-music-hat': 'White', 'camelot-music-hat-dark': 'Black',
    'mississippi-britches-hat': 'Cranberry', 'albert-speeds-hat': 'Stone', 'old-english-h-hat': 'Stone',
    'culpepper-body-paint-hat': 'Stone',
  },
  PLACE_DIR: '/images/hb/places',
  ADD_ONS: ['camelot-music-socks', 'hub-city-drag-raceway-socks', 'albert-speeds-socks', 'hub-city-drag-raceway-hat', 'camelot-music-hat', 'albert-speeds-hat', 'hub-city-drag-raceway-tee', 'camelot-music-1974-bag-tee', 'beverly-drive-in-theatre-tee', 'hub-city-drag-raceway-framed-poster-12-12'],
  MATE_FALLBACK: { Tee: 'hub-city-drag-raceway-hat', Hat: 'beverly-drive-in-theatre-tee', 'Framed print': 'hub-city-drag-raceway-socks' },
  TYPE_IMG: {
    Tee: 'hub-city-drag-raceway-tee', Hat: 'camelot-music-hat', Socks: 'hub-city-drag-raceway-socks', 'Framed print': 'main-street-hattiesburg-framed-poster-18-12',
  },
  COPY: {
    homeTitle: 'Hattiesburg tees, hats & prints',
    metaDescription: 'Tees, hats, socks and framed prints redrawn from lost Hattiesburg signs, ads and postcards: the Beverly Drive-In, Camelot Music, Hub City Drag Raceway and more.',
    ogImage: '/images/hb/og.jpg',
    placesDesc: 'Seven lost Hattiesburg stories, from the Beverly Drive-In to Camelot Music at Cloverleaf Mall, each with its story, sources and collection.',
    shopDesc: 'Every Nostalgic Hattiesburg tee, hat, sock and framed print, by place and by type: the Beverly Drive-In, Hub City Drag Raceway, Camelot Music and more.',
    footerBlurb: 'Tees, hats, socks and prints for the places Hattiesburg remembers, redrawn and restored from the original signs, ads and postcards. Made to order, one at a time.',
    footerLegalHtml: 'Nostalgic Hattiesburg is an independent tribute shop, not affiliated with or endorsed by the businesses, schools or institutions shown. Archival postcards from the MDAH Cooper Postcard Collection, Mississippi Department of Archives and History.',
    aboutDesc: 'How Nostalgic Hattiesburg researches, restores and redraws the places Hattiesburg remembers, and where every image comes from.',
    termsArtworkHtml: 'The designs on this site were researched, restored and redrawn by Nostalgic Hattiesburg. Please don\'t copy or resell them. Archival postcards come from the MDAH Cooper Postcard Collection, which the archive states are in the public domain.',
  },
};
