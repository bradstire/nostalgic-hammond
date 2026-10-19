import { mockProducts, type Product } from '../data/mockProducts';
import { siteConfig, town, townSlug } from '../config/site.config';
import { getProductImages, hasLocalImages } from './imageMap';
import { DEFAULT_TOWN } from '../config/towns.mjs';

// A product belongs to a town through a Shopify tag `town:<slug>`.
// The pilot town (Hammond) also keeps every untagged product, so its catalog needs no retagging.
function belongsToThisTown(tags: string[] = []): boolean {
  const townTags = tags.map(t => t.trim().toLowerCase()).filter(t => t.startsWith('town:'));
  if (townTags.length === 0) return townSlug === DEFAULT_TOWN;
  return townTags.includes(`town:${townSlug}`);
}

const USE_LIVE_API = !!siteConfig.shopifyStorefrontToken;

export async function getAllProducts(): Promise<Product[]> {
  if (!USE_LIVE_API) {
    console.log('[Products] Using mock data (no Shopify token configured)');
    return townSlug === DEFAULT_TOWN ? mockProducts : [];
  }

  // TODO: Implement Shopify Storefront API GraphQL call
  console.log('[Products] Fetching from Shopify Storefront API...');
  
  try {
    const response = await fetch(
      `https://${siteConfig.shopifyStoreDomain}/api/2024-01/graphql.json`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Shopify-Storefront-Access-Token': siteConfig.shopifyStorefrontToken,
        },
        body: JSON.stringify({
          query: `
            query GetAllProducts {
              products(first: 250, sortKey: TITLE) {
                edges {
                  node {
                    handle
                    title
                    description
                    priceRange {
                      minVariantPrice {
                        amount
                      }
                    }
                    images(first: 5) {
                      edges {
                        node {
                          url
                          altText
                        }
                      }
                    }
                    variants(first: 20) {
                      edges {
                        node {
                          id
                          title
                          availableForSale
                          price {
                            amount
                          }
                        }
                      }
                    }
                    tags
                  }
                }
              }
            }
          `,
        }),
      }
    );

    const { data } = await response.json();
    
    // Transform Shopify response to our Product interface
    let products: Product[] = [];
    
    data.products.edges.forEach((edge: any) => {
      if (!belongsToThisTown(edge.node.tags)) return;

      // Use local transparent PNGs instead of Shopify CDN when we have them;
      // newer products (other towns) use their Shopify images.
      const shopifyImages = edge.node.images.edges.map((img: any) => ({
        src: img.node.url,
        alt: img.node.altText || edge.node.title,
      }));
      const localImages = hasLocalImages(edge.node.handle) || shopifyImages.length === 0
        ? getProductImages(edge.node.handle)
        : shopifyImages;
      
      const baseProduct = {
        handle: edge.node.handle,
        title: edge.node.title,
        description: edge.node.description,
        price: edge.node.priceRange.minVariantPrice.amount,
        images: localImages, // Local PNG paths
        variants: edge.node.variants.edges.map((v: any) => ({
          id: v.node.id,
          title: v.node.title,
          available: v.node.availableForSale,
        })),
        tags: edge.node.tags,
      };
      
      // Split "Greetings from Hammond" poster variants into separate products
      if (edge.node.handle === 'greetings-from-hammond') {
        const variants = edge.node.variants.edges;
        variants.forEach((variant: any) => {
          const size = variant.node.title;
          // Normalize size string: remove quotes/primes and standardize separator to 'x'
          const normalizedSize = size
            .replace(/[""″′]/g, '') // Remove all types of quotes/primes
            .replace(/×/g, 'x')      // Replace multiplication sign with x
            .toLowerCase()
            .trim();
          
          const splitHandle = `greetings-from-hammond-${normalizedSize}`;
          const splitImages = getProductImages(splitHandle); // Get size-specific images
          
          products.push({
            ...baseProduct,
            handle: splitHandle,
            title: `Greetings from Hammond — ${size.replace(/″/g, '"').replace(/×/g, '×')}`,
            price: variant.node.price.amount,
            images: splitImages, // Size-specific local images
            variants: [{ 
              id: variant.node.id, 
              title: size, 
              available: variant.node.availableForSale 
            }],
            shopifyProductTitle: edge.node.title,
            shopifyVariantId: variant.node.id,
          });
        });
      } else {
        products.push(baseProduct);
      }
    });

    // Custom sort order per town (src/config/towns.mjs). Hammond: Cave Tangi items first, then
    // Hammond PE, Tornadoes, posters (with split Greetings sizes), Retro Sketch.
    const sortOrder: string[] = town.sortOrder;

    products.sort((a, b) => {
      const indexA = sortOrder.indexOf(a.handle);
      const indexB = sortOrder.indexOf(b.handle);
      if (indexA === -1 && indexB === -1) return 0;
      if (indexA === -1) return 1;
      if (indexB === -1) return -1;
      return indexA - indexB;
    });

    return products;
  } catch (error) {
    if (townSlug !== DEFAULT_TOWN) {
      // Never ship the pilot's mock catalog under another town's name.
      throw new Error(`[Products] Shopify fetch failed for town "${townSlug}": ${error}`);
    }
    console.error('[Products] Failed to fetch from Shopify, falling back to mock data:', error);
    return mockProducts;
  }
}

export async function getProductByHandle(handle: string): Promise<Product | null> {
  const products = await getAllProducts();
  return products.find(p => p.handle === handle) || null;
}
