"""Camelot Music — Hattiesburg (Cloverleaf Mall, est. 1974), v2 in the chain's own 1970s colors.
Reference: 1970s Camelot paper bag (red inline blackletter, royal-blue record-groove arcs, red Futura caps)
and the 1990s plastic bags (red/black wordmark + yellow/cyan/red tri-stripe). Knight emblem NOT used."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text
from teemock import place_print, sheet, chest
from PIL import Image

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/camelot"
RED, BLUE, BLACK, YEL, CYAN = (198, 40, 50), (46, 73, 184), (20, 20, 20), (242, 190, 40), (30, 160, 212)
BL = "GrenzeGotisch[wght].ttf"

def crop(a):
    ys, xs = np.where(a > 0.5); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def word(text, font, ax, w=None, h=None, tr=0.0, xs=1.0):
    a = crop(render_text(text, font, 170, ax, tr, xs)[0])
    sc = min(w / a.shape[1] if w else 1e9, h / a.shape[0] if h else 1e9)
    return cv2.resize(a, (int(a.shape[1] * sc), int(a.shape[0] * sc)), interpolation=cv2.INTER_AREA) > 0.5
def inline(m, gap=10, stroke=9):
    """Bag-style letters: solid core, knockout gap, thin outer stroke."""
    p = gap + stroke + 4; m = np.pad(m, p)
    k = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    g = cv2.dilate(m.astype(np.uint8), k(gap)) > 0
    o = cv2.dilate(m.astype(np.uint8), k(gap + stroke)) > 0
    return m | (o & ~g)

class Layers:
    def __init__(self, h, w): self.h, self.w = h, w; self.L = []
    def add(self, mask, color, x, y):
        full = np.zeros((self.h, self.w), bool); full[y:y + mask.shape[0], x:x + mask.shape[1]] = mask[:self.h - y, :self.w - x]
        self.L.append((full, color))
    def save(self, path):
        rgba = np.zeros((self.h, self.w, 4), np.uint8)
        for m, c in self.L:  # later layers on top
            rgba[m, :3] = c; rgba[m, 3] = 255
        Image.fromarray(rgba, "RGBA").save(path, dpi=(300, 300)); return path

small_txt = "CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974"

# ---- A: 1974 bag — stacked inline blackletter in red inside royal-blue groove arcs
W, H = 3150, 3100
L = Layers(H, W)
cx, cy = W // 2, 1600
for i, (r, t) in enumerate(((1480, 110), (1300, 70), (1160, 46))):   # three grooves, heavy to light like the bag
    ring = np.zeros((H, W), np.uint8)
    cv2.circle(ring, (cx, cy), r, 1, t)
    ring[cy + 120:, :] = 0                                           # arcs over the top + down the sides
    L.add(ring > 0, BLUE, 0, 0)
cam = inline(word("Camelot", BL, {"wght": 700}, w=2050, xs=0.9))
mus = inline(word("Music", BL, {"wght": 700}, w=1650, xs=0.9))
# knock the arcs out behind the letters (white keyline like the bag)
halo = lambda m, r=26: cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) > 0
yc = 1120; ym = yc + cam.shape[0] + 40
for m, y in ((cam, yc), (mus, ym)):
    x = cx - m.shape[1] // 2
    hm = halo(m)
    for full, c in L.L:
        sub = full[y - 26:y - 26 + hm.shape[0], x - 26:x - 26 + hm.shape[1]]
        hh = np.pad(hm, 26)[:sub.shape[0], :sub.shape[1]]
        sub[hh] = False
    L.add(m, RED, x, y)
sm = word(small_txt, "Jost[wght].ttf", {"wght": 700}, w=2300, tr=0.08)
L.add(sm, RED, cx - sm.shape[1] // 2, ym + mus.shape[0] + 150)
ys = np.where(np.any([m for m, _ in L.L], axis=0).any(axis=1))[0]
L.h = ys.max() + 30
L.L = [(m[:L.h], c) for m, c in L.L]
pA = L.save(f"{D}/camelot_v2_bag1974.png")

# ---- B: the 1974 Cloverleaf sign (single line) in chain red, blue locator line
W2 = 3150
logo = word("Camelot Music", BL, {"wght": 700}, w=W2 - 140, xs=0.86)
sm2 = word(small_txt, "Jost[wght].ttf", {"wght": 640}, w=int(W2 * 0.70), tr=0.14)
H2 = logo.shape[0] + 70 + sm2.shape[0] + 40
L = Layers(H2, W2); L.add(logo, RED, (W2 - logo.shape[1]) // 2, 10); L.add(sm2, BLUE, (W2 - sm2.shape[1]) // 2, logo.shape[0] + 70)
pB = L.save(f"{D}/camelot_v2_sign_red_blue.png")
L = Layers(H2, W2); L.add(logo, RED, (W2 - logo.shape[1]) // 2, 10); L.add(sm2, (255, 255, 255), (W2 - sm2.shape[1]) // 2, logo.shape[0] + 70)
pB2 = L.save(f"{D}/camelot_v2_sign_red_white.png")

# ---- C: 1990s 'tri-stripe' nod — sign wordmark (red, black keyline) over yellow/cyan/red stripes
logoC = word("Camelot Music", BL, {"wght": 700}, w=2700, xs=0.86)
key = halo(logoC, 9) & ~logoC
sh = 70; gap = 22
H3 = logoC.shape[0] + 9 * 2 + 60 + 3 * sh + 2 * gap + 90 + sm2.shape[0] + 40
L = Layers(H3, W2)
x0 = (W2 - logoC.shape[1]) // 2
yS = logoC.shape[0] + 18 + 60
for i, c in enumerate((YEL, CYAN, RED)):
    bar = np.ones((sh, int(W2 * 0.92)), bool)
    L.add(bar, c, (W2 - bar.shape[1]) // 2, yS + i * (sh + gap))
L.add(np.pad(key, 9), BLACK, x0 - 9, 0); L.add(np.pad(logoC, 9), RED, x0 - 9, 0)
sm3 = word(small_txt, "Jost[wght].ttf", {"wght": 640}, w=int(W2 * 0.70), tr=0.14)
L.add(sm3, BLACK, (W2 - sm3.shape[1]) // 2, yS + 3 * sh + 2 * gap + 90)
pC = L.save(f"{D}/camelot_v2_tristripe.png")

WHITE, NAT, BLK, HEATHER = (250, 250, 250), (236, 228, 210), (24, 24, 26), (200, 200, 198)
combos = [(pA, WHITE, 10.5, "White tee / 1974 bag (red + royal blue)"),
          (pA, NAT, 10.5, "Natural tee / 1974 bag"),
          (pB, WHITE, 10.5, "White tee / 1974 sign, chain red + blue"),
          (pB2, BLK, 10.5, "Black tee / sign red + white"),
          (pC, WHITE, 10.5, "White tee / 1990s tri-stripe nod"),
          (pC, HEATHER, 10.5, "Heather grey / tri-stripe")]
sheet([chest(p, g, print_w_in=w, W=560, top_in=2.6, label=l) for p, g, w, l in combos], cols=3).save(f"{D}/camelot_v2_mocks.jpg", quality=88)
print("done")
