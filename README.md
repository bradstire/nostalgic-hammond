# Nostalgic Hammond

Hammond, Louisiana nostalgia apparel and prints.

## Project Status

**Phase 1: COMPLETE ✅**
- Full site built with mock product data
- All pages functional (home, product detail, about, cart)
- Cart system working with localStorage
- Responsive design (mobile-first)
- Ready for Vercel deployment

**Phase 2: To Do (Human)**
- Purchase domain: NostalgicHammond.com
- Create Shopify store + install Printful
- Add Shopify Storefront API token to environment
- Point domain DNS to Vercel

## Tech Stack

- **Framework**: Astro (static site generation)
- **Styling**: Tailwind CSS with custom theme
- **Commerce**: Shopify Storefront API + Buy SDK (Phase 2)
- **Deployment**: Vercel

## Local Development

```bash
npm install
npm run dev
```

Site will be available at `http://localhost:4321`

## Build

```bash
npm run build
```

Output in `dist/` directory.

## Deployment to Vercel

### Option 1: Vercel CLI (if authenticated)

```bash
npx vercel --prod
```

### Option 2: GitHub + Vercel Dashboard

1. Push to GitHub:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/nostalgic-hammond.git
   git branch -M main
   git push -u origin main
   ```

2. Connect repository in Vercel dashboard:
   - Go to https://vercel.com/new
   - Import repository
   - Framework preset: Astro
   - Deploy

### Option 3: Direct Upload

```bash
npx vercel --prod --yes
```

## Environment Variables

For Phase 2 (live Shopify), add these to Vercel:

```
SHOPIFY_STOREFRONT_TOKEN=your_token_here
SHOPIFY_STORE_DOMAIN=nostalgic-hammond.myshopify.com
```

## File Structure

```
src/
├── components/
│   ├── Header.astro         # Navigation + cart icon
│   ├── Footer.astro         # Site footer
│   ├── ProductCard.astro    # Product grid item
│   └── CartDrawer.astro     # Cart overlay
├── layouts/
│   └── Layout.astro         # Base layout
├── pages/
│   ├── index.astro          # Homepage (product grid)
│   ├── about.astro          # About page
│   └── products/[handle].astro  # Product detail pages
├── config/
│   └── site.config.ts       # Site-wide config
├── data/
│   └── mockProducts.ts      # Mock product data
├── lib/
│   └── products.ts          # Product data layer (mock/live switching)
└── styles/
    └── global.css           # Global styles + Tailwind
```

## Product Data Switching

The site automatically uses mock data when `SHOPIFY_STOREFRONT_TOKEN` is not set.

To switch to live Shopify data:
1. Add Storefront API token to environment variables
2. Rebuild/redeploy

No code changes needed.

## Mock Products

Current catalog (12 products):
- Cave Tangi Tees (3 colors)
- Cave Tangi Dad Hats (3 colors)
- Hammond Phys Ed Ringer Tee
- Tornadoes Crew Neck Sweatshirt
- Strawberry Stadium Framed Poster
- Greetings from Hammond Prints (3 sizes)

## Design System

**Colors:**
- Charcoal: #1E1E1C
- Cream: #F5F0E6
- Rust: #B5533E
- Aged Gold: #C4A35A
- Warm White: #FAF8F3
- Warm Black: #2C2A26

**Typography:**
- Display: Playfair Display (product names, titles)
- Body: Source Serif 4 (descriptions, about page)
- Utility: Barlow Condensed (nav, buttons, prices)

## Cart Behavior

- LocalStorage-based cart
- Add/remove items, update quantities
- Subtotal calculation
- Free shipping callout ($75 threshold)
- "Checkout" button shows Phase 1 alert (Phase 2: redirects to Shopify)

## Next Steps

1. **Deploy to Vercel** (generates temporary URL)
2. **Test on mobile** (expect 70-80% mobile traffic)
3. **Purchase domain** (NostalgicHammond.com)
4. **Set up Shopify**:
   - Create store ($39/mo Basic plan)
   - Install Printful app
   - Sync products from pricing model
   - Create Storefront API access token
5. **Add environment variables** to Vercel
6. **Point domain** to Vercel
7. **Test checkout** flow
8. **Launch ads**

## Budget Spent

- Build cost: ~$0.50 (well under $5 budget)
- Remaining: $4.50 for debugging/polish if needed

## Template Notes

This is a template architecture. To launch a new city:
1. Fork repo
2. Edit `src/config/site.config.ts` (8 lines)
3. Swap `src/data/mockProducts.ts`
4. Deploy

**Never mention template/expansion plans in customer-facing content.**
