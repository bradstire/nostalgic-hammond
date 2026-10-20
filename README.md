# Print files (not part of the storefront build)

Print-ready files for Printful products. Sources are public-domain postcards.

## hattiesburg/
- `hattiesburg_greetings_pansy_12x18.jpg`: 2400×3600 (12×18 in at 200 dpi). "Greetings from Hattiesburg, Miss.", early 1900s.
  Source: Mississippi Department of Archives and History, Cooper Postcard Collection, PI/1992.0001, system ID 90128 ("no known copyright restrictions" on MDAH's Flickr Commons upload).
- `hattiesburg_main_street_18x12.jpg`: 3600×2400 (18×12 in at 200 dpi). "Main Street, Hattiesburg, Miss.", c. 1915–20 white-border card.
  Source: MDAH Cooper Postcard Collection, PI/1992.0001, system ID 90199 (same terms).

Processing: stitched from MDAH's full-resolution zoom tiles, run through the automated retouch layer (`src/retouch_postcard.py`: dust/foxing despeckle only — type, halftone, postmarks and creases untouched), trimmed to the card edge, and fitted to the frame ratio (the pansy card gets a few percent of matching paper on each side).

Scaling: both cards are ~173 dpi native at the launch sizes (12×18 / 18×12) — above Printful's 150 dpi floor. Larger sizes (18×24, 24×36) need the script's `--sr` EDSR 2× pass (CPU-slow; run as a batch job) or Brad's Photoshop Super Resolution.
- `hattiesburg_pe_front.png`: 3150×1224 transparent PNG at 300 dpi (10.5 in wide), DTG-compliant (binary alpha, uniform ink). Color #3A1055 Dark Plum from the production color bank — Hattiesburg High's colors are purple and gold (documented to the 1924 state-title run), dominant color purple. Chest print for the Hattiesburg Physical Ed. ringer tee.
  Fonts: Graduate (OFL) and Oswald (OFL), Google Fonts. Generator: `src/hattiesburg_pe.py`.
  Per-school protocol: one shirt per verified school, in that school's dominant color, one school color per product (anti-signal-stack rule from NOSTALGIC_PRINT_PRODUCTION.md on Drive).
