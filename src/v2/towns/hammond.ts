// Hammond content for storefront v2 ("shop by place").
//
// Sourcing rule: every history line traces to one of
//   [repo]   existing site copy: src/towns/hammond/About.astro, src/towns/hammond/collections/ponchatoula.astro,
//            and the Shopify product descriptions written for the pilot;
//   [brief]  HQ's research brief for this build (claude/HAMMOND_WAVE2.md, 10-22), with the source URL given there;
//   [art]    what the artifact itself shows (a postcard caption, an ad, a sign, the Cave Tangi floor medallion).
// When nothing is on the record, the copy says so instead of guessing. Never: people's names, phone numbers,
// anything about violence or crime connected with the Cave Tangi or its era.
import { FREE_SHIP, HOLIDAY_CUTOFF, type Place, type Pair, type Faq, type TownContent, type Blank } from '../shared';
import productImages from './hammond-product-images.json';
import opaqueImages from './hammond-opaque-images.json';

const PLACES: Place[] = [
  {
    slug: 'cave-tangi',
    name: 'The Cave Tangi',
    short: 'Cave Tangi',   // reads "More from Cave Tangi"; headings add the article
    era: '1938',
    line: 'Drink, dine, dance on Highway 51, just north of Ponchatoula.',
    story: [
      // [repo] ponchatoula.astro + product copy ("on the road to Hammond", "Drink. Dine. Dance.")
      'The Cave Tangi opened in October 1938 on Highway 51, just north of Ponchatoula on the road to Hammond. It was a nightclub and restaurant: drink, dine, dance.',
      // [repo] ponchatoula.astro
      'About ten years later the Cave Tangi Drive-In opened across the road. It showed its last picture in 1957.',
      'Hammond folks drove down for it too, and people from both towns still talk about it.',
    ],
    storyIf: [{
      // [brief] the restaurants' napkin (IMG_7198): rooster art, Baton Rouge and Ponchatoula locations
      prefix: 'cave-tangi-restaurants',
      text: 'There were Cave Tangi Restaurants too, in Baton Rouge and Ponchatoula. Our napkin tee follows one of their paper napkins, strutting rooster and all.',
      source: { label: 'Cave Tangi Restaurants paper napkin (Baton Rouge and Ponchatoula), from a photo shared by locals' },
    }],
    facts: [
      { k: 'Opened', v: 'October 1938' },
      { k: 'Where', v: 'Highway 51, north of Ponchatoula' },
      { k: 'Drive-in', v: 'Last picture 1957' },
    ],
    sources: [
      // [art] the inlaid floor medallion in the hero photo reads "CAVE TANGI 1938 OCT-1"
      { label: 'The Cave Tangi floor medallion, inlaid "Cave Tangi 1938 Oct-1" (photograph on our home page)' },
    ],
    prefixes: ['cave-tangi'],
    tile: 'cave-tangi', tone: '#2a211b', ink: '#f4ecdd',
    locality: 'Ponchatoula',
  },
  {
    slug: 'strawberry-stadium',
    name: 'Strawberry Stadium',
    short: 'Strawberry Stadium',
    era: '1937',
    line: 'Built by the WPA and named for the strawberry farmers.',
    story: [
      // [repo] product copy
      'Strawberry Stadium was built in 1937 as a WPA project at Southeastern Louisiana College, and named for the area\'s strawberry farmers.',
      // [repo] product copy + [art] the card's caption
      'Our framed print is a 1940 linen postcard of the stadium, published by Curt Teich & Co.',
    ],
    facts: [
      { k: 'Built', v: '1937, a WPA project' },
      { k: 'Postcard', v: '1940, Curt Teich & Co.' },
    ],
    sources: [{ label: 'Linen postcard, "Strawberry Stadium, Southeastern Louisiana College, Hammond, La.", Curt Teich & Co., 1940' }],
    prefixes: ['strawberry-stadium'],
    tile: 'strawberry-stadium', tone: '#d9cfb8', ink: '#1e1a16',
    note: 'Not affiliated with Southeastern Louisiana University.',
  },
  {
    slug: 'greetings-from-hammond',
    name: 'Greetings from Hammond',
    short: 'Greetings from Hammond',
    era: '1946',
    line: '“The strawberry capital of the world,” on a large-letter postcard.',
    story: [
      // [repo] product copy
      'Our Greetings from Hammond print is a large-letter linen postcard published by Curt Teich & Co. in 1946. The back of the card calls Hammond “the strawberry capital of the world.”',
      // [art]
      'Every letter of HAMMOND holds a scene from town, with strawberries along the bottom. We frame it in three sizes.',
    ],
    facts: [
      { k: 'Published', v: '1946, Curt Teich & Co.' },
      { k: 'Sizes', v: '8×10, 11×14 and 16×20 in' },
    ],
    sources: [{ label: 'Large-letter linen postcard, "Greetings from Hammond, Louisiana", Curt Teich & Co., 1946' }],
    prefixes: ['greetings-from-hammond'],
    tile: 'greetings-from-hammond', tone: '#e9dfc8', ink: '#1e1a16',
  },
  {
    slug: 'hammond-high',
    name: 'Hammond High Tornadoes',
    short: 'Hammond High',
    line: 'Tornadoes on the sweatshirt, phys. ed. on the ringer.',
    story: [
      // [repo] About.astro ("the hallways of Hammond High when 'Tornadoes' meant something") + product copy
      'Tornadoes: Hammond\'s team, Hammond\'s storm. Our crew neck carries the name and a twister in purple, for Friday nights and Saturday mornings.',
      'The Phys. Ed. ringer is our own gym-class design: HAMMOND arched over a blank name banner and PHYSICAL ED., on a natural ringer with black trim.',
    ],
    facts: [],
    sources: [],
    prefixes: ['hammond-phys-ed', 'tornadoes'],
    tile: 'hammond-high', tone: '#f3ecdd', ink: '#1e1a16',
    note: 'Not affiliated with Hammond High Magnet School or the Tangipahoa Parish School System.',
  },
  {
    slug: 'casa-de-fresa',
    name: 'Hotel Casa de Fresa',
    short: 'Hotel Casa de Fresa',
    era: 'Closed 1966',
    line: 'The strawberry buyers’ hotel on the depot block.',
    story: [
      // [brief] NRHP form https://npgallery.nps.gov/GetAsset/c48e5991-58ca-4c94-8904-5e9e187f1ca4
      'The Hotel Casa de Fresa stood on the depot block in Hammond. Its name, Spanish for “House of Strawberries,” was picked in a contest after the 1929 fire, and it was where the strawberry buyers stayed.',
      'The hotel closed in 1966. It burned in 1979 and was later torn down.',
      // [brief] wave 2 art: traced from the hotel's matchbook
      'Our lettering is traced from the hotel\'s own matchbook.',
    ],
    facts: [
      { k: 'Named', v: 'After the 1929 fire' },
      { k: 'Closed', v: '1966' },
      { k: 'Where', v: 'The depot block' },
    ],
    sources: [{ label: 'National Register of Historic Places nomination form (NPGallery)', url: 'https://npgallery.nps.gov/GetAsset/c48e5991-58ca-4c94-8904-5e9e187f1ca4' }],
    prefixes: ['casa-de-fresa'],
    tile: 'casa-de-fresa', tone: '#f1e8d2', ink: '#1e1a16',
    note: 'Not affiliated with any current business using the name.',
  },
  {
    slug: 'toggery-shop',
    name: 'The Toggery Shop',
    short: 'Toggery Shop',
    era: 'Closed 2002',
    line: 'Its 1930s neon sign still hangs on West Thomas Street.',
    story: [
      // [brief] https://hammondhistoricdistrict.org/tour-toggery
      'The Toggery Shop sold men\'s clothing at 105 W. Thomas St. in downtown Hammond until it closed in 2002.',
      'Its 1930s Art Deco neon blade sign still hangs downtown, in the Hammond Historic District.',
      // [brief] wave 2 art: sign redrawn flat; logotype traced from the shop's ad
      'Our designs follow the sign and the logotype from one of the shop\'s own ads.',
    ],
    facts: [
      { k: 'Address', v: '105 W. Thomas St.' },
      { k: 'Closed', v: '2002' },
      { k: 'Sign', v: '1930s Art Deco neon' },
    ],
    sources: [{ label: 'Hammond Historic District walking tour: the Toggery Shop', url: 'https://hammondhistoricdistrict.org/tour-toggery' }],
    prefixes: ['toggery-shop'],
    tile: 'toggery-shop', tone: '#efe5cf', ink: '#1e1a16',
  },
  {
    slug: 'joy-galaxy-drive-in',
    name: 'Joy Twin / Galaxy Drive-In',
    short: 'Joy / Galaxy Drive-In',
    era: '1968–1992',
    line: 'The Joy Twin, later the Galaxy: a drive-in from 1968 to 1992.',
    story: [
      // [brief] https://drive-ins.com/wiki/latjoyd/galaxy-drive-in-theater
      'The drive-in opened in 1968 as the Joy Twin and was later called the Galaxy. It closed in 1992, and apartments stand on the site today.',
      // [art] both passes
      'Our tees follow the theatre\'s driver\'s courtesy passes.',
    ],
    facts: [
      { k: 'Opened', v: '1968, as the Joy Twin' },
      { k: 'Later', v: 'The Galaxy' },
      { k: 'Closed', v: '1992' },
    ],
    sources: [{ label: 'Drive-ins.com: Galaxy Drive-In Theater, Hammond', url: 'https://drive-ins.com/wiki/latjoyd/galaxy-drive-in-theater' }],
    prefixes: ['joy-drive-in', 'galaxy-drive-in'],
    tile: 'joy-galaxy-drive-in', tone: '#14171c', ink: '#f4ecdd',
    note: 'Not affiliated with the Joy Theater in New Orleans.',
  },
  {
    slug: 'rushs-drive-in',
    name: 'Rush\'s Drive-In\u00a0·\u00a0Hammond',   // never the bare name (Brad's differentiation rule)
    short: 'Rush\'s Drive-In',
    line: '“Louisiana’s Finest Drive In,” at 1722 W. Thomas St.',
    story: [
      // [brief] + [art] the drive-in's own ad
      'Rush\'s Drive-In stood at 1722 W. Thomas St. in Hammond. Its own ad called it “Louisiana\'s Finest Drive In.”',
      'Our tee restores that ad, photo and all.',
    ],
    facts: [{ k: 'Address', v: '1722 W. Thomas St.' }],
    sources: [{ label: 'Rush\'s Drive-In advertisement, “Louisiana\'s Finest Drive In” (clipping shared by locals)' }],
    prefixes: ['rushs-drive-in'],
    tile: 'rushs-drive-in', tone: '#e6dcc3', ink: '#1e1a16',
    note: 'Not affiliated with any current business using the name.',
  },
  {
    slug: 'magnolia-inn',
    name: 'Magnolia Inn Restaurant\u00a0·\u00a0Hammond',   // never the bare name (Brad's differentiation rule)
    short: 'Magnolia Inn Restaurant',
    era: '1970s',
    line: 'A motel and 24-hour restaurant at 1111 W. Thomas St.',
    story: [
      // [brief]
      'The Magnolia Inn was a motel and 24-hour restaurant at 1111 W. Thomas St. in Hammond in the 1970s.',
      // [brief] wave 2 art: the sign from a 1970s postcard
      'Our tee redraws its roadside sign from a 1970s postcard.',
    ],
    facts: [
      { k: 'Address', v: '1111 W. Thomas St.' },
      { k: 'Restaurant', v: 'Open 24 hours' },
    ],
    sources: [{ label: 'Postcard of the Magnolia Inn and its sign, 1970s' }],
    prefixes: ['magnolia-inn'],
    tile: 'magnolia-inn', tone: '#dfe9e6', ink: '#1e1a16',
    note: 'Not affiliated with any current business using the name.',
  },
  {
    slug: 'didi-wa',
    name: 'Didi-Wa Restaurant',
    short: 'Didi-Wa Restaurant',
    line: 'Southern fried chicken, Hammond, La.',
    story: [
      // [brief] nothing else is documented
      'Didi-Wa Restaurant served Southern fried chicken in Hammond, La. That\'s what its roadside sign says, and it\'s nearly all we know.',
      'Our tee is redrawn from a photo of the sign shared by locals. If you remember it, we\'d love to hear from you.',
    ],
    facts: [],
    sources: [{ label: 'Photo of the restaurant\'s roadside sign, shared by locals' }],
    prefixes: ['didi-wa'],
    tile: 'didi-wa', tone: '#f6f1e6', ink: '#1e1a16',
  },
  {
    slug: 'fiesta-club',
    name: 'Fiesta Club',
    short: 'Fiesta Club',
    line: 'A club at Town & Country Plaza.',
    story: [
      // [brief] little documented
      'The Fiesta Club was a club at Town & Country Plaza in Hammond. We don\'t know much more than that.',
      'Our design follows the club\'s own logotype. Remember it? Tell us.',
    ],
    facts: [],
    sources: [{ label: 'Fiesta Club logotype, from a photo shared by locals' }],
    prefixes: ['fiesta-club'],
    tile: 'fiesta-club', tone: '#e9a23b', ink: '#1e1a16',
  },
  {
    slug: 'around-hammond',
    name: 'Around Hammond',
    short: 'Around Hammond',
    line: 'A few designs that don’t belong to one place.',
    story: ['A few designs from around town that don\'t belong to one place.'],
    facts: [],
    sources: [],
    prefixes: ['retro-sketch'],
    tile: 'around-hammond', tone: '#f3ecdd', ink: '#1e1a16',
    catchAll: true,
  },
];

// Colour of single-colour products (their Shopify variants carry only a size).
const SINGLE_COLOR: Record<string, string> = {
  'cave-tangi-tee-black': 'Black',
  'cave-tangi-tee-white': 'White',
  'cave-tangi-tee-cream': 'Cream',
  'cave-tangi-dad-hat-black': 'Black',
  'cave-tangi-dad-hat-forest': 'Forest',
  'cave-tangi-dad-hat-khaki': 'Khaki',
  'hammond-phys-ed-ringer-tee': 'Natural / Black',
  'tornadoes-crew-neck-sweatshirt': 'White',
  'retro-sketch-raglan-baby-tee': 'White / Black',
  'retro-sketch-3-4-sleeve-raglan': 'White / Black',
};

// Size chart by blank, read from the Printful mockup file name (new products need no entry here).
// Blanks without a Printful chart on file (sweatshirt, raglans) show no chart rather than a wrong one.
function blankFor(handle: string, imageUrl = ''): Blank | null {
  if (handle.includes('ringer') || imageUrl.includes('unisex-ringer-t-shirt')) return 'ringer';
  if (imageUrl.includes('cotton-heritage-mc1082')) return 'mc1082';
  if (imageUrl.includes('bella-canvas-3001') || imageUrl.includes('unisex-staple-t-shirt')) return 'bc3001';
  return null;
}

// Homepage "Start here" picks, in order. AUTO_START adds the first piece of any place not covered here.
// Brad 10-29 (SFV, applied to every town): the designs drawn from a place's own sign, ad or card lead; our own
// generic designs (phys. ed., greetings) come last. Neighbours alternate garment colour where the catalog allows.
const START_HERE = [
  'cave-tangi-tee-black',
  'didi-wa-restaurant-sign-tee',
  'magnolia-inn-restaurant-sign-tee',
  'fiesta-club-tee',
  'toggery-shop-logo-tee',
  'cave-tangi-dad-hat-black',
  'casa-de-fresa-hotel-dixie-home-ad-tee',
  'strawberry-stadium-framed-poster-12-16',
  'rushs-drive-in-tee',
  'tornadoes-crew-neck-sweatshirt',
  'galaxy-drive-in-courtesy-pass-tee-natural',
  'hammond-phys-ed-ringer-tee',
  'greetings-from-hammond',
];

// Site copy where the store description needs more (frame and garment details from the Printful product).
const DESC_OVERRIDE: Record<string, string> = {
  'greetings-from-hammond': 'A large-letter linen postcard from 1946, published by Curt Teich & Co. The back of the card calls Hammond "the strawberry capital of the world." • Printed on thick enhanced-matte paper • Black wood frame • 8×10, 11×14 or 16×20 in',
  'strawberry-stadium-framed-poster-12-16': 'A 1940 linen postcard of Strawberry Stadium at Southeastern Louisiana College, published by Curt Teich & Co. The stadium was built in 1937 as a WPA project and named for the area\'s strawberry farmers. • Printed on thick enhanced-matte paper • Black wood frame, 12×16 in',
  'cave-tangi-tee-black': 'Drink. Dine. Dance. The Cave Tangi opened in October 1938 on Highway 51, just north of Ponchatoula on the road to Hammond. People still talk about it. • Cotton Heritage MC1082 premium tee • 100% combed ring-spun cotton, 5.5 oz',
  'cave-tangi-tee-white': 'Drink. Dine. Dance. The Cave Tangi opened in October 1938 on Highway 51, just north of Ponchatoula on the road to Hammond. People still talk about it. • Cotton Heritage MC1082 premium tee • 100% combed ring-spun cotton, 5.5 oz',
  'cave-tangi-tee-cream': 'Drink. Dine. Dance. The Cave Tangi opened in October 1938 on Highway 51, just north of Ponchatoula on the road to Hammond. People still talk about it. • Cotton Heritage MC1082 premium tee • 100% combed ring-spun cotton, 5.5 oz',
  'hammond-phys-ed-ringer-tee': 'Standard issue. Our own gym-class design: HAMMOND arched over a blank name banner and PHYSICAL ED., on a natural ringer with black trim. • 100% combed ring-spun cotton • Contrast ringer collar and sleeve cuffs',
};

// Gift pairs: a tee + a hat, each pair clears the free-shipping line ($34 + $32).
const PAIRS: Pair[] = [
  { title: 'The Roadhouse', items: [{ h: 'cave-tangi-tee-black', label: 'Black' }, { h: 'cave-tangi-dad-hat-khaki', label: 'Khaki' }], note: 'Drink, dine, dance: the Cave Tangi on a tee and a cap.' },
  { title: 'The Gym Class', items: [{ h: 'hammond-phys-ed-ringer-tee' }, { h: 'cave-tangi-dad-hat-black', label: 'Black' }], note: 'Phys. ed. by day, the Cave Tangi on a Friday night.' },
  { title: 'The Highway 51', items: [{ h: 'cave-tangi-tee-cream', label: 'Cream' }, { h: 'cave-tangi-dad-hat-forest', label: 'Forest' }], note: 'For the drive down Highway 51, just north of Ponchatoula.' },
];

// Same design in other colours lives in separate Shopify products: one card in grids, linked swatches on the page.
const FAMILIES: string[][] = [
  ['cave-tangi-tee-black', 'cave-tangi-tee-white', 'cave-tangi-tee-cream'],
  ['cave-tangi-dad-hat-black', 'cave-tangi-dad-hat-forest', 'cave-tangi-dad-hat-khaki'],
];

// Display names (Shopify titles carry the colour and frame size; the site shows those as options).
const TITLE_OVERRIDE: Record<string, string> = {
  'cave-tangi-tee-black': 'Cave Tangi Tee (Black)',
  'cave-tangi-tee-white': 'Cave Tangi Tee (White)',
  'cave-tangi-tee-cream': 'Cave Tangi Tee (Cream)',
  'cave-tangi-dad-hat-black': 'Cave Tangi Dad Hat (Black)',
  'cave-tangi-dad-hat-forest': 'Cave Tangi Dad Hat (Forest)',
  'cave-tangi-dad-hat-khaki': 'Cave Tangi Dad Hat (Khaki)',
  'hammond-phys-ed-ringer-tee': 'Hammond Phys. Ed. Ringer Tee',
  'greetings-from-hammond': 'Greetings from Hammond Postcard Framed Print',
  'strawberry-stadium-framed-poster-12-16': 'Strawberry Stadium Postcard Framed Print',
};
const FRAME_SIZE: Record<string, string> = {
  'strawberry-stadium-framed-poster-12-16': '12×16 in, black wood frame',
};

const FAQ: Faq[] = [
  { q: 'Are you affiliated with these businesses?', a: 'No. Nostalgic Hammond is an independent tribute shop. We research each place from postcards, old ads and photos, and restore or redraw the art ourselves. We are not affiliated with or endorsed by the businesses, schools or institutions shown.' },
  { q: 'How do the sizes run?', a: 'Our tees fit like a classic unisex tee. Where we have the maker\'s size chart, it\'s on the product page with flat measurements; lay a favorite shirt flat and compare. Between sizes? Size up for a relaxed fit. Hats are one size with an adjustable strap.' },
  { q: 'When will my order arrive?', a: 'Everything is made to order. Most orders ship in 2–5 business days, then take 3–4 business days to reach most US addresses. For Christmas delivery, order by ' + HOLIDAY_CUTOFF + ' with standard shipping.' },
  { q: 'What if something is wrong with my order?', a: 'If your item arrives misprinted, damaged or wrong, email us a photo within 30 days of delivery and we will send a replacement or refund at no cost.' },
  { q: 'Can I return it if it doesn\'t fit?', a: 'Because each piece is printed just for you, we can\'t take back items for fit or a change of mind. Check the size chart first, and email us if you\'re unsure; we\'ll help you pick.' },
  { q: 'Do you ship outside the US?', a: 'Right now we ship within the United States only.' },
  { q: 'Does the welcome discount still get free shipping?', a: 'Free shipping applies when your order total is $' + FREE_SHIP + ' or more after any discount code.' },
];

export const hammond: TownContent = {
  PLACES, FALLBACK_PLACE: 'around-hammond', HIDE_EMPTY_PLACES: true,
  HELD_PREFIXES: [], SINGLE_COLOR, TYPE_OVERRIDE: { 'tornadoes-crew-neck-sweatshirt': 'Sweatshirt' }, blankFor,
  START_HERE, AUTO_START: true,
  NOTE_BY_PREFIX: {}, DESC_OVERRIDE, PAIRS, FAMILIES, MEMBER_LABEL: {}, TITLE_OVERRIDE, FRAME_SIZE, FAQ,
  // The pilot's products are untagged. New ones are tagged town:hammond-next (the live legacy site skips them, on
  // purpose) or town:hammond. Any other town tag (town:hattiesburg, ...) belongs to another site.
  CATALOG_QUERY: null,
  includeTags: (tags) => {
    const t = tags.map((x) => x.trim().toLowerCase()).filter((x) => x.startsWith('town:'));
    return t.length === 0 || t.includes('town:hammond') || t.includes('town:hammond-next');
  },
  PRODUCT_IMAGES: productImages as Record<string, string>,
  OPAQUE_IMAGES: opaqueImages,
  // Print close-ups: the pilot's hand-made close-up shots (public/images/*-06.png), resized.
  DETAIL: ['cave-tangi-tee-black', 'cave-tangi-tee-white', 'cave-tangi-tee-cream', 'tornadoes-crew-neck-sweatshirt'],
  DETAIL_DIR: '/images/hm/detail',
  SOCK_FIX: ['casa-de-fresa-hotel-socks'], SOCK_DIR: '/images/hm/socks',
  STALE_IMAGE: null,
  PLACE_DIR: '/images/hm/places',
  ADD_ONS: ['cave-tangi-dad-hat-black', 'cave-tangi-dad-hat-khaki', 'cave-tangi-dad-hat-forest', 'cave-tangi-tee-black', 'hammond-phys-ed-ringer-tee', 'greetings-from-hammond', 'strawberry-stadium-framed-poster-12-16'],
  MATE_FALLBACK: { Tee: 'cave-tangi-dad-hat-black', Sweatshirt: 'cave-tangi-dad-hat-black', Hat: 'cave-tangi-tee-black', 'Framed print': null },
  TYPE_IMG: {
    Tee: 'cave-tangi-tee-black', Sweatshirt: 'tornadoes-crew-neck-sweatshirt', Hat: 'cave-tangi-dad-hat-khaki', 'Framed print': 'greetings-from-hammond',
  },
  COPY: {
    homeTitle: 'Hammond tees, hats & prints from the places we remember',
    metaDescription: 'Tees, hats and framed prints redrawn and restored from the places Hammond remembers: the Cave Tangi, Strawberry Stadium, Hammond High and the 1946 Greetings from Hammond postcard.',
    ogImage: '/images/hm/og.jpg',
    placesDesc: 'Lost Hammond stories, from the Cave Tangi on Highway 51 to Strawberry Stadium, each with its story, sources and collection.',
    shopDesc: 'Every Nostalgic Hammond tee, sweatshirt, hat and framed print, by place and by type: the Cave Tangi, Strawberry Stadium, Hammond High and more.',
    footerBlurb: 'Tees, hats and prints for the places Hammond remembers, redrawn and restored from the original signs, ads and postcards. Made to order, one at a time.',
    footerLegalHtml: 'Nostalgic Hammond is an independent tribute shop, not affiliated with or endorsed by the businesses, schools or institutions shown.',
    aboutDesc: 'How Nostalgic Hammond researches, restores and redraws the places Hammond remembers, and where every image comes from.',
    termsArtworkHtml: 'The designs on this site were researched, restored and redrawn by Nostalgic Hammond. Please don\'t copy or resell them.',
  },
};
