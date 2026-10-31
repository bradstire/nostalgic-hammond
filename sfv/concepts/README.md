# SFV concepts (HQ, 2026-10-31) — not published

Pulled from Facebook archive posts (Valley Relics Museum) during Brad's 10-31 overnight QA.

| Concept | Master | Source | Status |
|---|---|---|---|
| Biff's Restaurants (menu cover) | `sfv_biffs_concept.png` 10.7 x 11.8 in, cream/yellow/red, for B+C 3001 Forest | `src/biffs_44.jpg` (menu cover, VRM post) | S9 FAIL (hairlines, tight gaps in the stippled ground): production pass needed |
| Builders Emporium (1961 brochure) | `sfv_builders_emporium_concept.png` 7.4 x 13.1 in, cream/dark brown, for B+C 3001 Teal | `src/be_42.jpg` (brochure), `src/be_41.jpg` (storefront) | S9 FAIL (tail crosshatch, BUILDERS edges): production pass needed |
| Darby's Coffee Shop | — | `src/darbys_27.jpg` | candidate; source too small to trace |

Builds: `src/builds/sfv/concepts/` (`*_sep.py` = x4 Real-ESRGAN output → colour separation; `*_master.py` = print-clean, hairline-gap fill, 300 dpi master). The x4 upscales are regenerated with `src/newsprint/resr_ncnn.py <in> <out> realesrgan-x4plus`.
June Ellen's v2 sources (`src/je_5.jpg` contact sheet, `src/je_7.jpg` 'Donuts' frame) are kept here too; the v2 build is `src/builds/sfv/june_ellens_v2.py`.
