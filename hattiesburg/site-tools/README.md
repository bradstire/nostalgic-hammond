# Hattiesburg storefront v2: image tools (HQ, 2026-10-23)

- `make_hero.py [wide|stack]`: large-letter "Greetings from Hattiesburg" postcard. Writes `out/hero_<layout>.png` and `boxes_<layout>.json` (letter hotspots).
  - Sources are in `src/`: MDAH Cooper Postcard Collection scans, "no known copyright restrictions". The 89943 crop excludes the handwriting.
  - Art comes from `../wave2/` and `../hubcity_ad_front_v3.png`.
  - Rule: no cropped lettering inside a letter.
- `make_hero_assets.py`: writes the AVIF/WebP hero sizes, `og.jpg`, the place share JPGs and `src/v2/hero-boxes.json` in the site repo.
- `make_socks.py`: sock product images rendered upright from Printful mockups.
- Paths in the scripts point at HQ's container. Set `SP` to `src/` and `PA` to `..` to run them from here.
