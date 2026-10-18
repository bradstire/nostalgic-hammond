# Add to Cart Fix - Test Plan

**Date**: February 3, 2026  
**Issue**: Framed poster add-to-cart buttons failing due to data-product-title mismatch  
**Fix**: Added `shopifyProductTitle` field to map per-size pages to master Shopify products

---

## Changes Made

### 1. Product Interface (`src/data/mockProducts.ts`)
- Added optional `shopifyProductTitle?: string` field to Product interface
- Allows mapping frontend product pages to their actual Shopify product names

### 2. Mock Product Data
Updated the following products with `shopifyProductTitle` field:
- `greetings-from-hammond-8x10` → "Greetings from Hammond - Framed Poster"
- `greetings-from-hammond-11x14` → "Greetings from Hammond - Framed Poster"
- `greetings-from-hammond-16x20` → "Greetings from Hammond - Framed Poster"
- `strawberry-stadium-framed-poster` → "Strawberry Stadium - Framed Poster"

### 3. Product Page Template (`src/pages/products/[handle].astro`)
- Changed: `data-product-title={product.title}`
- To: `data-product-title={product.shopifyProductTitle || product.title}`
- Falls back to regular title for non-framed poster products

### 4. Shopify Query Logic (`src/lib/shopify.ts`)
- Added `normalizeTitle()` function to handle special characters:
  - Em dash (—), en dash (–), minus (−) → hyphen (-)
  - Multiplication sign (×) → x
  - Normalizes whitespace
- Updated `findProductByTitle()` to use normalized comparison
- Added debug logging when product not found

---

## Testing Checklist

### Pre-Deployment (Local Build ✅)
- [x] Build completes without errors (`npm run build`)
- [x] All 12 products generate static pages
- [x] data-product-title correctly set for all framed posters:
  - [x] greetings-from-hammond-8x10 → "Greetings from Hammond - Framed Poster"
  - [x] greetings-from-hammond-11x14 → "Greetings from Hammond - Framed Poster"
  - [x] greetings-from-hammond-16x20 → "Greetings from Hammond - Framed Poster"
  - [x] strawberry-stadium-framed-poster → "Strawberry Stadium - Framed Poster"

### Post-Deployment (Production)

#### For Each Framed Poster Product Page:
Test all four products:
1. `/products/greetings-from-hammond-8x10`
2. `/products/greetings-from-hammond-11x14`
3. `/products/greetings-from-hammond-16x20`
4. `/products/strawberry-stadium-framed-poster`

**For each page:**

**1. Variant Dropdown Population**
- [ ] Open page, check browser console (F12)
- [ ] Look for: `[Product] Found matching Shopify product: <product-name>`
- [ ] Variant select dropdown should populate with Shopify variant IDs
- [ ] Example: `gid://shopify/ProductVariant/45678901234567` (not "8x10", "11x14", etc.)

**2. Add to Cart Functionality**
- [ ] Select a size from dropdown
- [ ] Click "Add to Cart" button
- [ ] Button should show "Adding..." then "Added!"
- [ ] Cart drawer should open
- [ ] Product should appear in cart with:
  - Correct image
  - Correct title + size variant
  - Correct price

**3. Checkout Flow**
- [ ] Add multiple variants to cart (e.g., 8x10 + 11x14 of same poster)
- [ ] Verify cart shows both items separately
- [ ] Click "Checkout" button
- [ ] Should redirect to Shopify checkout
- [ ] Verify correct products and quantities in Shopify checkout

**4. Browser Console Check**
- [ ] No JavaScript errors
- [ ] No failed API calls
- [ ] Shopify product query succeeds

---

## Expected Console Output

When a framed poster page loads successfully, you should see:

```
[Product] Found matching Shopify product: Greetings from Hammond - Framed Poster
```

If the product is NOT found, you'll see:
```
[Shopify] No product found matching title: Greetings from Hammond - Framed Poster
[Shopify] Searched for (normalized): greetings from hammond - framed poster
```

---

## Rollback Plan

If issues occur after deployment:

**Option 1: Revert Commit**
```bash
cd ~/nostalgic-hammond
git log --oneline -5  # Find commit before the fix
git revert <commit-hash>
git push origin main
```

**Option 2: Quick Fix**
If only the shopifyProductTitle needs adjustment:
```bash
# Edit src/data/mockProducts.ts
# Change shopifyProductTitle to match exact Shopify product name
npm run build
npx vercel --prod
```

---

## Deployment Command

```bash
cd ~/nostalgic-hammond
npx vercel --prod
```

Or via Vercel dashboard (auto-deploys on git push if connected).

---

## Notes

- This fix assumes Shopify products are published to the "Nostalgic Towns Headless" storefront channel
- Variant IDs must match between Shopify and the frontend
- Test with real Shopify checkout to verify payment flow
- Monitor console for any 404s or API errors

---

## Success Criteria

✅ All framed poster pages successfully query Shopify  
✅ Variant dropdowns populate with real Shopify variant IDs  
✅ Add to cart succeeds for all size variants  
✅ Cart displays correct product info  
✅ Checkout redirects to Shopify with correct items  
✅ No JavaScript errors in browser console  

---

**Tester**: _____________  
**Date Tested**: _____________  
**Status**: ❌ Not Tested | ⚠️ Issues Found | ✅ Passed
