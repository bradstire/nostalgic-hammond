# Hattiesburg — wave 2 art (HQ, 2026-10-21)

All PNGs: 300 dpi, sRGB, **binary alpha** (no semi-transparent pixels), transparent background. Widths ~10–10.5 in unless noted.
Pipeline + build scripts: `src/newsprint/` (`newsprint.py`, `teemock.py`, `resr_ncnn.py`, `builds/`). Mock sheets: `mocks/`.

| File(s) | Design | Garment intent | Notes |
|---|---|---|---|
| `../hubcity_ad_front.png` | Hub City Drag Raceway, 1966 ad (v2) | White tee, black ink | Large type = Real-ESRGAN restoration; small copy re-typeset in Jost (Futura match) from verbatim transcription (incl. original "Facon" typo); photos re-screened 8px halftone. 10.5 × 11.1 in |
| `britches_{logo,hours,cloverleaf}_{white,cream}.png` | Mississippi Britches logotype (1987) | Burgundy family (maroon/cardinal/burgundy/brick) | Inter 580, tight tracking = the original's Helvetica Medium. `hours` = faithful store-hours line; `cloverleaf` = "CLOVERLEAF MALL · HATTIESBURG, MISS." |
| `camelot_hattiesburg_{flat,raised,flat_logo_only}_{white,black,gold}.png` | Camelot Music, Cloverleaf Mall, est. 1974 | Black / natural / navy | Grenze Gotisch (textura) at 0.86 width = the 1974 sign. `raised` = single-color raised-letter effect (12 px knockout gap). **Pending Brad's IP call (RetroBrands petition)** |
| `culpepper_full_{black,white}.png` | Culpepper Body & Paint Shop, 1968 ad — faithful | White / natural / black | Includes owner's personal name line + phone 545-7785 |
| `culpepper_houserule_{black,white}.png` | Same, house-rule cut | White / natural / black | Owner-name lines and phone removed |
| `culpepper_duck_hat_embroidery.{png,svg}` | Duck mascot, embroidery test | Khaki/stone dad hat, black thread | 1.38 × 1.82 in; strokes ≥ ~1.2 mm, holes < 1 mm² filled, potrace-smoothed. Test file — sample before listing |
| `speeds_sign_front_{cream,black}loc.png` | Albert Speed's Restaurant sign redraw | Black (cream locator) / natural or white (black locator) | Flat red/cream/green vector-style art; "304 BROADWAY DR. · HATTIESBURG, MISS. · 1966". **Mr. Peanut-like top-hat panel excluded** |
| `speeds_pylon_full.png` | Full pylon stack (Fresh Sea Food / main sign / Parking / Steaks) | Natural / black / forest; back print | 9 × 14 in |
| `sacks_front_{black,white,cream}.png`, `sacks_storefront.svg` | Sack's Army Store, 1980 ad | Natural (black) / olive drab (cream) / black (white) | Storefront line art vector-smoothed; subline + bottom block re-typeset. **VISA/Master Charge logos, phone and hours removed** |
| `hhs_v2_{H_physed,H_hattiesburg_physed,H_only_leftchest}_{purple,gold}.png`, `hhs_oldenglish_H_s9.svg` | **v2 (10-21):** the actual 1983 jersey letter, an Old English capital H reconstructed from 7 registered views in the original team photo (fused, traced, wrinkle-cleaned) | Natural ringer (purple); black tee (gold) | v1 stock-font set removed (Brad: felt like guesswork). Current HHS marks are a tiger head ® and a block "H" (MHSAA plate), not this letter |

## Revision pass (10-21 afternoon)
| File(s) | Change |
|---|---|
| `camelot_v2_bag1974.png` | **Chain's own 1970s colors**: stacked inline blackletter in Camelot red (#C62832) inside royal-blue (#2E49B8) record-groove arcs, per the 1970s Camelot paper bag. Knight emblem not used |
| `camelot_v2_sign_red_{blue,white}.png` | 1974 Cloverleaf sign wordmark in chain red, locator line blue (light tees) or white (dark tees) |
| `camelot_v2_tristripe.png` | 1990s plastic-bag nod (yellow/cyan/red tri-stripe) for the millennial read |
| `britches_*_black.png` + `mocks/britches_colors_v2.jpg` | Maroon/cream approved; added navy (denim; it was a jeans store), wood-tan + black ink (1971 wooden nickel, 631 Main St.), black + white (1987 ad) |
| `culpepper_*` | Duck face redrawn on the exact 1968 silhouette: pie-cut eye (the white slit in the print), cap keyline, bill mouth line. Only one printing exists online (Kepper's 10-16 post = same ad). Hat file uses an eye-only face for embroidery |
| `speeds_*` | QA vs the 1966 photo: warmer brick red, rounded neon-channel lettering (Archivo) with depth shadow, pale yellow-green arrow, wide mustard tower + orange base + white legs (pylon) |
| `hats/hat_*.png` | Embroidery fronts, all within 4.0 × 2.0 in, text ≥ 0.25 in, est. min stroke ≥ 0.05 in: Hub City (authentic SR letters), Camelot stacked red/white, Britches stacked cream, Speed's 3-line red, HHS Old English H purple/gold, Culpepper duck. `concept_britches_nickel_badge_print.png` = print/patch idea, not embroidery |
| `socks/sock_*.png` | Printful sublimation socks, basic template 4.49 × 18.85 in @300dpi (full bleed): HHS gym sock, Camelot, Hub City, Speed's |
