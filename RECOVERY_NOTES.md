# Nostalgic Hammond storefront — recovery from Vercel (2026-10-17, HQ)
Source: Vercel project brad-stires-projects/nostalgic-hammond, production deployment HSdTuSze3DeVkAik8L8Bh61b9t1D (Feb 5 2026, `vercel deploy` CLI, current production).
Method: Vercel dashboard file API (read-only, cookie-authenticated in the built-in browser) for text files; live site www.nostalgichammond.com for public images. Every file verified by SHA-1 against the deployment manifest (Vercel file ids are SHA-1 of content).
Recovered and verified: 40 text/source files + 233 public assets = 273/273. No `.git` (CLI deploys do not upload history) — history, if any, lives only on the original build host (see DISPATCH-N3).
Deliberately not copied: `dist/` (258 build outputs, regenerable with `npm run build`), `.astro/` (6 cache files), `tmp_product_images/` (69 raw renders; the 12 artwork files and the tee/hat renders are byte-identical to `public/images/originals/*` except `individual/black_5.png`, 2.3 MB, still on Vercel).
Secrets: none. Only the intentionally public Storefront token in `src/lib/shopify.ts`. `.env` was not part of the upload.
Copies: full tree (227 MB) in HQ's container at /home/claude/nh-recovered/nostalgic-hammond; source zip + MANIFEST.sha1 uploaded to Drive HQ/nostalgic-hammond-recovered/. Images re-fetchable from the live site and verifiable against MANIFEST.sha1.
