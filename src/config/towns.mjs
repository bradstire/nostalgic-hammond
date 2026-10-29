// One storefront codebase, one Shopify store, many towns.
// Each town is a separate Vercel project built from this repo with PUBLIC_TOWN=<slug>.
// Products belong to a town through a Shopify tag: `town:<slug>`.
// Hammond (the pilot) also shows untagged products, so its catalog never needs retagging; its v2 site also
// shows `town:hammond-next` (see src/v2/towns/hammond.ts).
//
// To add a town: copy the hattiesburg entry, add src/towns/<slug>/About.astro,
// tag its products `town:<slug>` in Shopify, and create a Vercel project with PUBLIC_TOWN=<slug>.

export const DEFAULT_TOWN = 'hammond';

export const towns = {
  hammond: {
    slug: 'hammond',
    townName: 'Hammond',
    stateName: 'Louisiana',
    tagline: 'Hammond, Louisiana',
    brandName: 'Nostalgic Hammond',
    siteUrl: 'https://www.nostalgichammond.com',
    contactEmail: 'info@nostalgichammond.com',
    // false = noindex + robots disallow (private preview on its vercel.app URL)
    launched: true,
    // Storefront v2 ("shop by place", src/v2), same as Hattiesburg. The original layout stays in src/legacy.
    layout: 'v2',
    // URLs the original layout published that v2 serves elsewhere (static redirect pages; see astro.config.mjs).
    // The original split the Greetings print's three sizes into pseudo-products; v2 has one product with a size option
    // (?size= picks it on the product page). Astro URL-encodes the destination itself.
    redirects: {
      '/ponchatoula': '/places/cave-tangi',
      '/products/greetings-from-hammond-8x10': '/products/greetings-from-hammond?size=8″×10″',
      '/products/greetings-from-hammond-11x14': '/products/greetings-from-hammond?size=11″×14″',
      '/products/greetings-from-hammond-16x20': '/products/greetings-from-hammond?size=16″×20″',
      // Wave-2 listings Brad pulled 10-25 (archived in Shopify): each goes to what replaced it.
      '/products/casa-de-fresa-hotel-matchbook-tee': '/products/casa-de-fresa-hotel-front-back-tee',   // same mark, on the front
      '/products/toggery-shop-blade-sign-tee': '/products/toggery-shop-logo-tee',                     // sign merged onto the back
      '/products/cave-tangi-restaurants-napkin-tee': '/places/cave-tangi',
    },
    heroImage: '/images/hero-background.jpg',
    heroPosition: 'center 68%',
    popup: { enabled: true, footer: 'Hammond — remembered right.' },
    // Klaviyo list for v2 email signups (the original popup's list; its welcome flow sends WELCOME15).
    klaviyoCompany: 'X6vHTB',
    klaviyoList: 'XdKJkQ',
    footerLinks: [
      { href: '/', label: 'SHOP' },
      { href: '/about', label: 'ABOUT' },
      { href: '/ponchatoula', label: 'PONCHATOULA' },
    ],
    // Sub-collection pages: /<slug>, content in src/towns/<town>/collections/<slug>.astro
    collections: [
      {
        slug: 'ponchatoula',
        title: 'Ponchatoula — the Cave Tangi',
        description:
          'The Cave Tangi opened in October 1938 on Highway 51, just north of Ponchatoula. Tees and hats in its memory.',
        handlePrefix: 'cave-tangi',
      },
    ],
    featured: [
      {
        handle: 'cave-tangi-tee-black',
        badge: 'BEST SELLER',
        title: 'Cave Tangi Tee — Black',
        image: '/images/tee-black-01.png',
        price: '$34',
      },
      {
        handle: 'hammond-phys-ed-ringer-tee',
        badge: 'FEATURED',
        badgeAlt: true,
        title: 'Hammond Phys Ed Ringer Tee',
        image: '/images/ringer-tee-01.png',
        price: '$34',
      },
    ],
    sortOrder: [
      'cave-tangi-tee-white',
      'cave-tangi-tee-cream',
      'cave-tangi-tee-black',
      'cave-tangi-dad-hat-black',
      'cave-tangi-dad-hat-forest',
      'cave-tangi-dad-hat-khaki',
      'hammond-phys-ed-ringer-tee',
      'tornadoes-crew-neck-sweatshirt',
      'strawberry-stadium-framed-poster-12-16',
      'greetings-from-hammond-8x10',
      'greetings-from-hammond-11x14',
      'greetings-from-hammond-16x20',
      'retro-sketch-raglan-baby-tee',
      'retro-sketch-3-4-sleeve-raglan',
    ],
  },

  hattiesburg: {
    slug: 'hattiesburg',
    townName: 'Hattiesburg',
    stateName: 'Mississippi',
    tagline: 'Hattiesburg, Mississippi',
    brandName: 'Nostalgic Hattiesburg',
    siteUrl: 'https://www.nostalgichattiesburg.com',
    contactEmail: 'info@nostalgichattiesburg.com',
    launched: true,
    // Storefront v2 ("shop by place", src/v2).
    layout: 'v2',
    heroImage: '/images/hattiesburg/hero.jpg',
    heroPosition: 'center 55%',
    // No Klaviyo list for this town yet; the popup stays off until one exists.
    popup: { enabled: false, footer: 'Hattiesburg — remembered right.' },
    // Its own Klaviyo account (Nostalgic Hattiesburg, public site ID XH3hzS), list "Email List".
    klaviyoCompany: 'XH3hzS',
    klaviyoList: 'TmFHnz',
    footerLinks: [
      { href: '/', label: 'SHOP' },
      { href: '/about', label: 'ABOUT' },
    ],
    collections: [],
    featured: [],
    sortOrder: [],
  },

  sfv: {
    slug: 'sfv',
    townName: 'San Fernando Valley',
    stateName: 'California',
    tagline: 'San Fernando Valley, California',
    brandName: 'Nostalgic San Fernando Valley',
    // Working URL until a domain is bought (Brad's call); switch siteUrl + contactEmail together then.
    siteUrl: 'https://nostalgic-sfv.vercel.app',
    contactEmail: 'stire.brad@gmail.com',
    // Own icons; and the build ships only images/sfv (none of the shared legacy files).
    iconDir: '/images/sfv',
    strictAssets: true,
    redirects: {
      // Listings retired 10-28 after Brad's wave-2 review (archived in Shopify, reversible): each goes to its place.
      '/products/duttons-books-sign-tee': '/places/records-books',
      '/products/a-little-land-and-a-living-postcard-framed-print': '/places/orchard-valley',
      '/products/burbank-brand-peaches-label-framed-print': '/places/orchard-valley',
    },
    launched: false,
    layout: 'v2',
    heroImage: '/images/sfv/hero/ranchos-wide-1600.webp',
    heroPosition: 'center 50%',
    popup: { enabled: false, footer: 'San Fernando Valley — remembered right.' },
    // No Klaviyo account for this town yet: the site shows no email signup until klaviyoList is set.
    klaviyoCompany: '',
    klaviyoList: '',
    footerLinks: [
      { href: '/', label: 'SHOP' },
      { href: '/about', label: 'ABOUT' },
    ],
    collections: [],
    featured: [],
    sortOrder: [],
  },
};

// Unknown slugs fail the build rather than silently shipping Hammond under another name.
export function resolveTownSlug(raw) {
  const slug = String(raw || DEFAULT_TOWN).trim().toLowerCase();
  if (!towns[slug]) {
    throw new Error(`[towns] Unknown PUBLIC_TOWN "${raw}". Known: ${Object.keys(towns).join(', ')}`);
  }
  return slug;
}
