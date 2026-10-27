import { towns, resolveTownSlug } from './towns.mjs';

// Which town this build is for (resolved in astro.config.mjs: PUBLIC_TOWN, or a `town/<slug>` branch).
export const townSlug = resolveTownSlug(import.meta.env.PUBLIC_TOWN);
export const town = towns[townSlug as keyof typeof towns];

// Storefront API public access token. It is a public, client-side token (Shopify ships these to
// browsers) and the same value is already used by the cart in src/lib/shopify.ts. The env var
// still wins when set, so existing deployments are unchanged.
const PUBLIC_STOREFRONT_TOKEN = '26b7dcdc20879364ff735fbc45846857';

export const siteConfig = {
  townName: town.townName,
  tagline: town.tagline,
  brandName: town.brandName,
  siteUrl: town.siteUrl,
  contactEmail: town.contactEmail,
  // Folder holding favicon.svg + apple-touch-icon.png (v2 layout). Hattiesburg's set is the default.
  iconDir: (town as any).iconDir || '/images/hb',
  // Single source of truth for the free-shipping threshold (banner + cart maths read this).
  // Live store has shown $60 since launch; Shopify shipping rates must match this value.
  freeShippingThreshold: 60,
  accentColor: "#B5533E", // Rust
  secondaryAccent: "#C4A35A", // Aged Gold
  shopifyStoreDomain: "nostalgic-towns.myshopify.com",
  shopifyStorefrontToken: import.meta.env.SHOPIFY_STOREFRONT_TOKEN || PUBLIC_STOREFRONT_TOKEN,
  // Meta Pixel ID (not a secret; ships in every page). Empty = pixel disabled.
  metaPixelId: import.meta.env.PUBLIC_META_PIXEL_ID || "",
  socialLinks: {
    instagram: "",
    facebook: "",
  }
};
