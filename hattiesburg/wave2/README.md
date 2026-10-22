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

## Revision pass 2 (10-21, after Brad's 14:04 notes)
| File(s) | Change |
|---|---|
| `hhs_oldenglish_H_connected.svg` → all `hhs_v2_*`, `hats/hat_hhs_oldenglishH_*`, `socks/sock_hhs_gym_purple.png` | **Ear connectors forced** (Brad: "force that"). Left ear joined to the left stem by a tapered neck; right ear joined to the h body by a short arm, both stroke-matched to the letter (≈3% of height). The photo views don't show these joins clearly (wrinkle/shadow), so this is a design decision, not evidence. The letter is now 2 solid pieces: the spur stem and the h body, which are separate in the jersey letter too. `hhs_oldenglish_H_s9.svg` kept as the evidence-only trace |
| `hats/hat_culpepper_back_black.png` | **New back embroidery** for the Culpepper hat: arched CULPEPPER (0.32 in caps, 5.5 in radius) over straight BODY & PAINT (0.26 in caps), Jost Black (Futura family, like the ad headline). 2.86 × 0.89 in, inside Printful's back area (2.25–3.0 × 0.75–1.0 in); text ≥ 0.25 in; est. min stroke 0.053 in. Back instead of front because the duck fills the front's 1.8 in height; adding a line under it would shrink the restored face. "SHOP" dropped so the text stays ≥ 0.25 in within 3 in width. Mock: `mocks/culpepper_hat_front_back_mock.jpg` |
| `socks/sock_speeds.png` | Hyphen removed: RESTAU / RANT with matched letter heights, centered in the red panel. Alternate: `socks/sock_speeds_oneline.png` (RESTAURANT on one condensed line) |

## Revision pass 3 (10-22, Brad's notes) — current files
Specs re-verified from Printful's own templates (10-22): dad hat front **5.5 x 2.0 in**, side/back **2.0 x 1.0 in** (≤ 5 characters per inch), letters ≥ 0.25 in, details ≥ 0.05 in, **15 thread colours only**; socks = **separate FRONT and BACK files**, 1347 x 5657 px, keep marks inside the red safe box (2.73 in wide, front y 3.9–16.8 in on M; back = calf + sole boxes, heel between); DTG on white = no underbase, no stated minimums (Printful's DTF guidance: ≥ 1 pt lines, 10–12 pt text). Superseded files moved to `_superseded/` (nothing deleted).

| File(s) | What changed |
|---|---|
| `../hubcity_ad_front_v3.png` | **Use for the white tee.** v2 art + press compensation for DTG on cotton: smallest-copy strokes rebuilt to ≥ 1.5 pt; halftone minimum feature 0.01 in (highlight dots grown, shadow openings opened) so photos don't plug. Look unchanged. Proof: `mocks/hubcity_white_tee_press_check.jpg` (ink-spread simulation, v2 vs v3) |
| `camelot_v3_{bag1974,sign_red_blue,sign_red_white,tristripe}.{png,svg}` | Letterforms matched to the 1970s bag + 1974 Cloverleaf sign: Old English swash C (Manufacturing Consent, OFL) + Grenze Gotisch Black (OFL) at **natural width** (v2 was wrongly compressed). Bag construction rebuilt as **true vector offsets** (red fill / open channel / red keyline, mitred corners) — no raster rings. Groove arcs pass behind the lettering. SVG masters included. Mocks: `mocks/camelot_v3_mocks.jpg` |
| `hhs_v3_*`, `hhs_H_v3.svg` | **Real typeface letter.** Surveyed ~40 blackletter faces (Google OFL, Peter Wiegel OFL, 1001fonts FFC); Old English Text MT = Cloister Black design (looped H), not the jersey's. Closest usable match to the 1983 jersey H = **Manufacturing Consent capital H (OFL)** — same top flag, mid spur, sweeping foot — leaned to the jersey slant, clean vector. `mocks/hhs_H_v3_compare.png` (jersey / v2 / v3), `mocks/hhs_font_survey_*.png` |
| `culpepper_{full,houserule}_*`, `culpepper_duck_hat_embroidery.*` | Duck v3: more negative space — bill base line, collar V, sleeve line, armpit line, wrist cuff, glove fingers on the gun hand (traces in the original), cloud as clean outline. The 1968 print is solid black there (ink spread), so these are drawn in the ad's cartoon idiom. Hat weight: every cut ≥ 0.05 in, pie-cut eye, no fingers/cuff (too small to stitch). `mocks/culpepper_duck_v2_v3.jpg` |
| `hats/*` (all) | **Every file run through an embroidery checker** (medial-axis stroke width, stitch-merge test for gaps/counters, text height, cpi, size): letters re-spaced ≥ 0.06 in, thin strokes rebuilt to 0.05 in, counters opened, **exact Printful thread colours** (Red 1839 #CC3333, Purple 1832 #6B5294, Gold 1951 #FFCC00, White, Black). Britches now `hat_britches_white.png` (no cream thread exists). All PASS except the flagged alternate below |
| `hats/hat_culpepper_front_lockup_black.png` | **Culpepper text, primary:** duck + CULPEPPER / BODY & PAINT on the 5.5 in front (passes every check) |
| `hats/hat_culpepper_back_black.png` | Alternate: arched CULPEPPER on the 2 x 1 in back (1.96 in, 4.6 cpi, condensed gothic like the ad). **Flag:** at this size the P/R bowls (~0.04 in) will fill when stitched. "BODY & PAINT" can't fit the back at ≤ 5 cpi |
| `socks/sock_{hhs_gym_purple,camelot,hubcity,speeds}_{front,back}.png` | Re-laid to the real template: v2 art was 3.5–3.9 in wide (wrapped round the leg) and started inside the cuff zone. Marks now inside the S/M/L safe-box overlap; bands/background full-bleed; Camelot letters solid (inline can't survive knit stretch); Speed's = one-line RESTAURANT. QA: `mocks/socks_v3_template_check.jpg` |
| `../beverly_front_navy_v2.png` | Natural/navy layout: subline tucked under "Bever", clear of the y-descender (was 1 in of dead space). Teal + white black-tee versions unchanged (ready) |
| `src/newsprint/vtype.py`, `src/newsprint/embcheck.py`, `src/newsprint/builds/*_v3.py` | Vector-type helpers (font → polygons → mitred offsets → SVG/PNG) and the embroidery checker, reusable for every town |

Fonts used in art (outlines baked into the art, no font files shipped): Manufacturing Consent, Grenze Gotisch, Jost, Inter, Archivo, Oswald, Graduate (all SIL OFL); TeX Gyre Heros (GUST licence).
