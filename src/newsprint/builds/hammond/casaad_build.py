"""Casa de Fresa Hotel - the hotel's own listing ad ("Your Dixie Home", IMG_7169) rebuilt as a print. Pipeline B:
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
    m = roughen(np.pad(a, 10).astype(np.float32), 1.3, 0.12)              # letterpress edge, sits with the traced headline
    ys, xs = np.where(m); return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
R, B, BI = "texgyreschola-regular.otf", "texgyreschola-bold.otf", "texgyreschola-bolditalic.otf"
import os
if not os.path.exists("/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts/" + R): R = B
W0, H0 = 4520, 1760
c = np.zeros((H0, W0), bool)
def put(m, cx, ytop):
    x = int(cx - m.shape[1] / 2); c[ytop:ytop + m.shape[0], x:x + m.shape[1]] |= m
def put_base(m, cx, ybase, desc=0):
    put(m, cx, int(ybase - m.shape[0] + desc))
c[HEAD_Y0:HEAD_Y0 + head.shape[0], HEAD_X0:HEAD_X0 + head.shape[1]] |= head
put(line("On U. S. Highways Nos. 51 and 190", B, 50, 0.02), 2262, 370)
LX, RX = 700, 3800
for t, y in (("“Your", 590), ("Dixie", 726), ("Home”", 862)): put(line(t, BI, 64, 0.03), LX + (8 if t != "Dixie" else 0), y)
for t, y in (("Rates:", 575), ("$3.00", 708), ("up", 870)): put(line(t, B, 62 if t != "$3.00" else 84, 0.03), RX, y)
yy, xx = np.mgrid[:H0, :W0]
for cx in (LX, RX): c |= (xx - cx) ** 2 + (yy - 1080) ** 2 <= 33 ** 2         # the round bullets
for t, y in (("Excellent", 1200), ("Dining Room", 1290)): put(line(t, R, 50, 0.02), LX, y)
for t, y in (("Free Parking", 1185), ("on Premises", 1275)): put(line(t, R, 50, 0.02), RX, y)
put(line("FIREPROOF    –  –    STEAM HEAT    –  –    AIR COOLED", R, 62, 0.06), 2262, 1468)
put(line("AIR CONDITIONED ROOMS AVAILABLE", R, 62, 0.06), 2262, 1572)
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
cv2.rectangle(cc, (60, 20), (W0 - 60, H0 - 20), 1, 7)
cv2.rectangle(cc, (92, 52), (W0 - 92, H0 - 52), 1, 12)
c = cc > 0
# raster master (the halftone is thousands of dots - a vector trace adds nothing), 10 in wide @300 dpi
s_ = 3000 / W0; cs = cv2.resize(c.astype(np.float32), (3000, int(H0 * s_)), interpolation=cv2.INTER_AREA) > 0.5
rgba = np.zeros((*cs.shape, 4), np.uint8); rgba[cs, :3] = INK; rgba[cs, 3] = 255
Image.fromarray(rgba, "RGBA").save(f"{D}/casa_ad_dixiehome.png", dpi=(300, 300))
print(c.shape)
