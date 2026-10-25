"""Casa de Fresa strawberries back v2 (HQ 2026-10-25, S9). Changes from v1: (a) no roughen() on the re-set Caslon lines
(type straight from the font); (b) AIR CONDITIONED re-set in the same Libre Caslon (the traced line had a malformed A);
(c) the matchbook's own headline + HAMMOND, LA. keep their traced letters with corner-preserving smoothing.
The Caslon-italic slogan (passes the gate) is untouched. v1 notes follow.
Casa de Fresa — 'Down In The Land Of Strawberries' typographic print, from the matchbook's inside cover (IMG_7196).
Traced from the Real-ESRGAN x4 scan: headline, HAMMOND, LA., the Caslon-italic slogan (swash w), AIR CONDITIONED, bullet.
Re-typeset (Pipeline B, small copy partly under a fold/stain): COFFEE SHOP / AND / DINING ROOM / FIVE EFFICIENCY / APARTMENTS in Libre Caslon Text (OFL),
cap height and weight matched to the traced AIR CONDITIONED line."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
sys.path.insert(0, "/home/claude/nh-recovered/print-assets-repo/toolkit")
from vec import smooth_mask_corners, widen_gaps
from hmlib import remove_small, fill_small_holes, build_multi
from newsprint import render_text, roughen
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/casa"
GREEN, RED = (10, 104, 86), (206, 32, 46)
ink = cv2.imread(f"{D}/inside_ink.png", 0) < 128
ink = fill_small_holes(remove_small(ink, 900), 300)
# stray fleck above the d of "Land" (not part of the letter)
n, lab, st, _ = cv2.connectedComponentsWithStats(ink.astype(np.uint8), 8)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if 3600 < x < 3800 and 1150 < y < 1320 and a < 6000: ink[lab == i] = False
bands = [(143, 554), (667, 886), (1141, 1535), (1633, 2059), (2272, 2536), (2728, 2873)]
ANG = [1.13, 1.15, 1.0, 1.0, 0.65, 0.0]               # measured baseline tilt per line (photo ~1 deg off level); italics use 1.0
def band(y0, y1, ang):
    m = ink[y0 - 60:y1 + 60].astype(np.uint8) * 255
    h, w = m.shape; M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
    m = cv2.warpAffine(m, M, (w, h)) > 127
    ys, xs = np.where(m); return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
parts = [band(*b, a) for b, a in zip(bands, ANG)]
# v2: matchbook lettering (headline, HAMMOND, LA.) - traced letters kept, corner-preserving smoothing
from scipy import ndimage as _nd
def _clean(m, r, sig):
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; d = (xx ** 2 + yy ** 2) <= r * r
    m = _nd.binary_opening(_nd.binary_closing(m, structure=d), structure=d)   # notches / spurs out
    return smooth_mask_corners(m, sigma_px=sig, corner_deg=45)
parts[0] = _clean(parts[0], 6, 13)
parts[1] = _clean(parts[1], 5, 11)
cap = 227                                           # AIR CONDITIONED letter height after levelling (traced, median)
def typeset(text, tracking=0.035, wght=600):
    a, (x0, y0, x1, y1) = render_text(text, "LibreCaslonText[wght].ttf", 400, {"wght": wght}, tracking)
    a = a[y0:y1, x0:x1]
    s = cap / a.shape[0]; a = cv2.resize(a, (int(a.shape[1] * s), cap), interpolation=cv2.INTER_AREA)
    a = np.pad(a, 12)
    return a > 0.5                                                    # v2: crisp, straight from the font (no roughen, S9)
# v2: AIR CONDITIONED re-set in the same Caslon as the lines below (traced line had a malformed A)
air_w = parts[4].shape[1]
parts[4] = typeset("AIR CONDITIONED")
lines = [typeset("COFFEE SHOP"), typeset("AND"), typeset("DINING ROOM"),
         typeset("FIVE EFFICIENCY", tracking=0.06), typeset("APARTMENTS", tracking=0.06)]   # below the fold on the matchbook (IMG_7196)
# vertical rhythm: the original gaps; re-set lines spaced like AIR CONDITIONED -> bullet
gaps = [bands[i + 1][0] - bands[i][1] + 25 for i in range(len(bands) - 1)] + [190, 130, 130, 230, 130]
allp = parts + lines
W = max(p.shape[1] for p in allp) + 200; Hh = sum(p.shape[0] for p in allp) + sum(gaps) + 200
canvas = np.zeros((Hh, W), bool); y = 100
# original horizontal placement: lines are centred except the slogan, which keeps its hanging-quote indent
ref_cx = W // 2
offsets = {2: -60, 3: 120}                          # slogan line 1 starts with a hanging quote; line 2 indented (as printed)
for i, p in enumerate(allp):
    x = ref_cx - p.shape[1] // 2 + offsets.get(i, 0)
    canvas[y:y + p.shape[0], x:x + p.shape[1]] |= p
    y += p.shape[0] + (gaps[i] if i < len(gaps) else 0)
ys, xs = np.where(canvas); canvas = canvas[ys.min() - 40:ys.max() + 41, xs.min() - 40:xs.max() + 41]
H2, W2 = canvas.shape
canvas = widen_gaps(canvas, W2 / 10.0)              # v2: near-touching pairs opened to the gate's gap floor (10 in print)
import json as _j, os as _o
_j.dump({"typeset": [], "exempt": [[[0, 0, W2, int(0.07 * H2)], "hand-lettered matchbook headline CASA de FRESA HOTEL: traced, cleaned (close/open r6 + corner-preserving smoothing s13); irregular letter widths are the lettering's own"]]},
        open((sys.argv[1] if len(sys.argv) > 1 else f"{D}/casa_strawberries_v2") + "_green.prov.json", "w"), indent=1)
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{D}/casa_strawberries_v2"
build_multi([(canvas, GREEN)], W2, H2, 3000, OUT + "_green")       # 10 in wide
build_multi([(canvas, RED)], W2, H2, 3000, OUT + "_red")
print(W2, H2)
