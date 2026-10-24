// Route params for the original (Hammond) storefront.
import { getAllProducts } from '../../lib/products';
import { town } from '../../config/site.config';

export async function productPaths() {
  const products = await getAllProducts();
  return products.map((product) => ({ params: { handle: product.handle }, props: { product } }));
}
export async function collectionPaths() {
  return town.collections.map((c: any) => ({ params: { collection: c.slug }, props: { c } }));
}
export async function placePaths() {
  return [] as { params: { slug: string }; props: Record<string, unknown> }[];
}
