const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const response = await fetch(
  'https://nostalgic-towns.myshopify.com/api/2024-01/graphql.json',
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Shopify-Storefront-Access-Token': '26b7dcdc20879364ff735fbc45846857',
    },
    body: JSON.stringify({
      query: `
        query {
          products(first: 50) {
            edges {
              node {
                handle
                title
                variants(first: 20) {
                  edges {
                    node {
                      title
                    }
                  }
                }
              }
            }
          }
        }
      `,
    }),
  }
);

const { data } = await response.json();
data.products.edges.forEach(edge => {
  console.log(`${edge.node.handle}:`);
  if (edge.node.handle === 'greetings-from-hammond') {
    edge.node.variants.edges.forEach(v => {
      const size = v.node.title;
      const normalized = size
        .replace(/[""″′]/g, '')
        .replace(/×/g, 'x')
        .toLowerCase()
        .trim();
      console.log(`  Variant: "${size}" → handle: greetings-from-hammond-${normalized}`);
    });
  }
});
