export interface ProductVariant {
  id: string;
  title: string;
  available: boolean;
}

export interface ProductImage {
  src: string;
  alt: string;
}

export interface Product {
  handle: string;
  title: string;
  description: string;
  price: string;
  images: ProductImage[];
  variants: ProductVariant[];
  tags: string[];
  shopifyProductTitle?: string; // For multi-size products that map to one Shopify product
  shopifyVariantId?: string; // Direct Shopify variant ID for dedicated size pages (bypasses string matching)
}

export const mockProducts: Product[] = [
  {
    handle: "cave-tangi-tee-white",
    title: "Cave Tangi Tee — White",
    description: "Drink. Dine. Dance. The Cave Tangi opened in 1938 on the highway between Hammond and Ponchatoula. The sign didn't survive. The memory did.",
    price: "34.00",
    images: [
      { src: "/images/tee-white-01.png", alt: "Cave Tangi Tee White" },
      { src: "/images/tee-white-02.png", alt: "Cave Tangi Tee White - Detail" },
      { src: "/images/tee-white-03.png", alt: "Cave Tangi Tee White - Back" },
      { src: "/images/tee-white-04.png", alt: "Cave Tangi Tee White - Side" },
      { src: "/images/tee-white-05.png", alt: "Cave Tangi Tee White - View" },
      { src: "/images/tee-white-06.png", alt: "Cave Tangi Tee White - Angle" },
    ],
    variants: [
      { id: "s", title: "S", available: true },
      { id: "m", title: "M", available: true },
      { id: "l", title: "L", available: true },
      { id: "xl", title: "XL", available: true },
      { id: "2xl", title: "2XL", available: true },
    ],
    tags: ["cave-tangi", "hammond", "ponchatoula", "tee", "apparel"]
  },
  {
    handle: "cave-tangi-tee-cream",
    title: "Cave Tangi Tee — Cream",
    description: "Drink. Dine. Dance. The Cave Tangi opened in 1938 on the highway between Hammond and Ponchatoula. The sign didn't survive. The memory did.",
    price: "34.00",
    images: [
      { src: "/images/tee-cream-01.png", alt: "Cave Tangi Tee Cream" },
      { src: "/images/tee-cream-02.png", alt: "Cave Tangi Tee Cream - Detail" },
      { src: "/images/tee-cream-03.png", alt: "Cave Tangi Tee Cream - Back" },
      { src: "/images/tee-cream-04.png", alt: "Cave Tangi Tee Cream - Side" },
      { src: "/images/tee-cream-05.png", alt: "Cave Tangi Tee Cream - View" },
      { src: "/images/tee-cream-06.png", alt: "Cave Tangi Tee Cream - Angle" },
    ],
    variants: [
      { id: "s", title: "S", available: true },
      { id: "m", title: "M", available: true },
      { id: "l", title: "L", available: true },
      { id: "xl", title: "XL", available: true },
      { id: "2xl", title: "2XL", available: true },
    ],
    tags: ["cave-tangi", "hammond", "ponchatoula", "tee", "apparel"]
  },
  {
    handle: "cave-tangi-tee-black",
    title: "Cave Tangi Tee — Black",
    description: "Drink. Dine. Dance. The Cave Tangi opened in 1938 on the highway between Hammond and Ponchatoula. The sign didn't survive. The memory did.",
    price: "34.00",
    images: [
      { src: "/images/tee-black-01.png", alt: "Cave Tangi Tee Black" },
      { src: "/images/tee-black-02.png", alt: "Cave Tangi Tee Black - Detail" },
      { src: "/images/tee-black-03.png", alt: "Cave Tangi Tee Black - Back" },
      { src: "/images/tee-black-04.png", alt: "Cave Tangi Tee Black - Side" },
      { src: "/images/tee-black-05.png", alt: "Cave Tangi Tee Black - View" },
      { src: "/images/tee-black-06.png", alt: "Cave Tangi Tee Black - Angle" },
    ],
    variants: [
      { id: "s", title: "S", available: true },
      { id: "m", title: "M", available: true },
      { id: "l", title: "L", available: true },
      { id: "xl", title: "XL", available: true },
      { id: "2xl", title: "2XL", available: true },
    ],
    tags: ["cave-tangi", "hammond", "ponchatoula", "tee", "apparel"]
  },
  {
    handle: "cave-tangi-dad-hat-black",
    title: "Cave Tangi Dad Hat — Black",
    description: "The Cave Tangi, 1938. Hammond and Ponchatoula's roadhouse. Embroidered on a classic dad hat.",
    price: "32.00",
    images: [
      { src: "/images/hat-black-01.png", alt: "Cave Tangi Dad Hat Black" },
      { src: "/images/hat-black-02.png", alt: "Cave Tangi Dad Hat Black - Side" },
      { src: "/images/hat-black-03.png", alt: "Cave Tangi Dad Hat Black - Back" },
      { src: "/images/hat-black-04.png", alt: "Cave Tangi Dad Hat Black - Detail" },
      { src: "/images/hat-black-05.png", alt: "Cave Tangi Dad Hat Black - View" },
      { src: "/images/hat-black-06.png", alt: "Cave Tangi Dad Hat Black - Angle" },
    ],
    variants: [{ id: "os", title: "One Size", available: true }],
    tags: ["cave-tangi", "hammond", "ponchatoula", "hat", "accessory"]
  },
  {
    handle: "cave-tangi-dad-hat-forest",
    title: "Cave Tangi Dad Hat — Forest",
    description: "The Cave Tangi, 1938. Hammond and Ponchatoula's roadhouse. Embroidered on a classic dad hat.",
    price: "32.00",
    images: [
      { src: "/images/hat-forest-01.png", alt: "Cave Tangi Dad Hat Forest" },
      { src: "/images/hat-forest-02.png", alt: "Cave Tangi Dad Hat Forest - Side" },
      { src: "/images/hat-forest-03.png", alt: "Cave Tangi Dad Hat Forest - Back" },
      { src: "/images/hat-forest-04.png", alt: "Cave Tangi Dad Hat Forest - Detail" },
      { src: "/images/hat-forest-05.png", alt: "Cave Tangi Dad Hat Forest - View" },
      { src: "/images/hat-forest-06.png", alt: "Cave Tangi Dad Hat Forest - Angle" },
    ],
    variants: [{ id: "os", title: "One Size", available: true }],
    tags: ["cave-tangi", "hammond", "ponchatoula", "hat", "accessory"]
  },
  {
    handle: "cave-tangi-dad-hat-khaki",
    title: "Cave Tangi Dad Hat — Khaki",
    description: "The Cave Tangi, 1938. Hammond and Ponchatoula's roadhouse. Embroidered on a classic dad hat.",
    price: "32.00",
    images: [
      { src: "/images/hat-khaki-01.png", alt: "Cave Tangi Dad Hat Khaki" },
      { src: "/images/hat-khaki-02.png", alt: "Cave Tangi Dad Hat Khaki - Side" },
      { src: "/images/hat-khaki-03.png", alt: "Cave Tangi Dad Hat Khaki - Back" },
      { src: "/images/hat-khaki-04.png", alt: "Cave Tangi Dad Hat Khaki - Detail" },
      { src: "/images/hat-khaki-05.png", alt: "Cave Tangi Dad Hat Khaki - View" },
      { src: "/images/hat-khaki-06.png", alt: "Cave Tangi Dad Hat Khaki - Angle" },
    ],
    variants: [{ id: "os", title: "One Size", available: true }],
    tags: ["cave-tangi", "hammond", "ponchatoula", "hat", "accessory"]
  },
  {
    handle: "hammond-phys-ed-ringer-tee",
    title: "Hammond Phys Ed Ringer Tee",
    description: "Standard issue. Hammond physical education. Cream and black ringer cut, the way they made them.",
    price: "34.00",
    images: [
      { src: "/images/ringer-tee-01.png", alt: "Hammond Phys Ed Ringer Tee" },
      { src: "/images/ringer-tee-02.png", alt: "Hammond Phys Ed Ringer Tee - Detail" },
      { src: "/images/ringer-tee-03.png", alt: "Hammond Phys Ed Ringer Tee - Back" },
      { src: "/images/ringer-tee-04.png", alt: "Hammond Phys Ed Ringer Tee - Side" },
      { src: "/images/ringer-tee-05.png", alt: "Hammond Phys Ed Ringer Tee - View" },
      { src: "/images/ringer-tee-06.png", alt: "Hammond Phys Ed Ringer Tee - Angle" },
    ],
    variants: [
      { id: "s", title: "S", available: true },
      { id: "m", title: "M", available: true },
      { id: "l", title: "L", available: true },
      { id: "xl", title: "XL", available: true },
      { id: "2xl", title: "2XL", available: true },
    ],
    tags: ["hammond", "phys-ed", "ringer", "tee", "apparel"]
  },
  {
    handle: "tornadoes-crew-neck-sweatshirt",
    title: "Tornadoes Crew Neck Sweatshirt",
    description: "Tornadoes. Hammond's team, Hammond's storm. Crew neck sweatshirt for Friday nights and Saturday mornings.",
    price: "44.00",
    images: [
      { src: "/images/sweatshirt-01.png", alt: "Tornadoes Crew Neck Sweatshirt" },
      { src: "/images/sweatshirt-02.png", alt: "Tornadoes Crew Neck Sweatshirt - Detail" },
      { src: "/images/sweatshirt-03.png", alt: "Tornadoes Crew Neck Sweatshirt - Back" },
      { src: "/images/sweatshirt-04.png", alt: "Tornadoes Crew Neck Sweatshirt - Side" },
      { src: "/images/sweatshirt-05.png", alt: "Tornadoes Crew Neck Sweatshirt - View" },
      { src: "/images/sweatshirt-06.png", alt: "Tornadoes Crew Neck Sweatshirt - Angle" },
    ],
    variants: [
      { id: "s", title: "S", available: true },
      { id: "m", title: "M", available: true },
      { id: "l", title: "L", available: true },
      { id: "xl", title: "XL", available: true },
      { id: "2xl", title: "2XL", available: true },
    ],
    tags: ["tornadoes", "hammond", "sweatshirt", "apparel"]
  },
  {
    handle: "strawberry-stadium-framed-poster",
    title: "Strawberry Stadium — Framed Poster 12×16",
    description: "Southeastern Louisiana College, circa 1940. Hand-tinted postcard, Curt Teich & Co. The stadium was erected in 1937 for $50,000.",
    price: "58.00",
    images: [
      { src: "/images/poster-stadium-01.png", alt: "Strawberry Stadium Framed Poster" },
      { src: "/images/poster-stadium-02.png", alt: "Strawberry Stadium Framed Poster - In Room" },
      { src: "/images/poster-stadium-03.png", alt: "Strawberry Stadium Framed Poster - Detail" },
    ],
    variants: [{ id: "12x16", title: "12×16", available: true }],
    tags: ["strawberry-stadium", "southeastern", "slu", "poster", "wall-art"],
    shopifyProductTitle: "Strawberry Stadium - Framed Poster 12x16",
    shopifyVariantId: "gid://shopify/ProductVariant/62506314826099"
  },
  {
    handle: "greetings-from-hammond-8x10",
    title: "Greetings from Hammond — 8×10",
    description: "Large letter postcard, Curt Teich & Co. The kind they sold at the drugstore on Thomas Street.",
    price: "38.00",
    images: [
      { src: "/images/poster-greetings-8x10-01.png", alt: "Greetings from Hammond 8x10" },
      { src: "/images/poster-greetings-8x10-02.png", alt: "Greetings from Hammond 8x10 - In Room" },
      { src: "/images/poster-greetings-8x10-03.png", alt: "Greetings from Hammond 8x10 - Detail" },
    ],
    variants: [{ id: "8x10", title: "8×10", available: true }],
    tags: ["greetings", "hammond", "postcard", "poster", "wall-art"],
    shopifyProductTitle: "Greetings from Hammond - Framed Poster",
    shopifyVariantId: "gid://shopify/ProductVariant/62506316562803"
  },
  {
    handle: "greetings-from-hammond-11x14",
    title: "Greetings from Hammond — 11×14",
    description: "Large letter postcard, Curt Teich & Co. The kind they sold at the drugstore on Thomas Street.",
    price: "48.00",
    images: [
      { src: "/images/poster-greetings-11x14-01.png", alt: "Greetings from Hammond 11x14" },
      { src: "/images/poster-greetings-11x14-02.png", alt: "Greetings from Hammond 11x14 - In Room" },
      { src: "/images/poster-greetings-11x14-03.png", alt: "Greetings from Hammond 11x14 - Detail" },
    ],
    variants: [{ id: "11x14", title: "11×14", available: true }],
    tags: ["greetings", "hammond", "postcard", "poster", "wall-art"],
    shopifyProductTitle: "Greetings from Hammond - Framed Poster",
    shopifyVariantId: "gid://shopify/ProductVariant/62506316595571"
  },
  {
    handle: "greetings-from-hammond-16x20",
    title: "Greetings from Hammond — 16×20",
    description: "Large letter postcard, Curt Teich & Co. The kind they sold at the drugstore on Thomas Street.",
    price: "72.00",
    images: [
      { src: "/images/poster-greetings-16x20-01.png", alt: "Greetings from Hammond 16x20" },
      { src: "/images/poster-greetings-16x20-02.png", alt: "Greetings from Hammond 16x20 - In Room" },
      { src: "/images/poster-greetings-16x20-03.png", alt: "Greetings from Hammond 16x20 - Detail" },
    ],
    variants: [{ id: "16x20", title: "16×20", available: true }],
    tags: ["greetings", "hammond", "postcard", "poster", "wall-art"],
    shopifyProductTitle: "Greetings from Hammond - Framed Poster",
    shopifyVariantId: "gid://shopify/ProductVariant/62506316628339"
  },
];
