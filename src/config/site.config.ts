export const siteConfig = {
  townName: "Hammond",
  tagline: "Hammond, Louisiana",
  brandName: "Nostalgic Hammond",
  siteUrl: "https://nostalgichammond.com",
  contactEmail: "info@nostalgichammond.com",
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
