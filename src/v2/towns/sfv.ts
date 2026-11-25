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
      'Around 1908 the Lankershim Development Company mailed a painted bird\'s-eye postcard of the Lankershim and Van Nuys Ranchos, looking from above Los Angeles across Hollywood and the Santa Monica Mountains, with the Pacific at the left. A decade later Little Farms Magazine sold the same dream as "A Little Land and a Living" in California.',
      'The McKeon Canning Company packed the Valley\'s fruit in Burbank under the Burbank Brand label; the library dates one of its peach-can labels to about 1922.',
      'Our framed print reproduces the Ranchos postcard. It is cleaned of dust and enlarged, never repainted.',
    ],
    facts: [
      { k: 'Lankershim ad', v: '1887' },
      { k: 'Ranchos postcard', v: 'c. 1908' },
      { k: 'Little Farms card', v: 'c. 1919' },
      { k: 'McKeon Canning label', v: 'c. 1922' },
    ],
    sources: [
      { label: 'San Fernando Valley History Digital Library, CSUN Oviatt Library: Lankershim and Van Nuys Ranchos postcard, c. 1908 (West Valley Museum)', url: CSUN + '2320' },
      { label: 'Same library: "A Little Land and a Living" small-farm postcard, c. 1919 (West Valley Museum)', url: CSUN + '2354' },
      { label: 'Same library: Lankershim Ranch Land and Water Co. advertisement, 1887', url: CSUN + '2442' },
      { label: 'Same library: Burbank Brand peach can label, McKeon Canning Company, c. 1922 (Burbank Historical Society)', url: CSUN + '1721' },
    ],
    prefixes: ['lankershim-van-nuys-ranchos'],
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
      'San Fernando Raceway, known to locals as "the Pond," opened in 1955 on a triangle of land off Glenoaks Boulevard in San Fernando. It was one of the first purpose-built drag strips in the country and ran for 15 seasons, closing in late 1969. A swap meet later took over the site.',
      'Both designs are our own lockups.',
    ],
    facts: [
      { k: 'Cruise night', v: 'Wednesdays, Van Nuys Blvd.' },
      { k: 'San Fernando Raceway', v: '1955 to late 1969' },
      { k: 'Raceway site later', v: 'A swap meet' },
    ],
    sources: [
      { label: 'NHRA, "They left their hearts in San Fernando" (2008)', url: 'https://www.nhra.com/news/2008/they-left-their-hearts-san-fernando' },
      { label: 'Wikipedia: Cruising (driving), Van Nuys Boulevard', url: 'https://en.wikipedia.org/wiki/Cruising_(driving)' },
    ],
    prefixes: ['van-nuys-blvd-cruise-night', 'san-fernando-raceway', 'june-ellens'],
    storyIf: [{ prefix: 'june-ellens', text: 'June Ellen\'s donuts was one of the turnarounds; the CSUN Daily Sundial wrote about "the June Ellen\'s side" of the boulevard in 1973.', source: { label: 'CSUN Daily Sundial, Nov. 6, 1973, p. 3', url: 'https://digital-collections.csun.edu/digital/collection/Sundial/id/16350' } }],
    tile: 'cruise-night', tone: '#14171c', ink: '#f4ecdd',
  },
  {
    slug: 'valley-music-theatre',
    name: 'Valley Music Theatre',
    short: 'Valley Music Theatre',
    era: '1964',
    line: 'Theater in the round under a dome in Woodland Hills.',
    story: [
      'The Valley Music Theatre opened on July 6, 1964, at 20600 Ventura Boulevard in Woodland Hills: a theater in the round under a concrete dome. Wikipedia gives 2,865 seats; the CSUN archive says 2,500.',
      'The Doors, the Byrds and Buffalo Springfield shared its stage on February 22, 1967. It later became a Jehovah\'s Witnesses assembly hall (in the 1970s by one account, sold in 1980 by the other), and it was torn down by 2007.',
      'Our dome is drawn fresh and the name is set in period lettering.',
    ],
    facts: [
      { k: 'Opened', v: 'July 6, 1964' },
      { k: 'Seats', v: '2,500 to 2,865, in the round' },
      { k: 'Torn down', v: '2006–07' },
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
    era: '1951–1993',
    line: 'The Plaza, GEMCO, Zodys, White Front and Builders Emporium.',
    story: [
      'Valley Plaza opened at Laurel Canyon and Victory in North Hollywood on August 12, 1951, and by the mid-1950s it was called the largest shopping center on the West Coast. It declined after the 1970s, and demolition began on October 29, 2025.',
      'Out on the boulevards the Valley shopped at the discount stores. White Front opened its ninth store at 21300 Roscoe in Canoga Park in May 1963; the chain closed in 1974. Zodys opened at 8201 Topanga Canyon on September 27, 1962, under five hexagon letter boxes, and its California stores closed in March 1986. GEMCO, the members-only department store and supermarket, closed all 80 of its stores that same year. Builders Emporium, the hardware chain that began at Sepulveda and Oxnard in Van Nuys, lasted until 1993.',
      'The signs are redrawn from photos and the membership card, with the old lettering traced wherever the photos hold it.',
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
      { label: 'UPI, "Lucky to close Gemco unit" (Oct. 9, 1986)', url: 'https://www.upi.com/Archives/1986/10/09/Lucky-to-close-Gemco-unit/5698529214400/' },
      { label: 'Wikipedia: Builders Emporium', url: 'https://en.wikipedia.org/wiki/Builders_Emporium' },
      { label: 'Calisphere: "Builders Emporium celebrates birthday," Valley Times photograph, Oct. 13, 1955', url: 'https://calisphere.org/item/00a5692f7cebb935aa6dbc528999262c' },
      { label: 'D. J. Waldie, "For the vanished discounters of suburban L.A.," PBS SoCal (2014)', url: 'https://www.pbssocal.org/commentary/for-the-vanished-discounters-of-suburban-l-a-retail-nostalgia' },
    ],
    prefixes: ['valley-plaza', 'gemco', 'zodys', 'white-front', 'builders-emporium'],
    tile: 'shopping', tone: '#161a20', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using the Valley Plaza, GEMCO, Zodys, White Front or Builders Emporium names.',
  },
  {
    slug: 'coffee-shops',
    name: 'Coffee Shops & Supper Spots',
    short: 'Coffee Shops & Supper Spots',
    era: '1928–2003',
    line: 'Biff\'s, Leon\'s, Phil\'s, Don\'s, Mike\'s and more.',
    story: [
      'Phil\'s Diner, a 1926 dining car called the oldest in California, opened beside the Lankershim depot in 1928 and was moved to 5230 Lankershim Blvd. in 2010. Leon\'s Steak House and Coffee Shop opened at Victory and Vineland in 1945 and closed in July 2003. Don\'s in Burbank started as a drive-in in 1947 and closed in 2002.',
      'Biff\'s Restaurants ran six coffee shops, among them No. 5 on Van Nuys Blvd. at Chase St. and No. 3 on Magnolia at Lankershim. Mike\'s Pizza in Panorama City was "serving since 1954" until 1993. The Jolly Roger put a woodcut galleon on its menus in Sherman Oaks and Canoga Park, Rusty\'s Hacienda ran a cocktail lounge on Lankershim, and Encino Bowl kept a coffee shop next to the lanes from 1962 to 1986.',
      'Each design comes from the place\'s own menu, ad or sign, with the old lettering traced wherever the source holds it.',
    ],
    facts: [
      { k: 'Phil\'s Diner', v: 'from 1928' },
      { k: 'Leon\'s', v: '1945–2003' },
      { k: 'Don\'s, Burbank', v: '1947–2002' },
      { k: 'Encino Bowl', v: '1962–1986' },
    ],
    sources: [
      { label: 'Wikipedia: Phil\'s Diner', url: 'https://en.wikipedia.org/wiki/Phil%27s_Diner' },
      { label: 'Angels Walk LA: NoHo Self Guided Historic Trail guidebook (2014), stop 31, Phil\'s Diner', url: 'https://www.angelswalkla.org/wp-content/uploads/AWLA_NOHO_GUIDEBOOK.pdf' },
      { label: 'Biff\'s Restaurants menu cover, 1950s: "Six Locations" (posted by the Valley Relics Museum)' },
      { label: 'Roadside Architecture: Don\'s Restaurant sign, Burbank', url: 'https://www.roadarch.com/signs/ca6.html' },
      { label: 'Roadside Peek: Leon\'s Steak House, North Hollywood', url: 'https://roadsidepeek.com/roadusa/southwest/california/socal/socaleats/socalsitdown/index2.htm' },
      { label: 'The Valley Observed: Gone But Not Forgotten (Leon\'s)', url: 'https://www.americassuburb.com/gone.html' },
      { label: 'Valley Relics Museum archive: The Jolly Roger menu (Gorsky Menu Collection)', url: 'https://valleyrelicsmuseum.org/archives/items/show/566' },
      { label: 'Los Angeles Public Library Menu Collection: Rusty\'s Hacienda menu, c. 1965', url: 'https://tessa2.lapl.org/digital/collection/menus/id/3082' },
    ],
    prefixes: ['biffs-restaurants', 'phils-diner', 'leons', 'dons-restaurant', 'mikes-pizza', 'the-jolly-roger', 'rustys-hacienda', 'encino-bowl'],
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
      'The signs, matchbook and coupon art are traced from the originals; only lines too small to trace are re-set.',
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
      'Moby Disc Records grew from a store on Victory Boulevard in the early 1970s into a small chain, with stores at 14410 Ventura in Sherman Oaks and on Topanga Canyon in Canoga Park. It was sold in 2000 and its last stores closed in the early 2000s. Its sleeves carried a whale spouting a record: "A Whale of a Store!"',
      'Dutton\'s Books opened at Laurel Canyon and Magnolia in North Hollywood on New Year\'s Day 1961, selling books and art, "New-Old & Rare, Bought & Sold," as the rooftop sign said. The North Hollywood store closed in 2006.',
    ],
    facts: [{ k: 'Dutton\'s, North Hollywood', v: '1961–2006' }, { k: 'Moby Disc', v: 'early 1970s–early 2000s' }],
    sources: [
      { label: 'Wikipedia: Dutton\'s Books', url: 'https://en.wikipedia.org/wiki/Dutton%27s_Books' },
      { label: 'Daily Bruin, "Moby Disc runs out on lease" (Feb. 11, 2002)', url: 'https://dailybruin.com/2002/02/11/moby-disc-runs-out-on-lease-ci' },
      { label: 'Los Angeles Business Journal (Jan. 15, 2006): Moby Disc sold to Djangos.com in 2000', url: 'https://labusinessjournal.com/?p=11685' },
      { label: 'LA Weekly, "Bob Say" (2007)', url: 'https://www.laweekly.com/bob-say/' },
    ],
    prefixes: ['moby-disc'],
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
      'Devonshire Downs, at Devonshire Street and Zelzah Avenue in Northridge, held its first Sunday harness races in 1946. The state bought it in 1948 for the San Fernando Valley Fair, and it later became part of San Fernando Valley State College, now CSUN. Racing faded in the 1960s, the last race horse left in 1971, and most of the buildings came down in 2001.',
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

// One page per business inside a shared place (/places/<slug>). Products keep their place (the category page).
const NAMES: Place[] = [
  {
    slug: 'gemco',
    name: 'GEMCO',
    short: 'GEMCO',
    era: '1959–1986',
    line: 'The membership department store, card and all.',
    story: [
      'GEMCO was a membership department store chain that sold groceries, clothing and household goods. It started in Anaheim in October 1959 and was bought a year later by Lucky Stores, the supermarket company.',
      'Members got a monthly catalog, the Gemco Courier. The name was never an acronym; it was chosen to be easy to say and remember.',
      'Lucky closed the chain in late 1986: all 80 stores, in California, Arizona and Nevada, with the clearance running from September to November. Many of the leases went to Target, which had opened in most of the old GEMCO buildings by the fall of 1987.',
      'Our tee is redrawn from a GEMCO membership card, with the store-sign letters traced.',
    ],
    facts: [
      { k: 'Founded', v: 'Oct. 1959, Anaheim' },
      { k: 'Closed', v: 'Late 1986' },
      { k: 'Afterward', v: 'Most stores became Target, 1987' },
    ],
    sources: [
      { label: 'Wikipedia: Gemco', url: 'https://en.wikipedia.org/wiki/Gemco' },
      { label: 'UPI, "Lucky to close Gemco unit" (Oct. 9, 1986)', url: 'https://www.upi.com/Archives/1986/10/09/Lucky-to-close-Gemco-unit/5698529214400/' },
      { label: 'Calisphere: interior of a Gemco store, Herald-Examiner Collection photographs', url: 'https://calisphere.org/item/73346a68cfa236372add2d67b410553a' },
    ],
    prefixes: ['gemco'],
    parent: 'shopping',
    tile: 'gemco', tone: '#f6f1e6', ink: '#1e1a16',
    note: 'Not affiliated with any current business using the GEMCO name.',
  },
  {
    slug: 'leons-steak-house',
    name: 'Leon\'s Steak House',
    short: 'Leon\'s Steak House',
    era: '1945–2003',
    line: 'Steaks, a coffee shop and a piano bar at Victory and Vineland.',
    story: [
      'Leon\'s Steak House and Coffee Shop stood at the northeast corner of Victory Boulevard and Vineland Avenue in North Hollywood. It opened in 1945 and fed workers from the nearby aerospace plants, Lockheed among them.',
      'It was two places under one roof: a coffee shop and a steak house with a piano bar, where Buddy Worth played on Tuesday nights for years.',
      'Leon\'s closed in July 2003, when its lease ran out, after nearly 58 years. The building was torn down and a drugstore took the corner.',
      'Our tee is redrawn from the roadside sign. The LEONS letters and the brush-lettered COFFEE SHOP are traced from a photo of it.',
    ],
    facts: [
      { k: 'Opened', v: '1945' },
      { k: 'Closed', v: 'July 2003' },
      { k: 'Corner', v: 'Victory & Vineland, North Hollywood' },
    ],
    sources: [
      { label: 'Roadside Peek: Leon\'s Steak House, North Hollywood', url: 'https://roadsidepeek.com/roadusa/southwest/california/socal/socaleats/socalsitdown/index2.htm' },
      { label: 'The Valley Observed: Gone But Not Forgotten (Leon\'s)', url: 'https://www.americassuburb.com/gone.html' },
    ],
    prefixes: ['leons'],
    parent: 'coffee-shops',
    tile: 'leons-steak-house', tileTall: true, tone: '#f6f1e6', ink: '#1e1a16',
    note: 'Not affiliated with any current business using the Leon\'s name.',
  },
  {
    slug: 'zodys',
    name: 'Zodys',
    short: 'Zodys',
    era: '1960–1986',
    line: 'The discount store under five hexagon letters.',
    story: [
      'Zodys was a discount department store chain from Hartfield Stores, a Los Angeles women\'s clothing company. The first one opened in Garden Grove in June 1960, and by 1962 the company had renamed itself Hartfield-Zodys.',
      'The Canoga Park store opened at 8201 Topanga Canyon Boulevard, at Roscoe, on September 27, 1962. The Valley Times photographed the crowd pressing in that morning and reported that the doors were opened by a radio signal, at the same moment as a new store in West Covina. Northridge already had a Zodys, Burbank got one that December and North Hollywood followed in 1969.',
      'The chain grew to 37 stores by 1979. Its parent began closing them in 1984, and the last California stores shut in March 1986. Many of the locations were sold to the owner of the Ralphs supermarkets and to HomeClub.',
      'Our tee is redrawn from a photo of the Canoga Park canopy sign: five hexagon boxes with one letter in each. The letters are traced.',
    ],
    facts: [
      { k: 'Canoga Park opened', v: 'Sept. 27, 1962' },
      { k: 'Address', v: '8201 Topanga Canyon Blvd.' },
      { k: 'Closed', v: 'March 1986' },
    ],
    sources: [
      { label: 'Wikipedia: Hartfield-Zodys', url: 'https://en.wikipedia.org/wiki/Hartfield-Zodys' },
      { label: 'Calisphere: "Radio wave opens doors of Zodys in Canoga Park," Valley Times photograph, Sept. 28, 1962', url: 'https://calisphere.org/item/58b1e8b061e2882e8f379338c2431ca3/' },
    ],
    prefixes: ['zodys'],
    parent: 'shopping',
    tile: 'zodys', tone: '#101010', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using the Zodys name.',
  },
  {
    slug: 'white-front',
    name: 'White Front',
    short: 'White Front',
    era: '1929–1974',
    line: 'The discount store behind the giant arch.',
    story: [
      'White Front began in 1929 as a small self-service grocery on Central Avenue in Los Angeles, opened by Harry Blackman and named for the color of its storefront. It grew into a discount store known for appliances, opened a second store on Sherman Way in Van Nuys in October 1957, and was bought by Interstate Department Stores in April 1959.',
      'The Canoga Park store opened on Roscoe Boulevard in May 1963. The Valley Times counted it as the ninth White Front in Southern California and the second in the Valley. A third Valley store followed in Pacoima that fall, billed as the chain\'s largest in California.',
      'The stores were known for their fronts: an enormous, sweeping archway with the name spelled out in letters fanned across the top. At its height in mid-1972 the chain had 37 stores in three states. That December Interstate announced it would close 21 of them, and the rest shut in 1974, when the parent company filed for bankruptcy.',
      'Our tee redraws that entrance from a photo posted by the Valley Relics Museum, with a box for each letter across the crown. The arch is our own drawing after the photo, and the lettering is re-set.',
    ],
    facts: [
      { k: 'Canoga Park opened', v: 'May 1963' },
      { k: 'Chain founded', v: '1929, Los Angeles' },
      { k: 'Closed', v: '1974' },
    ],
    sources: [
      { label: 'Wikipedia: White Front', url: 'https://en.wikipedia.org/wiki/White_Front' },
      { label: 'Calisphere: opening of the Canoga Park White Front store, Valley Times photograph, June 3, 1963', url: 'https://calisphere.org/item/3d77f0d46efe877b0c2d6cafd4fb86ac/' },
      { label: 'Calisphere: White Front opens in Pacoima, Valley Times photograph, Nov. 1, 1963', url: 'https://calisphere.org/item/b22a61fa24891a0d83c073b4ae6288ab' },
      { label: 'D. J. Waldie, "For the vanished discounters of suburban L.A.," PBS SoCal (2014)', url: 'https://www.pbssocal.org/commentary/for-the-vanished-discounters-of-suburban-l-a-retail-nostalgia' },
    ],
    prefixes: ['white-front'],
    parent: 'shopping',
    tile: 'white-front', tone: '#f6f1e6', ink: '#1e1a16',
    note: 'Not affiliated with any current business using the White Front name.',
  },
  {
    slug: 'valley-plaza',
    name: 'Valley Plaza',
    short: 'Valley Plaza',
    era: '1951–2025',
    line: 'North Hollywood\'s shopping center at Laurel Canyon and Victory.',
    story: [
      'Valley Plaza opened at Laurel Canyon and Victory boulevards in North Hollywood on August 12, 1951. The idea was developer Bob Symonds\'s, going back to 1942: a shopping center built for people arriving by car, with parking for 4,000. Sears opened that September, and J. C. Penney added a two-level store in February 1959.',
      'By 1956 the Valley Times was reporting it as the largest shopping center on the West Coast and the third largest in the country. In 1960 the Los Angeles Federal Savings and Loan tower, now called the Valley Plaza Tower, was finished; it was the tallest building in the Valley when it opened.',
      'Newer malls drew shoppers away, and the 1994 Northridge earthquake hurt it further. Sears closed in 2019. In August 2025 the city declared six empty buildings a public nuisance, and demolition began on October 29, 2025.',
      'Our tee is redrawn from a photo of the Valley Plaza pole sign: the stepped panel, the double border and the tall channel letters.',
    ],
    facts: [
      { k: 'Opened', v: 'Aug. 12, 1951' },
      { k: 'Corner', v: 'Laurel Canyon & Victory, North Hollywood' },
      { k: 'Demolition began', v: 'Oct. 29, 2025' },
    ],
    sources: [
      { label: 'Wikipedia: Valley Plaza', url: 'https://en.wikipedia.org/wiki/Valley_Plaza' },
    ],
    prefixes: ['valley-plaza'],
    parent: 'shopping',
    tile: 'valley-plaza', tileTall: true, tone: '#161a20', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using the Valley Plaza name.',
  },
  {
    slug: 'builders-emporium',
    name: 'Builders Emporium',
    short: 'Builders Emporium',
    era: '1946–1993',
    line: 'The Van Nuys hardware store that became a chain.',
    story: [
      'Builders Emporium started in Van Nuys in August 1946, when Si L. Bercutt opened a hardware store on Sepulveda Boulevard under the motto "Everything to build anything." The store stood at 5960 Sepulveda, at Oxnard Street.',
      'Victor M. Carter bought the ailing store in 1949. In October 1954 the Valley Times photographed him opening a month-long "Gay Ninety Days" sale from the driver\'s seat of an early Cadillac, with bearded salesmen and 5,000 derby hats to give away. A year later the paper showed him serving the first slice of a 40-foot birthday cake for the store\'s ninth anniversary.',
      'Food Giant Markets bought the company in 1962, and Two Guys took it over in 1967, when Builders Emporium had 14 stores across Southern California. Wickes Companies bought the chain in 1978. It closed in 1993 with 82 stores in Southern California and 15 more in Nevada, New Mexico, Arizona and Texas.',
      'Our tee is traced from a 1961 Builders Emporium brochure shared by the Valley Relics Museum: the logo, the line "America\'s Greatest Hardware Stores" and the B·E beaver with his armful of pipe.',
    ],
    facts: [
      { k: 'Opened', v: 'Aug. 1946' },
      { k: 'First store', v: '5960 Sepulveda Blvd., Van Nuys' },
      { k: 'Closed', v: '1993' },
    ],
    sources: [
      { label: 'Wikipedia: Builders Emporium', url: 'https://en.wikipedia.org/wiki/Builders_Emporium' },
      { label: 'Calisphere: "Builders Emporium celebrates birthday," Valley Times photograph, Oct. 13, 1955', url: 'https://calisphere.org/item/00a5692f7cebb935aa6dbc528999262c' },
      { label: 'Calisphere: "Gay Ninety Days" at Builders Emporium, Valley Times photograph, Oct. 20, 1954', url: 'https://calisphere.org/item/7b5eef627d1f3cb2f0e6e94cc32a28ea/' },
    ],
    prefixes: ['builders-emporium'],
    parent: 'shopping',
    tile: 'builders-emporium', tileTall: true, tone: '#0f84a6', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using the Builders Emporium name.',
  },
  {
    slug: 'biffs',
    name: 'Biff\'s Restaurants',
    short: 'Biff\'s',
    era: 'From 1948',
    line: 'Tiny Naylor\'s coffee shops, two of them in the Valley.',
    story: [
      'Biff\'s was the coffee shop chain of W. W. "Tiny" Naylor, who came to Los Angeles after running waffle shops in central California. The first Biff\'s opened in 1948 at Yucca and Cahuenga in Hollywood, named for his son. A year later he opened the first Tiny Naylor\'s, the drive-in at Sunset and La Brea.',
      'A Biff\'s menu in the Los Angeles Public Library, dated 1948 to 1951, lists three shops: Beverly Hills, Hollywood and 11146 Magnolia Blvd. in North Hollywood. The 1950s menu cover our tee comes from prints "Six Locations," and two are in the Valley: No. 3, Magnolia at Lankershim, and No. 5, 8510 Van Nuys Blvd. at Chase St.',
      'Tiny Naylor died in August 1959 and Biff Naylor took over the business. Together, Biff\'s and Tiny Naylor\'s came to more than 40 restaurants in Los Angeles and Orange counties. We have not found a dated record of when the two Valley shops closed.',
      'Our tee is traced from that menu cover, shared by the Valley Relics Museum: the restaurant and its tower with the neon script, the Biff\'s signature and RESTAURANTS on its climb, in the cover\'s own cream, yellow and red.',
    ],
    facts: [
      { k: 'First Biff\'s', v: '1948, Hollywood' },
      { k: 'No. 3', v: '11146 Magnolia Blvd., North Hollywood' },
      { k: 'No. 5', v: '8510 Van Nuys Blvd. at Chase St.' },
    ],
    sources: [
      { label: 'Biff\'s Restaurants menu cover, 1950s: "Six Locations" (posted by the Valley Relics Museum)' },
      { label: 'Calisphere: Biffs menu, 1948–1951, Los Angeles Public Library Menu Collection', url: 'https://calisphere.org/item/1f9e8dd94dcadcd536623fe612490440/' },
      { label: 'Water and Power Associates: Tiny Naylor\'s', url: 'https://waterandpower.org/Museum2/Tiny_Naylors.html' },
      { label: 'Patric Kuh, Los Angeles magazine, Nov. 21, 2017', url: 'https://www.lamag.com/mag-features/vintage-diners/' },
      { label: 'Wikipedia: Tiny Naylor\'s', url: 'https://en.wikipedia.org/wiki/Tiny_Naylor%27s' },
    ],
    prefixes: ['biffs-restaurants'],
    parent: 'coffee-shops',
    tile: 'biffs', tileTall: true, tone: '#2b422e', ink: '#f4ecdd',
    note: 'Not affiliated with any current business using the Biff\'s name.',
  },
  {
    slug: 'phils-diner',
    name: 'Phil\'s Diner',
    short: 'Phil\'s Diner',
    era: 'From 1928',
    line: 'The pink dining car by the Lankershim depot.',
    story: [
      'Phil\'s Diner is a dining car, believed to have been built in 1926 by the Phillips Company, which is where the name is said to come from. It has been called the oldest dining car in California. Phil\'s opened in it in 1928 at 11138 Chandler Blvd., alongside the Lankershim train depot in North Hollywood.',
      'It fed the railroad district for about seventy years and closed in the late 1990s, when subway construction came to the block. Casey Hallenbeck bought the car in 1998 and it sat in storage for more than a decade.',
      'On November 16, 2010 a crane set the 25,000-pound car down at 5230 Lankershim Blvd. It reopened in April 2011 after a $1.1 million restoration and closed again that December 11. The original neon sign had been stolen, so a new one was made from photographs. Other restaurants have used the car since.',
      'Our tee is our own drawing of the car and its pole sign, after a 1950s photo of the Chandler Blvd. site.',
    ],
    facts: [
      { k: 'Opened', v: '1928' },
      { k: 'First site', v: '11138 Chandler Blvd., North Hollywood' },
      { k: 'Moved', v: 'Nov. 2010, to 5230 Lankershim Blvd.' },
    ],
    sources: [
      { label: 'Angels Walk LA: NoHo Self Guided Historic Trail guidebook (2014), stop 31, Phil\'s Diner', url: 'https://www.angelswalkla.org/wp-content/uploads/AWLA_NOHO_GUIDEBOOK.pdf' },
      { label: 'Wikipedia: Phil\'s Diner', url: 'https://en.wikipedia.org/wiki/Phil%27s_Diner' },
      { label: 'Calisphere: Phil\'s Diner on Chandler Boulevard, Los Angeles Public Library photograph, Feb. 2000', url: 'https://calisphere.org/item/f0658b16a290f6c190891a6a22b0b1bc/' },
      { label: 'LAist, "Historic Phil\'s Diner hoisted into NoHo" (Nov. 17, 2010)', url: 'https://laist.com/news/food/historic-phils-diner-hoisted-into-n' },
      { label: 'Los Angeles Daily News, "Phil\'s Diner closes in NoHo, seeks new owner" (Dec. 20, 2011)', url: 'https://www.dailynews.com/2011/12/20/phils-diner-closes-in-noho-seeks-new-owner/' },
    ],
    prefixes: ['phils-diner'],
    parent: 'coffee-shops',
    tile: 'phils-diner', tone: '#eeb5bd', ink: '#1e1a16',
    note: 'Not affiliated with any current business at the car\'s present site.',
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
  'biffs-restaurants-menu-tee': 'Forest',
  'builders-emporium-van-nuys-tee': 'Aqua',
};

const BC3001 = new Set(['moby-disc-records-tee', 'the-pass-club-tee', 'phils-diner-tee', 'the-sugar-shack-tee', 'fantasy-faire-1967-tee', 'biffs-restaurants-menu-tee', 'builders-emporium-van-nuys-tee']);

function blankFor(handle: string): Blank | null {
  if (handle.includes('ringer')) return 'ringer';
  if (BC3001.has(handle)) return 'bc3001';
  if (handle.endsWith('-hat') || handle.includes('framed-print')) return null;
  return 'mc1082';
}

// Brad 10-31: the Shop page still led with the generic wave-1 lockups (it sorted by story, and the first stories
// were the Orchard Valley print and Greetings). Ranked order now, strongest first: measured Facebook signal
// (SFV_WAVE2.md score) weighed with how the design reads as a thumbnail, garment colours alternated so
// neighbours differ. Our own lockups (Greetings, phys. ed.) close the list. June Ellen's moved up 10-31 once its
// v2 art (the storefront sign) replaced the font-set script. Brad 11-01: Biff's and Builders Emporium are top-tier
// graphic work (traced whole from a menu cover and a brochure), so they lead with FM; low scorers stay, at the bottom.
const SHOP_ORDER = [
  'fm-station-north-hollywood-tee',
  'biffs-restaurants-menu-tee',
  'mikes-pizza-menu-tee',
  'builders-emporium-van-nuys-tee',
  'valley-plaza-sign-tee',
  'leons-steak-house-sign-tee',
  'zodys-canoga-park-tee',
  'june-ellens-donuts-tee',
  'gemco-membership-card-tee',
  'encino-bowl-sign-tee',
  'white-front-canoga-park-tee',
  'the-jolly-roger-menu-tee',
  'moby-disc-records-tee',
  'devonshire-downs-tee',
  'van-nuys-blvd-cruise-night-tee',
  'the-pass-club-tee',
  'phils-diner-tee',
  'webers-place-reseda-tee',
  'san-fernando-raceway-tee',
  'sasch-studio-city-tee',
  'rustys-hacienda-tee',
  'the-sugar-shack-tee',
  'dons-restaurant-burbank-tee',
  'valley-music-theatre-tee',
  'fantasy-faire-1967-tee',
  'van-nuys-blvd-cruise-night-hat',
  'lankershim-van-nuys-ranchos-postcard-framed-print',
  'van-nuys-phys-ed-ringer-tee',
  'san-fernando-phys-ed-tee',
  'greetings-from-san-fernando-valley-tee',
];

// Home "Start here": the first twelve of the ranked order, exactly (no auto-added story leads, so Greetings stays off the rail).
const START_HERE = SHOP_ORDER.slice(0, 12);

// Stories in the same spirit: the places with the strongest signage and signal first, our own lockups last.
const PLACE_ORDER = ['shopping', 'coffee-shops', 'after-dark', 'cruise-night', 'records-books', 'devonshire-downs', 'valley-music-theatre', 'orchard-valley', 'phys-ed', 'greetings'];
const PLACES_RANKED = [...PLACES].sort((a, b) => PLACE_ORDER.indexOf(a.slug) - PLACE_ORDER.indexOf(b.slug));

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
  PLACES: PLACES_RANKED, NAMES, FALLBACK_PLACE: null, HIDE_EMPTY_PLACES: true,
  HELD_PREFIXES: [], SINGLE_COLOR, TYPE_OVERRIDE: {}, blankFor,
  START_HERE, AUTO_START: false, SHOP_ORDER,
  NOTE_BY_PREFIX, DESC_OVERRIDE: {}, PAIRS, FAMILIES, MEMBER_LABEL, TITLE_OVERRIDE, FRAME_SIZE, FAQ,
  CATALOG_QUERY: "tag:'town:sfv'",
  includeTags: () => true,
  PRODUCT_IMAGES: productImages as Record<string, string>,
  OPAQUE_IMAGES: opaqueImages,
  DETAIL: [], DETAIL_DIR: '/images/sfv/detail',
  SOCK_FIX: [], SOCK_DIR: '/images/sfv/socks',
  STALE_IMAGE: null,
  PLACE_DIR: '/images/sfv/places',
  ADD_ONS: ['van-nuys-blvd-cruise-night-hat', 'van-nuys-blvd-cruise-night-tee', 'fm-station-north-hollywood-tee', 'lankershim-van-nuys-ranchos-postcard-framed-print'],
  MATE_FALLBACK: { Tee: 'van-nuys-blvd-cruise-night-hat', Hat: 'van-nuys-blvd-cruise-night-tee', 'Framed print': 'fm-station-north-hollywood-tee' },
  TYPE_IMG: { Tee: 'fm-station-north-hollywood-tee', Hat: 'van-nuys-blvd-cruise-night-hat', 'Framed print': 'lankershim-van-nuys-ranchos-postcard-framed-print' },
  COPY: {
    homeTitle: 'San Fernando Valley tees, hats & prints',
    metaDescription: 'Tees, hats and framed prints from the San Fernando Valley we remember: Valley Plaza, GEMCO, Zodys, Moby Disc, FM Station, Phil\'s Diner and cruise night.',
    ogImage: '/images/sfv/og.jpg',
    placesDesc: 'The San Fernando Valley we remember, by theme: Valley Plaza and the discount stores, coffee shops, the clubs after dark, cruise night and more.',
    shopDesc: 'Every Nostalgic San Fernando Valley tee, hat and framed print, by place and by type: Valley Plaza, GEMCO, Zodys, Moby Disc, FM Station, Leon\'s and more.',
    footerBlurb: 'Tees, hats and prints for the San Fernando Valley we remember, redrawn and restored from old postcards, labels, ads and signs. Made to order, one at a time.',
    footerLegalHtml: 'Nostalgic San Fernando Valley is an independent tribute shop, not affiliated with or endorsed by the businesses, schools or institutions shown. Archival images from the San Fernando Valley History Digital Library, CSUN Oviatt Library.',
    aboutDesc: 'How Nostalgic San Fernando Valley researches, restores and redraws the Valley we remember, and where every image comes from.',
    startTitle: 'Start here: the Valley\'s own signs, then every story',
    termsArtworkHtml: 'The designs on this site were researched, restored and redrawn by Nostalgic San Fernando Valley. Please don\'t copy or resell them. Archival postcards come from the San Fernando Valley History Digital Library at CSUN, which lists them as public domain.',
  },
};
