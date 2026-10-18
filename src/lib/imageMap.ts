// Map product handles to local transparent PNG paths
// Bypasses Shopify CDN to use our local images with preserved transparency

interface ImageSet {
  main: string;
  additional?: string[];
}

const imageMap: Record<string, ImageSet> = {
  // Cave Tangi Tees
  'cave-tangi-tee-black': {
    main: '/images/tee-black-01.png',
    additional: ['/images/tee-black-02.png', '/images/tee-black-03.png']
  },
  'cave-tangi-tee-white': {
    main: '/images/tee-white-01.png',
    additional: ['/images/tee-white-02.png', '/images/tee-white-03.png']
  },
  'cave-tangi-tee-cream': {
    main: '/images/tee-cream-01.png',
    additional: ['/images/tee-cream-02.png', '/images/tee-cream-03.png']
  },
  
  // Cave Tangi Dad Hats
  'cave-tangi-dad-hat-black': {
    main: '/images/hat-black-01.png',
    additional: ['/images/hat-black-02.png', '/images/hat-black-03.png']
  },
  'cave-tangi-dad-hat-forest': {
    main: '/images/hat-forest-01.png',
    additional: ['/images/hat-forest-02.png', '/images/hat-forest-03.png']
  },
  'cave-tangi-dad-hat-khaki': {
    main: '/images/hat-khaki-01.png',
    additional: ['/images/hat-khaki-02.png', '/images/hat-khaki-03.png']
  },
  
  // Hammond PE Ringer Tee
  'hammond-phys-ed-ringer-tee': {
    main: '/images/ringer-tee-01.png',
    additional: ['/images/ringer-tee-02.png', '/images/ringer-tee-03.png']
  },
  
  // Tornadoes Sweatshirt
  'tornadoes-crew-neck-sweatshirt': {
    main: '/images/sweatshirt-tornadoes-01.png',
    additional: ['/images/sweatshirt-tornadoes-02.png', '/images/sweatshirt-tornadoes-03.png']
  },
  
  // Strawberry Stadium Poster
  'strawberry-stadium-framed-poster-12-16': {
    main: '/images/poster-stadium-12x16-01.png',
    additional: ['/images/poster-stadium-12x16-02.png']
  },
  
  // Greetings Posters (split variants)
  'greetings-from-hammond-8x10': {
    main: '/images/poster-greetings-8x10-01.png',
    additional: ['/images/poster-greetings-8x10-02.png']
  },
  'greetings-from-hammond-11x14': {
    main: '/images/poster-greetings-11x14-01.png',
    additional: ['/images/poster-greetings-11x14-02.png']
  },
  'greetings-from-hammond-16x20': {
    main: '/images/poster-greetings-16x20-01.png',
    additional: ['/images/poster-greetings-16x20-02.png']
  },
  
  // Retro Sketch Products
  'retro-sketch-raglan-baby-tee': {
    main: '/images/tee-retro-baby-01.png',
    additional: ['/images/tee-retro-baby-02.png', '/images/tee-retro-baby-03.png']
  },
  'retro-sketch-3-4-sleeve-raglan': {
    main: '/images/tee-retro-raglan-01.png',
    additional: ['/images/tee-retro-raglan-02.png', '/images/tee-retro-raglan-03.png']
  },
};

export function getProductImages(handle: string): { src: string; alt: string }[] {
  const imageSet = imageMap[handle];
  
  if (!imageSet) {
    console.warn(`[ImageMap] No local images found for handle: ${handle}`);
    return [{ src: '/images/placeholder.png', alt: 'Product image' }];
  }
  
  const images = [
    { src: imageSet.main, alt: `${handle} product image` }
  ];
  
  if (imageSet.additional) {
    imageSet.additional.forEach((src, index) => {
      images.push({ src, alt: `${handle} product image ${index + 2}` });
    });
  }
  
  return images;
}

export function getMainImage(handle: string): { src: string; alt: string } {
  return getProductImages(handle)[0];
}
