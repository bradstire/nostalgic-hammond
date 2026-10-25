// Route params for storefront v2.
import { getCatalog } from '../catalog';
import { livePlaces } from '../data';

export async function productPaths() {
  const all = await getCatalog();
  return all.map((p) => ({ params: { handle: p.handle }, props: { p } }));
}
export async function collectionPaths() {
  return ['faq', 'shipping-returns', 'terms', 'shop', 'places', 'contact', '404'].map((page) => ({ params: { collection: page }, props: { page } }));
}
export async function placePaths() {
  // Only places with products get a page (towns with HIDE_EMPTY_PLACES); the rest appear once their products do.
  return livePlaces(await getCatalog()).map((pl) => ({ params: { slug: pl.slug }, props: { pl } }));
}
