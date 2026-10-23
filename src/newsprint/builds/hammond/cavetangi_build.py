"""Cave Tangi Restaurants - the printed paper napkin (IMG_7198): the strutting rooster with cane and spats, CAVE TANGI
RESTAURANTS, the two locations and 'Phone Orders Ready To Go In 20 Minutes'. Pipeline B: Real-ESRGAN x4 (anime model,
line art) -> red ink separated in Lab and traced as is (the napkin's own drawing and condensed gothic type).
Repairs (the photo has a souvenir mug lying across the napkin): the rooster's raised wing runs behind the mug - its hidden
right edge is closed with one outline stroke of the drawing's own weight along the mug's edge; the speed lines end at that
edge; the I of TANGI, clipped at its top by the mug, is rebuilt from its own visible stem. Left off: both phone numbers
(PHO. DI 2-3060, PHO. 7529); the two address lines are re-centred on the type column."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
from hmlib import remove_small, fill_small_holes, build_multi, disk
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/cavetangi"
im = cv2.imread(f"{D}/ct7198_x4.png"); lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32)
a = lab[..., 1] - 128
H, W = a.shape
red = a > 22
RED = tuple(int(v) for v in np.median(im[red & (a > 35)], axis=0)[::-1])
# ---- the mug's left edge per row (auto from its black outline above y 1250, then measured points) ----
from scipy.ndimage import median_filter
L_ = lab[..., 0] * 100 / 255; b_ = lab[..., 2] - 128
cer = (((L_ < 42) & (a < 14) & (np.abs(b_) < 15)) | ((b_ > 25) & (L_ < 75) & (a < 25))).astype(np.uint8)   # mug: black outline + brown glaze
cer[:, :1800] = 0
cer = cv2.morphologyEx(cer, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
n_, lab_, st_, _ = cv2.connectedComponentsWithStats(cer, 8)
Cm = np.isin(lab_, [i for i in range(1, n_) if st_[i, 4] > 20000])
bauto = np.array([np.where(r)[0].min() if r.any() else W for r in Cm], float)
bauto = median_filter(bauto, size=41)
bnd = np.full(H, float(W))
ys = np.arange(H)
bnd[:1250] = bauto[:1250]
bnd[1250:1380] = np.interp(ys[1250:1380], [1250, 1380], [bauto[1249], 2245])
bnd[1380:1850] = np.interp(ys[1380:1850], [1380, 1850], [2245, 2700])
bnd[1850:3700] = np.minimum(bauto[1850:3700], 3300)
yy, xx = np.mgrid[:H, :W]
MARG = 10
keep = xx < (bnd[:, None] - MARG)
ink = red & keep
ink = fill_small_holes(remove_small(ink, 60), 40)
# ---- wing closure: the longest run of rows where the drawing reaches the mug edge (y 850-1400) ----
touch = np.array([ink[y, max(0, int(bnd[y]) - MARG - 18):max(0, int(bnd[y]) - MARG)].any() for y in range(H)])
run, best, start = 0, (0, 0), None
for y in range(850, 1400):
    if touch[y]:
        if start is None: start = y
        if y - start > best[1] - best[0]: best = (start, y)
    else: start = None
y0w, y1w = best
STROKE = 14
pts = np.array([[int(bnd[y]) - MARG - STROKE // 2, y] for y in range(y0w, y1w + 1, 4)], np.int32)
cc = ink.astype(np.uint8)
cv2.polylines(cc, [pts], False, 1, STROKE, lineType=cv2.LINE_AA)
ink = cc > 0
# ---- TANGI's I: rebuild from its visible stem (left/right edges and foot), full cap height of the line ----
tb = ink[3550:4050, 2700:3000]
n, lb, st, _ = cv2.connectedComponentsWithStats(tb.astype(np.uint8), 8)
if n > 1:
    i = 1 + int(np.argmax(st[1:, 4])); x, y, w, h, ar = st[i]
    stem = lb == i
    rows = np.where(stem.any(1))[0]; bottom = rows.max()
    lefts = [np.where(stem[r])[0].min() for r in rows[-120:]]; rights = [np.where(stem[r])[0].max() for r in rows[-120:]]
    xl, xr = int(np.median(lefts)), int(np.median(rights))
    # cap height = the line's T (first letter of TANGI) height
    tline = ink[3550:4050, 1700:2700]; tr = np.where(tline.any(1))[0]; cap_top = tr.min()
    tb[:, :] = tb & ~stem
    tb[cap_top:bottom + 1, xl:xr + 1] = True
    ink[3550:4050, 2700:3000] = tb
# ---- drop the phone numbers; re-centre the address lines ----
def band_rows(y0, y1): return slice(y0, y1)
addr = []
for (y0, y1) in ((4640, 4894), (4894, 5160)):
    sub = ink[y0:y1].copy(); cols = np.where(sub.any(0))[0]
    # the phone sits at the left, separated from the address by the widest gap
    gaps = np.diff(cols); k = int(np.argmax(gaps)); split = cols[k] + gaps[k] // 2
    part = sub[:, split:]; ink[y0:y1] = False
    xs_ = np.where(part.any(0))[0]; part = part[:, xs_.min():xs_.max() + 1]
    addr.append((y0, part))
col = ink[3500:4600]; cx = int(np.mean(np.where(col.any(0))[0][[0, -1]]))          # CAVE TANGI / RESTAURANTS column centre
for y0, part in addr:
    x0 = cx - part.shape[1] // 2; ink[y0:y0 + part.shape[0], x0:x0 + part.shape[1]] |= part
ink = cv2.GaussianBlur(ink.astype(np.float32), (0, 0), 1.2) > 0.5
ys_, xs_ = np.where(ink); ink = ink[ys_.min() - 30:ys_.max() + 31, xs_.min() - 30:xs_.max() + 31]
Hh, Ww = ink.shape
build_multi([(ink, RED)], Ww, Hh, 2550, f"{D}/cavetangi_napkin", turd=8)                 # 8.5 in wide
print("RED", RED, "wing rows", best, "size", Ww, Hh, "-> in", 8.5, round(8.5 * Hh / Ww, 2))
