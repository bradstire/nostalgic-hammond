export const siteConfig = {
  townName: "Hammond",
  tagline: "Hammond, Louisiana",
  brandName: "Nostalgic Hammond",
  siteUrl: "https://www.nostalgichammond.com",
  contactEmail: "info@nostalgichammond.com",
  // Single source of truth for the free-shipping threshold (banner + cart maths read this).
  // Live store has shown $60 since launch; Shopify shipping rates must match this value.
  freeShippingThreshold: 60,
  accentColor: "#B5533E", // Rust
  secondaryAccent: "#C4A35A", // Aged Gold
  shopifyStoreDomain: "nostalgic-towns.myshopify.com",
  shopifyStorefrontToken: import.meta.env.SHOPIFY_STOREFRONT_TOKEN || "",
  // Meta Pixel ID (not a secret; ships in every page). Empty = pixel disabled.
  metaPixelId: import.meta.env.PUBLIC_META_PIXEL_ID || "",
  socialLinks: {
    instagram: "",
    facebook: "",
  }
};
