// Client-side cart on the Shopify Storefront Cart API (no SDK).
const DOMAIN = 'nostalgic-towns.myshopify.com';
const TOKEN = '26b7dcdc20879364ff735fbc45846857';
const KEY = 'nt_hb_cart';

export type Line = { id: string; quantity: number; variantId: string; variantTitle: string; title: string; handle: string; image?: string; price: number };
export type Cart = { id: string; checkoutUrl: string; count: number; subtotal: number; lines: Line[] };

const CART_FIELDS = `id checkoutUrl totalQuantity cost { subtotalAmount { amount } }
  lines(first: 50) { nodes { id quantity merchandise { ... on ProductVariant { id title price { amount } image { url }
  product { title handle } } } } }`;

async function gql(query: string, variables: Record<string, unknown> = {}) {
  const r = await fetch(`https://${DOMAIN}/api/2025-01/graphql.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Shopify-Storefront-Access-Token': TOKEN },
    body: JSON.stringify({ query, variables }),
  });
  const j = await r.json();
  if (j.errors) throw new Error(j.errors[0]?.message || 'Cart error');
  return j.data;
}

function shape(c: any): Cart | null {
  if (!c) return null;
  return {
    id: c.id, checkoutUrl: c.checkoutUrl, count: c.totalQuantity,
    subtotal: parseFloat(c.cost.subtotalAmount.amount),
    lines: c.lines.nodes.map((l: any) => ({
      id: l.id, quantity: l.quantity, variantId: l.merchandise.id, variantTitle: l.merchandise.title,
      title: l.merchandise.product.title, handle: l.merchandise.product.handle,
      image: l.merchandise.image?.url, price: parseFloat(l.merchandise.price.amount),
    })),
  };
}

function storedId(): string | null { try { return localStorage.getItem(KEY); } catch { return null; } }
function store(id: string | null) { try { id ? localStorage.setItem(KEY, id) : localStorage.removeItem(KEY); } catch { /* private mode */ } }

export async function getCart(): Promise<Cart | null> {
  const id = storedId();
  if (!id) return null;
  try {
    const d = await gql(`query($id: ID!) { cart(id: $id) { ${CART_FIELDS} } }`, { id });
    if (!d.cart) { store(null); return null; }
    return shape(d.cart);
  } catch { return null; }
}

export async function addLines(lines: { merchandiseId: string; quantity: number }[]): Promise<Cart> {
  const id = storedId();
  if (id) {
    const d = await gql(`mutation($id: ID!, $lines: [CartLineInput!]!) { cartLinesAdd(cartId: $id, lines: $lines) { cart { ${CART_FIELDS} } userErrors { message } } }`, { id, lines });
    if (d.cartLinesAdd.cart) return shape(d.cartLinesAdd.cart)!;
    store(null);
  }
  // Town + first-touch source ride on the cart as attributes and land on the Shopify order
  // ("Additional details"), so every order can be mapped to its town and source. "hq" marks internal carts.
  const attributes = [{ key: 'town', value: String(import.meta.env.PUBLIC_TOWN || '') }];
  try {
    const src = sessionStorage.getItem('nt_src'); if (src) attributes.push({ key: 'source', value: src });
    if ((window as any).NT_HQ) attributes.push({ key: 'hq', value: '1' });
  } catch { /* storage blocked */ }
  const d = await gql(`mutation($input: CartInput!) { cartCreate(input: $input) { cart { ${CART_FIELDS} } userErrors { message } } }`,
    { input: { lines, attributes, buyerIdentity: { countryCode: 'US' } } });
  const c = shape(d.cartCreate.cart);
  if (!c) throw new Error(d.cartCreate.userErrors?.[0]?.message || 'Could not create cart');
  store(c.id);
  return c;
}

export async function updateLine(lineId: string, quantity: number): Promise<Cart | null> {
  const id = storedId(); if (!id) return null;
  const d = quantity > 0
    ? await gql(`mutation($id: ID!, $lines: [CartLineUpdateInput!]!) { cartLinesUpdate(cartId: $id, lines: $lines) { cart { ${CART_FIELDS} } } }`, { id, lines: [{ id: lineId, quantity }] })
    : await gql(`mutation($id: ID!, $ids: [ID!]!) { cartLinesRemove(cartId: $id, lineIds: $ids) { cart { ${CART_FIELDS} } } }`, { id, ids: [lineId] });
  return shape((d.cartLinesUpdate || d.cartLinesRemove).cart);
}
