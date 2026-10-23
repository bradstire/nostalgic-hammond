"""Didi-Wa Restaurant (Hammond, La.; Southern fried chicken; sepia photo, c. 1940s-50s) — the roadside sign as a print.
Pipeline B: Real-ESRGAN x4 of the sign (IMG_7174) -> perspective rectified (4 points on the top/bottom edges) ->
letters traced (the sign's own painted letters). Sign outline redrawn as a clean symmetric polygon at the photo's
proportions: dark border, light keyline, dark field. Colour is unknown (sepia source) -> one ink, letters = garment.
'SOUTHERN FRIED CHICKEN' (lettered on the building) + 'HAMMOND, LA.' set in League Spartan (OFL) below."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from hmlib import remove_small, fill_small_holes, build_multi, disk
from newsprint import render_text
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/didiwa"
INK_DARK, INK_RED = (38, 34, 32), (150, 34, 38)
im = cv2.imread(f"{D}/sign_rect.png").astype(np.float32); g = im.mean(2)
Hs, Ws = g.shape
cx, tipy = 1765, 640
def sym(pts): return np.array(pts + [(2 * cx - x, y) for x, y in reversed(pts)], np.int32)
outer = sym([(cx - 1135, 50), (cx - 1225, 200), (cx - 1675, tipy), (cx - 1600, 1200)])[::-1]
outer = np.array([(cx - 1600, 1200), (cx - 1675, tipy), (cx - 1225, 200), (cx - 1135, 50),
                  (cx + 1135, 50), (cx + 1225, 200), (cx + 1675, tipy), (cx + 1600, 1200)], np.int32)
poly = np.zeros((Hs, Ws), np.uint8); cv2.fillPoly(poly, [outer], 1); poly = poly > 0
BORDER, KEY = 62, 44
inner1 = cv2.erode(poly.astype(np.uint8), disk(BORDER)) > 0            # inside the dark border
field = cv2.erode(inner1.astype(np.uint8), disk(KEY)) > 0              # inside the light keyline
# letters: light paint inside the field (traced)
light = g > 175
L = light & (cv2.erode(field.astype(np.uint8), disk(14)) > 0)
L = cv2.morphologyEx(L.astype(np.uint8), cv2.MORPH_OPEN, disk(4)) > 0
L = fill_small_holes(remove_small(L, 6000), 9000)                       # neon-socket holes and specks
n, lab, st, _ = cv2.connectedComponentsWithStats(L.astype(np.uint8), 8)
for i in range(1, n):
    x, y, w, h, a = st[i]
    hyphen = 1850 < x + w / 2 < 2150 and 280 < y + h / 2 < 520 and w > 80
    keyline_strip = (x + w < 800 and y < 650) or (x > 2900 and y + h < 720)   # the photo's keyline where it falls inside the redrawn field
    if (h < 180 and not hyphen) or keyline_strip: L[lab == i] = False
L = cv2.morphologyEx(L.astype(np.uint8), cv2.MORPH_CLOSE, disk(9))           # paint chips / photo cracks in the letters
L = cv2.morphologyEx(L, cv2.MORPH_OPEN, disk(7)) > 0                          # drips and burrs
L = cv2.GaussianBlur(L.astype(np.float32), (0, 0), 4) > 0.5
ink = (poly & ~inner1) | (field & ~L)                                   # dark border + dark field; keyline + letters = garment
# lower lines: 'SOUTHERN FRIED CHICKEN' / 'HAMMOND, LA.'
def tline(text, h, wght=800, tr=0.06):
    a, (x0, y0, x1, y1) = render_text(text, "LeagueSpartan[wght].ttf", 300, {"wght": wght}, tr)
    a = a[y0:y1, x0:x1]; s = h / a.shape[0]
    return cv2.resize(a, (int(a.shape[1] * s), h), interpolation=cv2.INTER_AREA) > 0.5
l1 = tline("SOUTHERN FRIED CHICKEN", 150, 800, 0.08)
l2 = tline("HAMMOND, LA.", 120, 700, 0.20)
pad = 60; Ht = Hs + 60 + l1.shape[0] + 50 + l2.shape[0] + pad
c = np.zeros((Ht, Ws), bool); c[:Hs] = ink
y = 1200 + 110
for l in (l1, l2):
    x = cx - l.shape[1] // 2; c[y:y + l.shape[0], x:x + l.shape[1]] |= l; y += l.shape[0] + 60
ys, xs = np.where(c); c = c[ys.min() - 30:ys.max() + 31, xs.min() - 30:xs.max() + 31]
H2, W2 = c.shape
build_multi([(c, INK_DARK)], W2, H2, 2850, f"{D}/didiwa_sign_charcoal")      # 9.5 in wide
build_multi([(c, INK_RED)], W2, H2, 2850, f"{D}/didiwa_sign_red")
print(W2, H2)
