// Route params for storefront v2.
import { getCatalog } from '../catalog';
import { PLACES } from '../data';

export async function productPaths() {
  const all = await getCatalog();
  return all.map((p) => ({ params: { handle: p.handle }, props: { p } }));
}
export async function collectionPaths() {
  return ['faq', 'shipping-returns', 'terms', 'shop', 'places', 'contact', '404'].map((page) => ({ params: { collection: page }, props: { page } }));
}
export async function placePaths() {
  return PLACES.map((pl) => ({ params: { slug: pl.slug }, props: { pl } }));
}
