import { mockProducts, type Product } from '../data/mockProducts';
import { siteConfig } from '../config/site.config';
import { getProductImages } from './imageMap';

const USE_LIVE_API = !!siteConfig.shopifyStorefrontToken;

export async function getAllProducts(): Promise<Product[]> {
  if (!USE_LIVE_API) {
    console.log('[Products] Using mock data (no Shopify token configured)');
    return mockProducts;
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
              products(first: 50, sortKey: TITLE) {
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
      // Use local transparent PNGs instead of Shopify CDN
      const localImages = getProductImages(edge.node.handle);
      
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

    // Custom sort order: Cave Tangi items first, then Hammond PE, Tornadoes, posters (with split Greetings sizes), Retro Sketch
    const sortOrder = [
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
    ];

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
    console.error('[Products] Failed to fetch from Shopify, falling back to mock data:', error);
    return mockProducts;
  }
}

export async function getProductByHandle(handle: string): Promise<Product | null> {
  const products = await getAllProducts();
  return products.find(p => p.handle === handle) || null;
}
