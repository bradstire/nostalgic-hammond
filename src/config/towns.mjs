// One storefront codebase, one Shopify store, many towns.
// Each town is a separate Vercel project built from this repo with PUBLIC_TOWN=<slug>.
// Products belong to a town through a Shopify tag: `town:<slug>`.
// Hammond (the pilot) also shows untagged products, so its catalog never needs retagging.
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
    heroImage: '/images/hero-background.jpg',
    heroPosition: 'center 68%',
    popup: { enabled: true, footer: 'Hammond — remembered right.' },
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
    launched: false,
    heroImage: '/images/hattiesburg/hero.jpg',
    heroPosition: 'center 55%',
    // No Klaviyo list for this town yet; the popup stays off until one exists.
    popup: { enabled: false, footer: 'Hattiesburg — remembered right.' },
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
