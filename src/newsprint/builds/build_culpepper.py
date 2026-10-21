import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import to_rgba_ink, vectorize, render_svg
from teemock import place_print, sheet, chest
from PIL import Image

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

# trim to content
ys, xs = np.where(ink); ink = ink[max(0, ys.min() - 20):ys.max() + 20, max(0, xs.min() - 20):xs.max() + 20]
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

# 5) hat: duck only, embroidery-spec. Front panel max ~4.0in x 1.75in; duck at 1.75in tall.
duck = ink[:, :]  # re-extract from the trimmed full
dy0 = int(305 * 3.84) - (ys.min() - 20); dy1 = int(625 * 3.84) - (ys.min() - 20)
dx0 = int(300 * 3.84) - (xs.min() - 20); dx1 = int(580 * 3.84) - (xs.min() - 20)
dk = full[max(0, dy0):dy1, max(0, dx0):dx1]
yy, xx = np.where(dk); dk = dk[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
target_h = int(1.75 * 300)
sc = target_h / dk.shape[0]
dk_s = cv2.resize(dk.astype(np.float32), (int(dk.shape[1] * sc), target_h), interpolation=cv2.INTER_AREA) > 0.5
# embroidery minimums (conservative): strokes thinner than ~1.2mm (14px) get +3px; holes < ~1mm^2 filled
min_px = 14
er = cv2.erode(dk_s.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (min_px, min_px)))
fat = cv2.dilate(er, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (min_px, min_px))) > 0
thin = dk_s & ~fat
thick = dk_s | (cv2.dilate(thin.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0)
n, lab, st, _ = cv2.connectedComponentsWithStats(thick.astype(np.uint8), 8)
thick[np.isin(lab, [i for i in range(1, n) if st[i][4] < 150])] = False
inv = (~thick).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 8)
for i in range(1, n):
    x, y, w, h, area = st[i]
    if area < 140 and not (x == 0 or y == 0 or x + w >= thick.shape[1] or y + h >= thick.shape[0]): thick[lab == i] = True
cv2.imwrite(f"{D}/hat_compare.png", np.hstack([np.where(dk_s, 0, 255), np.full((dk_s.shape[0], 20), 200), np.where(thick, 0, 255)]).astype(np.uint8))
hat = np.pad(thick, 10)
hat = cv2.GaussianBlur(hat.astype(np.float32), (0, 0), 3.2) > 0.5
svg = vectorize(hat, turdsize=20, alphamax=1.25, opttolerance=0.8)
open(f"{D}/culpepper_duck_hat_embroidery.svg", "w").write(svg)
hat_v = render_svg(svg, hat.shape[1], hat.shape[0])
print("hat vector ink before/after", round(hat.mean(), 3), round(hat_v.mean(), 3))
cv2.imwrite(f"{D}/hat_vec_compare.png", np.hstack([np.where(hat, 0, 255), np.full((hat.shape[0], 20), 200), np.where(hat_v, 0, 255)]).astype(np.uint8))
hat = hat_v
to_rgba_ink(hat, (17, 17, 17)).save(f"{D}/culpepper_duck_hat_embroidery.png", dpi=(300, 300))
print("hat", hat.shape, round(hat.shape[1] / 300, 2), "x", round(hat.shape[0] / 300, 2), "in")

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
