"""Sack's Army Store (143 Market St, Hattiesburg; ad dated 1980; 'In Business Since 1951').
Removed: VISA + Master Charge logos (live marks), phone number, hours."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import *
from teemock import place_print, sheet, chest
from PIL import Image, ImageDraw

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/sacks"
g = cv2.imread(f"{D}/sacks_gray_3150.png", 0)
H0, W = g.shape
S = 2.864  # view(1100) -> 3150 space

def speckless(m, min_area):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    return m & ~np.isin(lab, [i for i in range(1, n) if st[i][4] < min_area])

# --- headline (SR) ---
head = g[int(22 * S):int(98 * S), :] < 140
head = speckless(head, 80)
# --- storefront (SR, light threshold, VISA bar wiped, vector-smoothed) ---
sf = g[int(140 * S):int(410 * S), :] < 180
vx0, vy0 = int(930 * S), int(372 * S) - int(140 * S)
sf[vy0:, vx0:] = False                    # VISA bar region (right end of the sidewalk rows)
sf = speckless(sf, 60)
svg = vectorize(sf, turdsize=10, alphamax=1.0, opttolerance=0.3)
open(f"{D}/sacks_storefront.svg", "w").write(svg)
sf_v = render_svg(svg, sf.shape[1], sf.shape[0])
# restore the sidewalk rule lines across the full width where the VISA wipe cut them
rows = sf_v[:, int(100 * S):int(900 * S)].mean(axis=1)
for y in np.where(rows > 0.55)[0]:
    if y >= vy0 - 4: sf_v[y, int(900 * S):W - int(6 * S)] = True

# --- subline (re-typeset; separators drawn as stars) ---
F = "Jost[wght].ttf"
items = ["SURPLUS", "CAMPING", "CLOTHES", "JACKETS", "BOOTS", "KNIVES"]
sub_h = int(30 * S * 0.78)
def star(size):
    im = Image.new("L", (size * 3, size * 3), 0); d = ImageDraw.Draw(im)
    c = size * 1.5; R = size * 1.45; r = R * 0.42
    pts = [(c + (R if i % 2 == 0 else r) * np.sin(np.pi * i / 5), c - (R if i % 2 == 0 else r) * np.cos(np.pi * i / 5)) for i in range(10)]
    d.polygon(pts, fill=255); a = np.asarray(im) > 127
    ys, xs = np.where(a); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return cv2.resize(a.astype(np.uint8), (size, size), interpolation=cv2.INTER_AREA) > 0
words = []
_, fbb = render_text(" ".join(items), F, 120, {"wght": 700}, 0.10)   # shared vertical range = common baseline
for w_ in items:
    a, bb = render_text(w_, F, 120, {"wght": 700}, 0.10)
    a = a[fbb[1]:fbb[3], bb[0]:bb[2]] > 0.5
    words.append(cv2.resize(a.astype(np.uint8), (int(a.shape[1] * sub_h / a.shape[0]), sub_h), interpolation=cv2.INTER_AREA) > 0)
st_ = star(int(sub_h * 0.62))
gap = int(sub_h * 0.45)
total = sum(w.shape[1] for w in words) + (len(words) - 1) * (st_.shape[1] + 2 * gap)
target = int(W * 0.93)
scale = target / total
words = [cv2.resize(w.astype(np.uint8), (int(w.shape[1] * scale), int(w.shape[0] * scale)), interpolation=cv2.INTER_AREA) > 0 for w in words]
st_ = cv2.resize(st_.astype(np.uint8), (int(st_.shape[1] * scale), int(st_.shape[0] * scale)), interpolation=cv2.INTER_AREA) > 0
gap = int(gap * scale); sh = words[0].shape[0]
subline = np.zeros((sh, W), bool); x = (W - target) // 2
for i, w_ in enumerate(words):
    subline[:, x:x + w_.shape[1]] = w_; x += w_.shape[1]
    if i < len(words) - 1:
        x += gap; y = (sh - st_.shape[0]) // 2; subline[y:y + st_.shape[0], x:x + st_.shape[1]] = st_; x += st_.shape[1] + gap

# --- bottom block (rebuilt, centered) ---
addr = g[int(435 * S):int(482 * S), int(120 * S):int(560 * S)] < 140   # '143 MARKET STREET' is clean in SR
addr = speckless(addr, 60)
ys, xs = np.where(addr); addr = addr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def tline(text, ax, h, xs=1.0, tr=0.04):
    a, bb = render_text(text, F, 140, ax, tr, xs)
    a = a[bb[1]:bb[3], bb[0]:bb[2]]
    return cv2.resize(a, (int(a.shape[1] * h / a.shape[0]), h), interpolation=cv2.INTER_AREA)
down = tline("DOWNTOWN HATTIESBURG", {"wght": 600}, int(addr.shape[0] * 0.80), 1.0, 0.06) > 0.5
since_raw = tline("‘In Business Since 1951’", {"wght": 600}, int(addr.shape[0] * 0.92), 1.0, 0.05)
# Jost has no true italic in this file -> shear for the original's oblique
hh, ww = since_raw.shape
M = np.float32([[1, -0.19, 0.19 * hh], [0, 1, 0]])
since = cv2.warpAffine(since_raw, M, (ww + int(0.2 * hh), hh)) > 0.5
txt = np.zeros_like(down, dtype=np.float32)

# --- assemble ---
def put(canvas, m, y, x=None):
    x = (canvas.shape[1] - m.shape[1]) // 2 if x is None else x
    canvas[y:y + m.shape[0], x:x + m.shape[1]] |= m
    return y + m.shape[0]
pad = int(16 * S)
Ht = head.shape[0] + subline.shape[0] + sf_v.shape[0] + addr.shape[0] + down.shape[0] + since.shape[0] + 7 * pad
C = np.zeros((Ht, W), bool)
y = pad // 2
y = put(C, head, y) + int(pad * 0.5)
y = put(C, subline, y) + int(pad * 0.3)
y = put(C, sf_v, y) + int(pad * 1.2)
y = put(C, addr, y) + int(pad * 0.55)
y = put(C, down, y) + int(pad * 0.55)
y = put(C, since, y) + pad
C = C[:y]
# frame: clean box rule like the original ad border
fr = 14
C[:fr, :] = True; C[-fr:, :] = True; C[:, :fr] = True; C[:, -fr:] = True
C = roughen(C.astype(np.float32), spread=0.7, grain=0.10) | C
to_rgba_ink(C, (17, 17, 17)).save(f"{D}/sacks_front_black.png", dpi=(300, 300))
to_rgba_ink(C, (255, 255, 255)).save(f"{D}/sacks_front_white.png", dpi=(300, 300))
OD = (88, 92, 62)  # olive drab garment
to_rgba_ink(C, (236, 228, 210)).save(f"{D}/sacks_front_cream.png", dpi=(300, 300))
print("sacks", C.shape, round(C.shape[1] / 300, 2), "x", round(C.shape[0] / 300, 2), "in")
tiles = [chest(f"{D}/sacks_front_black.png", (236, 228, 210), print_w_in=10.5, W=560, top_in=3.0, label="Natural tee / black"),
         chest(f"{D}/sacks_front_cream.png", OD, print_w_in=10.5, W=560, top_in=3.0, label="Olive drab tee / cream"),
         chest(f"{D}/sacks_front_white.png", (24, 24, 26), print_w_in=10.5, W=560, top_in=3.0, label="Black tee / white")]
sheet(tiles, cols=3).save(f"{D}/sacks_mocks.jpg", quality=88)
cv2.imwrite(f"{D}/sacks_view.jpg", mock(C, width=1100), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("done")
