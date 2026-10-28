# R21 cleanup budget: calibrated on Hattiesburg + Hammond v2 only (2026-10-28)

Brad 10-28 08:16: the threshold for how far a trace gets cleaned should come from Hattiesburg and Hammond v2 alone.

## What those two towns actually did to their traced lettering

| Town | Design | Lettering | Cleanup applied (from the build scripts / prov) | Smoothing as % of cap | Notch removal as % of cap |
|---|---|---|---|---|---|
| Hattiesburg | Hub City 1966 ad | HUB CITY DRAG RACEWAY, FORD vs. CHEVY | Real-ESRGAN x4 + threshold; press fix only on the halftone | 0 | 0 |
| Hattiesburg | Culpepper 1968 ad | CULPEPPER BODY & PAINT SHOP, 113 N. Tipton | SR + threshold; print specks left in (119 + 60) | 0 | 0 |
| Hattiesburg | Sack's 1980 ad | SACK'S ARMY STORE | SR + light threshold | 0 | 0 |
| Hattiesburg | Beverly Drive-In | Beverly script | traced, colour fix only | ~0 | 0 |
| Hammond v2 | Casa de Fresa mark | CASA de FRESA / hotel | close/open r5 + corner-preserving smoothing 0.04 in | 2.8 % (cap 430 px) | 1.2 % |
| Hammond v2 | Casa strawberries | headline / HAMMOND, LA. | close/open r6 / r5 + smoothing s13 / s11 | 3.2 % / 5.0 % | 1.5 % / 2.3 % |
| Hammond v2 | Toggery logo v3 | Toggery logotype | close/open r6 + smoothing s14; one decisive slant kept (Brad 10-25) | ~5 % | ~2 % |
| Hammond v2 | Galaxy pass | brush script | outline smoothing 0.008 in; levelled as one unit | ~2 % | 0 |
| Hammond v2 | Magnolia v5 | Magnolia script | pixel-staircase melt only; levelled as one unit | ~0.5 % | 0 |
| Hammond v2 | Fiesta Club v4 | FIESTA block | traced, irregular by design | ~0 | 0 |

## The budget (R21 rule 2)

- Notches and spurs: close/open at up to **~1.5 % of cap height** (ceiling 2.3 %).
- Edge smoothing: corner-preserving, **sigma ~3 % of cap height** (Hammond v2 median), ceiling 5 % (the most Hammond used). Hattiesburg's print-scan ads used 0 %: SR + threshold is also in budget.
- Geometry: global moves only. Perspective, rotation and one-unit levelling are capture fixes. Nothing moves letter by letter, no stroke-weight or width regularising. A slant the lettering itself carries is kept (Toggery ruling).
- Counters and gaps are opened only to the print floors.
- Object damage (broken letter, glare, missing face) may be repaired from the same letter's own geometry, such as a mirrored jaw. This must be declared.
- More than this is a redraw: it is declared `redrawn` and the reason is logged.

## Edge measurements (sfv2/calib/edge_metrics*.py, micro.py)

Neither edge roughness relative to stroke weight (3.8-6.6 % in the references, but 4.0 % on Oswald too) nor fine edge wobble separated a trace from a font outline. Potrace output is smooth at that scale either way. What does separate them is letterform irregularity and how often an edge changes direction:

| Inflections per inch of outline at print | Fonts (Oswald, Libre Caslon, Knewave) | Hattiesburg + Hammond v2 traces | SFV v2 traces |
|---|---|---|---|
| range | 2.1-4.2 | 3.4-10.3 (sign scripts 3.4-4.3; print 4.5-10.3) | 3.6-11.2 |

So the line is drawn on process: what the recipe may do to a trace. It is not drawn on an edge-texture number.

## SFV pass 2: smoothing per trace (all inside the budget)

| Trace | Mask cap | Smoothing sigma | % of cap | Notch removal |
|---|---|---|---|---|
| FM | ~350 px | 10 | 2.9 % | opening r5 (1.4 %) |
| GEMCO | 274 px | 8 | 2.9 % | close/open r4 (1.5 %) |
| PIZZA | ~222 px | 7 | 3.2 % | none |
| Don's lines | ~85 px | 2.5 | 2.9 % | none |
| Leon's pillow letters | ~95 px | 3 | 3.2 % | close/open r1 |
| Leon's COFFEE SHOP | ~62 px | 2 | 3.2 % | opening r3 |
| Valley Plaza | ~365 px | 6 | 1.6 % | channel clip |
| Encino BOWL | ~312 px | 9 | 2.9 % | opening r2 |
| ENCINO | ~110 px | 3 | 2.7 % | opening r2 |
| Coffee Shop | ~168 px | 5 | 3.0 % | opening r2 |
| Zodys | ~790 px | 10 | 1.3 % | opening r2 |
| Devonshire Downs | ~210 px | 5 | 2.4 % | close/open r3 |
| Moby arc / tagline | ~640 / ~200 px | 3 | 0.5-1.5 % | specks only |
| Mike's script, Don's logo, Sasch, Jolly Roger, Fantasy Faire, Sugar Shack | | none | 0 % (SR + threshold + print-clean, the Hattiesburg way) | specks only |
