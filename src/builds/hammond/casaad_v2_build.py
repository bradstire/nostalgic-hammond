"""Casa de Fresa Dixie Home ad v2 (HQ 2026-10-25, S9). Changes from v1: small copy crisp (no roughen) in Schola Bold
at 1.4x the ad, re-set in TeX Gyre Bonum Bold (Bookman; Century hairlines fail the print floor)'s sizes (at the 9.5 in print v1's Schola Regular hairlines were ~0.006 in, under Printful's 0.015 in
minimum); traced headline re-set in League Spartan 800 fitted to the traced line; outer frame rule 0.02 in.
v1 notes: Casa de Fresa Hotel - the hotel's own listing ad ("Your Dixie Home", IMG_7169) rebuilt as a print. Pipeline B:
Real-ESRGAN x4plus -> the headline CASA de FRESA, Hammond, La. traced (the ad's own bold grotesque); the small copy, which
the newsprint scan has broken up, re-typeset in TeX Gyre Schola (GUST, Century-family roman/bold/bold italic) at the ad's
measured sizes and positions; the hotel photo re-screened as a round-dot halftone; frame redrawn as clean double rule.
Left off: the bottom line naming the manager and the chief clerk (private people)."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from hmlib import remove_small, fill_small_holes, build_multi
from newsprint import render_text, halftone, roughen
from PIL import Image
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/casaad"
INK = (36, 33, 31)
im = cv2.imread(f"{D}/c7169_x4.png").astype(np.float32); g = im.mean(2)
bg = cv2.GaussianBlur(g, (0, 0), 40)
soft = cv2.GaussianBlur(np.clip((bg - g - 40) / 60.0, 0, 1), (0, 0), 1.8)
ink = remove_small(soft > 0.5, 200)
# ---- headline (traced) ----
hb = ink[110:370, 300:4250].copy()
n, lab, st, _ = cv2.connectedComponentsWithStats(hb.astype(np.uint8), 8)
head = np.zeros_like(hb)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if h > 40 and w < 900 and y + h < 255: head[lab == i] = True        # letters + commas/periods; not the frame
head = fill_small_holes(head, 200)
ys, xs = np.where(head); HEAD_Y0, HEAD_X0 = 110 + ys.min(), 300 + xs.min()
head = head[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
# ---- small copy (re-typeset) ----
def cap_of(font, axes=None):
    a, (x0, y0, x1, y1) = render_text("H", font, 400, axes); return y1 - y0

def line(text, font, cap, tr=0.0):
    a, (x0, y0, x1, y1) = render_text(text, font, 400, None, tr); a = a[y0:y1, x0:x1]
    s = cap / cap_of(font); a = cv2.resize(a, (max(1, int(a.shape[1] * s)), max(1, int(a.shape[0] * s))), interpolation=cv2.INTER_AREA)
    m = np.pad(a, 10) > 0.5                                                # v2: crisp, straight from the font (S9)
    ys, xs = np.where(m); return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
R, B, BI = "texgyrebonum-bold.otf", "texgyrebonum-bold.otf", "texgyrebonum-bolditalic.otf"   # v2: Bookman Bold (low contrast): Century's hairlines fall under 0.015 in at ad sizes
K = 1.4                                                                    # v2: small copy 1.4x for legibility on a shirt
import os
if not os.path.exists("/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts/" + R): R = B
W0, H0 = 4520, 1760
c = np.zeros((H0, W0), bool)
def put(m, cx, ytop):
    x = int(cx - m.shape[1] / 2); c[ytop:ytop + m.shape[0], x:x + m.shape[1]] |= m
def put_base(m, cx, ybase, desc=0):
    put(m, cx, int(ybase - m.shape[0] + desc))
# v2: traced headline re-set in League Spartan 800, fitted to the traced line's cap height and width
_hl, _hn = __import__('scipy.ndimage', fromlist=['label']).label(head)
_C = max(__import__('scipy.ndimage', fromlist=['find_objects']).find_objects(_hl), key=lambda s: s[0].stop - s[0].start)
_cap = _C[0].stop - _C[0].start
_a, (_x0, _y0, _x1, _y1) = render_text("CASA de FRESA, Hammond, La.", "LeagueSpartan[wght].ttf", 400, {"wght": 800}, 0.02)
_a = _a[_y0:_y1, _x0:_x1]; _capr = cap_of("LeagueSpartan[wght].ttf", {"wght": 800})
_s = _cap / _capr
_a = cv2.resize(_a, (int(_a.shape[1] * _s), int(_a.shape[0] * _s)), interpolation=cv2.INTER_AREA)
_sx = min(max(head.shape[1] / _a.shape[1], 0.9), 1.1)
_a = cv2.resize(_a, (int(_a.shape[1] * _sx), _a.shape[0]), interpolation=cv2.INTER_AREA) > 0.5
_cx = HEAD_X0 + head.shape[1] / 2
put(_a, _cx, HEAD_Y0)
HEAD_BOX = (int(_cx - _a.shape[1] / 2), HEAD_Y0, int(_cx + _a.shape[1] / 2), HEAD_Y0 + _a.shape[0])
put(line("On U. S. Highways Nos. 51 and 190", B, 50 * K, 0.03), 2262, 366)
LX, RX = 700, 3800
for t, y in (("“Your", 590), ("Dixie", 726), ("Home”", 862)): put(line(t, BI, 64 * K, 0.07), LX + (8 if t != "Dixie" else 0), y)
for t, y in (("Rates:", 575), ("$3.00", 708), ("up", 870)): put(line(t, B, (62 if t != "$3.00" else 84) * K, 0.03), RX, y + {"up": 34, "$3.00": -10}.get(t, 0))   # v2: larger copy needs the stack opened (up was fusing with the period)
yy, xx = np.mgrid[:H0, :W0]
for cx in (LX, RX): c |= (xx - cx) ** 2 + (yy - 1080) ** 2 <= 33 ** 2         # the round bullets
for t, y in (("Excellent", 1165), ("Dining Room", 1280)): put(line(t, R, 50 * K, 0.03), LX, y)
for t, y in (("Free Parking", 1150), ("on Premises", 1280)): put(line(t, R, 50 * K, 0.03), RX, y)
put(line("FIREPROOF   –  –   STEAM HEAT   –  –   AIR COOLED", R, 62 * 1.35, 0.04), 2262, 1448)
put(line("AIR CONDITIONED ROOMS AVAILABLE", R, 62 * 1.35, 0.05), 2262, 1572)
# ---- photo, re-screened ----
px0, py0, px1, py1 = 1208, 491, 3320, 1421
ph = g[py0 + 8:py1 - 8, px0 + 8:px1 - 8] / 255.0
lo, hi = np.percentile(ph, 1.5), np.percentile(ph, 99.0)
gg = cv2.GaussianBlur(np.clip((ph - lo) / (hi - lo), 0, 1), (0, 0), 1.0)
dots = halftone(gg, cell=11.0, angle=45, gamma=1.05)
c[py0 + 8:py1 - 8, px0 + 8:px1 - 8] |= dots
cc = c.astype(np.uint8)
cv2.rectangle(cc, (px0, py0), (px1, py1), 1, 9)                            # photo keyline
# ---- frame: thin outer + heavier inner rule, as printed ----
cv2.rectangle(cc, (60, 20), (W0 - 60, H0 - 20), 1, 10)                     # v2: 0.02 in at 9.5 in (v1: 7 px)
cv2.rectangle(cc, (92, 52), (W0 - 92, H0 - 52), 1, 12)
c = cc > 0
# raster master (the halftone is thousands of dots - a vector trace adds nothing), 10 in wide @300 dpi
sys.path.insert(0, "/home/claude/nh-recovered/print-assets-repo/toolkit")
from vec import widen_gaps
s_ = 3000 / W0; cs = cv2.resize(c.astype(np.float32), (3000, int(H0 * s_)), interpolation=cv2.INTER_AREA) > 0.5
cs = widen_gaps(cs, 3000 / 9.5)                                             # v2: near-touching pairs opened (9.5 in print)
from vec import open_counters
_photo = np.zeros_like(cs); _photo[int(491 * s_) - 4:int(1421 * s_) + 4, int(1208 * s_) - 4:int(3320 * s_) + 4] = True
cs = (open_counters(cs & ~_photo, 3000 / 9.5) & ~_photo) | (cs & _photo)  # v2: small Bookman eyes opened to 0.026 in (print prep)

rgba = np.zeros((*cs.shape, 4), np.uint8); rgba[cs, :3] = INK; rgba[cs, 3] = 255
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{D}/casa_ad_dixiehome_v2.png"
Image.fromarray(rgba, "RGBA").save(OUT, dpi=(300, 300))
import json
json.dump({"typeset": [[[0, 0, 3000, int(H0 * s_)], "League Spartan 800 headline + TeX Gyre Bonum Bold / Bold Italic small copy (all set type)"]], "exempt": []},
          open(os.path.splitext(OUT)[0] + ".prov.json", "w"), indent=1)
print(c.shape)
