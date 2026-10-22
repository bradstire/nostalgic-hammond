import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import to_rgba_ink, vectorize, render_svg
from teemock import place_print, sheet, chest
from PIL import Image
sys.path.insert(0, '/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/culpepper')
from face_redraw import face_cuts, face_cuts_hat
from duck_details import details, details_hat, thicken_outlines

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/culpepper"
g = cv2.imread(f"{D}/culp_gray_3150.png", 0)
H, W = g.shape
ink = g < 140

# rows of the layout (3150-wide space, measured from the view x 3.84)
def band(y0, y1): return slice(int(y0 * 3.84), int(y1 * 3.84))
DUCK = (band(305, 625), slice(int(300 * 3.84), int(580 * 3.84)))
CLOUD = (band(300, 420), slice(int(495 * 3.84), int(575 * 3.84)))

# 1) cloud: the puffs are light-gray outlines in the source -> recover with a lighter threshold, locally
cl = g[CLOUD] < 190
cl = cv2.morphologyEx(cl.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
ink[CLOUD] |= cl

# 2) duck body: fill SR pinholes (white specks < 900 px inside the figure)
d = ink[DUCK].copy()
inv = (~d).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 8)
for i in range(1, n):
    x, y, w, h, area = st[i]
    touches = x == 0 or y == 0 or x + w >= d.shape[1] or y + h >= d.shape[0]
    if area < 900 and not touches:
        d[lab == i] = True
ink[DUCK] = d

# 3) global speck removal (isolated ink < 120 px) incl. the stray '.' before F.D.
n, lab, st, _ = cv2.connectedComponentsWithStats(ink.astype(np.uint8), 8)
small = np.isin(lab, [i for i in range(1, n) if st[i][4] < 120])
ink[small] = False
stray = (band(668, 700), slice(int(105 * 3.84), int(140 * 3.84)))  # the lone '.' left of F.D.
ink[stray] = False

# 3b) face-detail redraw (eye, cap keyline, bill line) — tee weight and a heavier embroidery weight
FR = (slice(1152, 2419), slice(1152, 2246))
ink_hat = ink.copy()
base_FR = ink[FR].copy()
ink[FR] = details(ink[FR], w=12, face_line=8)          # v3: face + shirt + arm negative space (Brad 10-22)
ink_hat[FR] = details(ink_hat[FR], w=12, face_line=8)  # (hat is rebuilt from base_FR below at embroidery weight)

# trim to content
ys, xs = np.where(ink)
TR = (slice(max(0, ys.min() - 20), ys.max() + 20), slice(max(0, xs.min() - 20), xs.max() + 20))
ink = ink[TR]; full_hat = ink_hat[TR]
full = ink.copy()

# 4) house-rule cut: remove the owner-name lines (F.D. "Duck" / Culpepper-owner) and close the gap
rows = full.mean(axis=1) > 0.002
# find text-line bands below the duck
y_duck_end = int(625 * 3.84) - (ys.min() - 20)
bands = []; inb = False
for y in range(y_duck_end, full.shape[0]):
    if rows[y] and not inb: s = y; inb = True
    elif not rows[y] and inb:
        inb = False
        if y - s > 30: bands.append((s, y))
if inb: bands.append((s, full.shape[0]))
print("text bands below duck:", bands)
# bands: [F.D. Duck], [Culpepper-owner], [The king of body &], [paint work"], [113 N. Tipton], [545-7785]
cut0, cut1 = bands[0][0], bands[2][0]
gap = bands[0][0] - y_duck_end if bands[0][0] > y_duck_end else 60
house = np.vstack([full[:cut0 - 4], np.zeros((60, full.shape[1]), bool), full[cut1 - 8:bands[4][1] + 40]])  # drops owner lines + phone

designs = {"full": full, "houserule": house}
paths = {}
for k, m in designs.items():
    m = np.pad(m, 12)
    for n_, rgb in (("black", (17, 17, 17)), ("white", (255, 255, 255))):
        p = f"{D}/culpepper_{k}_{n_}.png"; to_rgba_ink(m, rgb).save(p, dpi=(300, 300)); paths[(k, n_)] = p
    print(k, m.shape, round(m.shape[1] / 300, 2), "x", round(m.shape[0] / 300, 2), "in")

# 5) hat v3: embroidery weight built from the clean base (Brad 10-22). Printful dad hat front: 5.5 x 2.0 in;
#    lines >= 0.05in; duck 1.9in tall -> scale ~0.45 from FR px, so 0.05in = ~33 FR px.
def disk(r): return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
HAT_H = int(1.9 * 300)
b = base_FR.copy()
ys_, xs_ = np.where(b); b = b[ys_.min():ys_.max() + 1, xs_.min():xs_.max() + 1]
sc = HAT_H / b.shape[0]; MIN_FR = int(np.ceil(0.05 * 300 / sc)) + 2
b = thicken_outlines(b, MIN_FR)                                                   # thin black lines -> >= 0.05in
inv = (~b).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 8)
for i_ in range(1, n):                                                           # white specks too small to stitch -> fill
    x, y, w_, h_, area = st[i_]
    if area < MIN_FR ** 2 and not (x == 0 or y == 0 or x + w_ >= b.shape[1] or y + h_ >= b.shape[0]): b[lab == i_] = True
pad = np.zeros_like(base_FR); pad[ys_.min():ys_.max() + 1, xs_.min():xs_.max() + 1] = b
# spray cloud: clean outline-only puff (white inside, as printed) at stitch width; gun nozzle kept as-is
CY, CX = slice(15, 410), slice(800, 1005)
cb = pad[CY, CX].copy()
filled = cb.copy(); ff = np.zeros((cb.shape[0] + 2, cb.shape[1] + 2), np.uint8)
inv_ = (~cb).astype(np.uint8); cv2.floodFill(inv_, ff, (0, 0), 0); filled = cb | (inv_ > 0)
filled = cv2.morphologyEx(filled.astype(np.uint8), cv2.MORPH_OPEN, disk(6)) > 0
ring = filled & ~(cv2.erode(filled.astype(np.uint8), disk(MIN_FR // 2 + 2)) > 0)
yy, xx = np.mgrid[0:cb.shape[0], 0:cb.shape[1]]
gun = (xx < 80) & (yy > 230) & (yy < 345)                     # nozzle where it meets the puff
pad[CY, CX] = ring | (cb & gun)
b = details_hat(pad, MIN_FR + 2)[ys_.min():ys_.max() + 1, xs_.min():xs_.max() + 1]   # white details >= 0.05in
dk_s = cv2.resize(b.astype(np.float32), (int(b.shape[1] * sc), HAT_H), interpolation=cv2.INTER_AREA) > 0.5
hat = np.pad(dk_s, 10)
hat = cv2.GaussianBlur(hat.astype(np.float32), (0, 0), 1.6) > 0.5
svg = vectorize(hat, turdsize=20, alphamax=1.1, opttolerance=0.6)
open(f"{D}/culpepper_duck_hat_embroidery.svg", "w").write(svg)
hat = render_svg(svg, hat.shape[1], hat.shape[0])
to_rgba_ink(hat, (17, 17, 17)).save(f"{D}/culpepper_duck_hat_embroidery.png", dpi=(300, 300))
print("hat", hat.shape, round(hat.shape[1] / 300, 2), "x", round(hat.shape[0] / 300, 2), "in; FR px per 0.05in =", MIN_FR)

# mocks
combos = [(paths[("full", "black")], (250, 250, 250), "White tee / full ad"),
          (paths[("houserule", "black")], (236, 228, 210), "Natural tee / house-rule cut"),
          (paths[("houserule", "white")], (24, 24, 26), "Black tee / house-rule cut")]
tiles = [place_print(p, gcol, print_w_in=10.0, W=560, top_in=2.2, label=l) for p, gcol, l in combos]
# hat mock: simple panel
hm = Image.new("RGB", (560, int(560 * 0.86)), (236, 234, 230))
from PIL import ImageDraw
dr = ImageDraw.Draw(hm); dr.chord((60, 90, 500, 560), 180, 360, fill=(196, 178, 140)); dr.rectangle((60, 324, 500, 340), fill=(176, 158, 120))
dr.ellipse((30, 320, 530, 420), fill=(186, 168, 130)); dr.text((14, 14), "Khaki dad hat / duck embroidery (black thread)", fill=(90, 90, 90))
ha = Image.open(f"{D}/culpepper_duck_hat_embroidery.png").convert("RGBA"); hh = 150; ha = ha.resize((int(ha.width * hh / ha.height), hh))
hm.paste(ha, (280 - ha.width // 2, 165), ha)
tiles.append(hm)
tiles = [t.resize((560, int(560 * 0.86))) for t in tiles]
sheet(tiles, cols=2).save(f"{D}/culpepper_mocks.jpg", quality=88)
print("done")
