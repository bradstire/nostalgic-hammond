import Client from 'shopify-buy';

// Shopify client singleton
let shopifyClient: any = null;

export function getShopifyClient() {
  if (!shopifyClient) {
    shopifyClient = Client.buildClient({
      domain: 'nostalgic-towns.myshopify.com',
      storefrontAccessToken: '26b7dcdc20879364ff735fbc45846857',
    });
  }
  return shopifyClient;
}

export interface ShopifyLineItem {
  id: string;
  title: string;
  variant: {
    id: string;
    title: string;
    price: {
      amount: string;
      currencyCode: string;
    };
    image?: {
      src: string;
    };
  };
  quantity: number;
}

export interface ShopifyCheckout {
  id: string;
  webUrl: string;
  lineItems: ShopifyLineItem[];
  subtotalPrice: {
    amount: string;
    currencyCode: string;
  };
  totalPrice: {
    amount: string;
    currencyCode: string;
  };
}

// Create or retrieve checkout from localStorage
export async function getOrCreateCheckout(): Promise<ShopifyCheckout> {
  const client = getShopifyClient();
  const existingCheckoutId = localStorage.getItem('shopify_checkout_id');

  if (existingCheckoutId) {
    try {
      const checkout = await client.checkout.fetch(existingCheckoutId);
      if (checkout && !checkout.completedAt) {
        return checkout as ShopifyCheckout;
      }
    } catch (error) {
      console.error('[Shopify] Failed to fetch existing checkout:', error);
      localStorage.removeItem('shopify_checkout_id');
    }
  }

  // Create new checkout
  const checkout = await client.checkout.create();
  localStorage.setItem('shopify_checkout_id', checkout.id);
  return checkout as ShopifyCheckout;
}

// Add item to checkout
export async function addToCheckout(variantId: string, quantity: number = 1): Promise<ShopifyCheckout> {
  const client = getShopifyClient();
  const checkout = await getOrCreateCheckout();

  const lineItemsToAdd = [
    {
      variantId,
      quantity,
    },
  ];

  const updatedCheckout = await client.checkout.addLineItems(checkout.id, lineItemsToAdd);
  return updatedCheckout as ShopifyCheckout;
}

// Update line item quantity
export async function updateLineItem(lineItemId: string, quantity: number): Promise<ShopifyCheckout> {
  const client = getShopifyClient();
  const checkout = await getOrCreateCheckout();

  const lineItemsToUpdate = [
    {
      id: lineItemId,
      quantity,
    },
  ];

  const updatedCheckout = await client.checkout.updateLineItems(checkout.id, lineItemsToUpdate);
  return updatedCheckout as ShopifyCheckout;
}

// Remove line item
export async function removeLineItem(lineItemId: string): Promise<ShopifyCheckout> {
  const client = getShopifyClient();
  const checkout = await getOrCreateCheckout();

  const lineItemIdsToRemove = [lineItemId];
  const updatedCheckout = await client.checkout.removeLineItems(checkout.id, lineItemIdsToRemove);
  return updatedCheckout as ShopifyCheckout;
}

// Normalize title for comparison (handles em dashes, multiplication signs, etc.)
function normalizeTitle(title: string): string {
  return title
    .toLowerCase()
    .replace(/[—–−]/g, '-')           // Em dash, en dash, minus → hyphen
    .replace(/×/g, 'x')                // Multiplication sign → x
    .replace(/\s+/g, ' ')              // Normalize whitespace
    .trim();
}

// Find product by title (for matching with our product pages)
export async function findProductByTitle(title: string): Promise<any> {
  const client = getShopifyClient();
  
  // Fetch all products (Shopify Buy SDK doesn't have a direct search by title)
  const products = await client.product.fetchAll();
  
  const normalizedSearchTitle = normalizeTitle(title);
  
  // Find product with matching title
  const product = products.find((p: any) => 
    normalizeTitle(p.title) === normalizedSearchTitle
  );

  if (!product) {
    console.warn('[Shopify] No product found matching title:', title);
    console.log('[Shopify] Searched for (normalized):', normalizedSearchTitle);
  }

  return product || null;
}
