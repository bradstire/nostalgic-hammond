"""Albert Speed's Restaurant (304 Broadway Dr., Hattiesburg, 1966) — sign redraw, flat colors, binary alpha.
Excludes the yellow top-hat figure panel (Mr. Peanut lookalike; live Planters mark)."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text
from teemock import place_print, sheet, chest
from PIL import Image, ImageDraw

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/speeds"
K = 2  # supersample
RED, DRED, CREAM, BLACK, GREEN, YEL, ORANGE, WHITE = (178, 46, 34), (104, 22, 16), (244, 233, 206), (22, 22, 22), (48, 132, 78), (204, 160, 58), (206, 120, 42), (246, 242, 230)
ARROW = (218, 214, 140)  # pale yellow-green per the 1966 photo

def text_mask(text, font, ax, tr, xs, w=None, h=None, rounded=False):
    a, _ = render_text(text, font, 160, ax, tr, xs)
    if rounded:  # neon-tube corners
        a = cv2.GaussianBlur(a, (0, 0), 6.0)
    ys, xs_ = np.where(a > 0.5); a = a[ys.min():ys.max() + 1, xs_.min():xs_.max() + 1]
    if w and h:
        sc = min(w / a.shape[1], h / a.shape[0])
    elif w: sc = w / a.shape[1]
    else: sc = h / a.shape[0]
    return cv2.resize(a, (max(1, int(a.shape[1] * sc)), max(1, int(a.shape[0] * sc))), interpolation=cv2.INTER_AREA) > 0.5

class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w * K, h * K
        self.rgb = np.zeros((self.h, self.w, 3), np.uint8); self.a = np.zeros((self.h, self.w), bool)
    def shape(self, fn, color):
        m = Image.new("1", (self.w, self.h), 0); fn(ImageDraw.Draw(m)); m = np.array(m, bool)
        self.rgb[m] = color; self.a |= m
    def rrect(self, box, r, color):
        self.shape(lambda d: d.rounded_rectangle([v * K for v in box], radius=r * K, fill=1), color)
    def poly(self, pts, color):
        self.shape(lambda d: d.polygon([(x * K, y * K) for x, y in pts], fill=1), color)
    def text(self, mask, cx, top, color, align="center", x0=None):
        mh, mw = mask.shape; big = cv2.resize(mask.astype(np.uint8), (mw * K, mh * K), interpolation=cv2.INTER_NEAREST) > 0
        X = int((cx * K - big.shape[1] / 2) if align == "center" else x0 * K); Y = int(top * K)
        sub = self.rgb[Y:Y + big.shape[0], X:X + big.shape[1]]; sub[big] = color
        self.a[Y:Y + big.shape[0], X:X + big.shape[1]] |= big
    def save(self, path):
        rgb = cv2.resize(self.rgb, (self.w // K, self.h // K), interpolation=cv2.INTER_NEAREST)
        a = cv2.resize(self.a.astype(np.uint8) * 255, (self.w // K, self.h // K), interpolation=cv2.INTER_AREA) > 127
        out = np.dstack([rgb, np.where(a, 255, 0).astype(np.uint8)])
        Image.fromarray(out, "RGBA").save(path, dpi=(300, 300)); return path

SIGN_F, SIGN_AX = "Archivo[wdth,wght].ttf", {"wght": 720, "wdth": 82}

def main_sign(c, x, y, w, h):
    c.rrect((x, y, x + w, y + h), 70, DRED)
    c.rrect((x + 34, y + 34, x + w - 34, y + h - 34), 46, RED)
    c.rrect((x + 58, y + 58, x + w - 58, y + h - 58), 34, None or RED)
    lh = (h - 220) / 3.3
    for i, (t, wf) in enumerate((("ALBERT", 0.56), ("SPEED'S", 0.62), ("RESTAURANT", 0.88))):
        m = text_mask(t, SIGN_F, SIGN_AX, 0.05, 1.0, w=int(w * wf), h=int(lh), rounded=True)
        c.text(m, x + w / 2 + 12, y + 110 + i * lh * 1.15 + 12, DRED)   # channel-letter depth
        c.text(m, x + w / 2, y + 110 + i * lh * 1.15, CREAM)
    # green accent bars flanking SPEED'S (as on the sign)
    by = y + 110 + lh * 1.15 + lh * 0.38; bh = lh * 0.22
    for bx0, bx1 in ((x + 58, x + w * 0.19), (x + w * 0.81, x + w - 58)):
        c.rrect((bx0, by, bx1, by + bh), 10, GREEN)
        c.rrect((bx0, by + bh * 0.42, bx1, by + bh * 0.58), 2, CREAM)

def parking(c, x, y, w, h):
    c.poly([(x, y + h / 2), (x + h * 0.9, y - h * 0.12), (x + h * 0.9, y + h * 1.12)], ARROW)
    c.rrect((x + h * 0.75, y, x + w, y + h), 18, BLACK)
    m = text_mask("PARKING", SIGN_F, {"wght": 600}, 0.10, 1.0, w=int((w - h) * 0.80), h=int(h * 0.62))
    c.text(m, x + h * 0.75 + (w - h * 0.75) / 2, y + h * 0.19, CREAM)

def seafood(c, x, y, w, h):
    c.rrect((x, y, x + w, y + h), 24, BLACK); c.rrect((x + 18, y + 18, x + w - 18, y + h - 18), 16, WHITE)
    fr = text_mask("Fresh", "Yellowtail-Regular.ttf", None, 0.0, 1.0, w=int(w * 0.62), h=int(h * 0.36))
    c.text(fr, x + w / 2, y + h * 0.07, RED)
    sf = text_mask("SEA FOOD", SIGN_F, {"wght": 700}, 0.04, 1.0, w=int(w * 0.80), h=int(h * 0.27))
    c.text(sf, x + w / 2, y + h * 0.47, BLACK)
    cs = text_mask("CHOICE STEAKS", SIGN_F, {"wght": 600}, 0.08, 1.0, w=int(w * 0.72), h=int(h * 0.13))
    c.text(cs, x + w / 2, y + h * 0.80, BLACK)

def steaks(c, x, y, w, h):
    c.rrect((x, y, x + w, y + h), 22, BLACK); c.rrect((x + 16, y + 16, x + w - 16, y + h - 16), 14, WHITE)
    a = text_mask("CHARCOAL BROILED", SIGN_F, {"wght": 600}, 0.10, 1.0, w=int(w * 0.66), h=int(h * 0.13))
    c.text(a, x + w / 2, y + h * 0.10, RED)
    s = text_mask("STEAKS", SIGN_F, {"wght": 700}, 0.06, 1.0, w=int(w * 0.80), h=int(h * 0.44))
    c.text(s, x + w / 2, y + h * 0.30, RED)
    l = text_mask("• ALL CUTS •", SIGN_F, {"wght": 600}, 0.12, 1.0, w=int(w * 0.46), h=int(h * 0.13))
    c.text(l, x + w / 2, y + h * 0.80, BLACK)

# ---- A: main sign + locator line (chest, 10.5in)
WA, HA = 3150, 1900
c = Canvas(WA, HA)
main_sign(c, 0, 0, WA, 1560)
loc = text_mask("304 BROADWAY DR. · HATTIESBURG, MISS. · 1966", "Jost[wght].ttf", {"wght": 600}, 0.16, 1.0, w=int(WA * 0.74))
pa = c.save(f"{D}/speeds_sign_front.png")
# locator line in its own ink layer (color per garment)
def with_locator(path, ink):
    im = np.array(Image.open(path)); m = np.zeros(im.shape[:2], bool)
    mh, mw = loc.shape; X = (WA - mw) // 2; Y = 1560 + 120
    m[Y:Y + mh, X:X + mw] = loc
    im[m] = (*ink, 255); return Image.fromarray(im)
for n, ink in (("cream", CREAM), ("black", BLACK)):
    with_locator(pa, ink).save(f"{D}/speeds_sign_front_{n}loc.png", dpi=(300, 300))

# ---- B: full pylon stack (back print or large front, ~9in wide x 14in tall)
WB, HB = 2700, 4200
c = Canvas(WB, HB)
pole_x = WB * 0.5
c.rrect((pole_x - 70, 600, pole_x + 70, 900), 10, YEL)            # neck between top panel and main sign
c.rrect((pole_x - WB * 0.24, 2100, pole_x + WB * 0.24, HB - 300), 14, YEL)   # wide mustard tower (per 1966 photo)
c.rrect((pole_x - WB * 0.24, HB - 700, pole_x + WB * 0.24, HB - 300), 14, ORANGE)  # orange base box
for lx in (pole_x - WB * 0.16, pole_x + WB * 0.12):                    # white legs
    c.rrect((lx, HB - 300, lx + 70, HB - 30), 8, WHITE)
seafood(c, WB * 0.18, 0, WB * 0.64, 700)
main_sign(c, 0, 820, WB, 1340)
parking(c, WB * 0.10, 2290, WB * 0.80, 330)
steaks(c, WB * 0.22, 2760, WB * 0.56, 620)
pb = c.save(f"{D}/speeds_pylon_full.png")

combos = [(f"{D}/speeds_sign_front_cream" + "loc.png", (24, 24, 26), 10.5, "Black tee / sign"),
          (f"{D}/speeds_sign_front_blackloc.png", (236, 228, 210), 10.5, "Natural tee / sign"),
          (f"{D}/speeds_sign_front_blackloc.png", (250, 250, 250), 10.5, "White tee / sign"),
          (pb, (236, 228, 210), 9.0, "Natural tee / full pylon"),
          (pb, (24, 24, 26), 9.0, "Black tee / full pylon"),
          (pb, (60, 92, 74), 9.0, "Forest tee / full pylon")]
tiles = []
for p, g, w_in, l in combos:
    if "pylon" in l: tiles.append(place_print(p, g, print_w_in=w_in, W=560, top_in=2.4, label=l))
    else: tiles.append(chest(p, g, print_w_in=w_in, W=560, top_in=3.0, label=l))
# normalize tile sizes for the sheet
tw, th = 560, int(560 * 0.86)
tiles = [t.resize((tw, th)) for t in tiles]
sheet(tiles, cols=3).save(f"{D}/speeds_mocks.jpg", quality=88)
print("done", pa, pb)
