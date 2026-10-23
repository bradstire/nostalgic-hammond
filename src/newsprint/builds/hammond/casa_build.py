"""Casa de Fresa Hotel (Hammond, La.) — print files from the hotel's matchbook (Brad's asset dump IMG_7195/7196, 10-22).
Pipeline B: Real-ESRGAN x4 (anime model, CPU/ncnn) -> 3-ink segmentation in Lab -> cleanup -> potrace true vector.
Lettering, panel and stripes are the matchbook's own (traced, not re-drawn); only specks/dust removed.
Inks restored from the print: Casa red, teal green, matchbook cream."""
import sys, numpy as np, cv2
from PIL import Image
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
from hmlib import remove_small, fill_small_holes, build_multi, disk
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/casa"
RED, GREEN, CREAM = (206, 32, 46), (10, 104, 86), (243, 233, 207)

red = cv2.imread(f"{D}/seg_red.png", 0) > 127
green = cv2.imread(f"{D}/seg_green.png", 0) > 127
red = fill_small_holes(remove_small(red, 800), 1200)            # dust specks; keeps the period in "LA."
green = fill_small_holes(remove_small(green, 1000), 1000) & ~red
H0, W0 = red.shape
Y1 = 4112                                                       # striker fold below this row
red, green = red[:Y1], green[:Y1]

# ---------- 1) full matchbook cover (stripes + panel + ribbon) ----------
PADL, PADR = 130, 90                                            # cover paper margins: left edge 62px / right 1112px (orig)
YT = 50                                                         # ragged photo edge at the top: straight cut
def pad(m): return np.pad(m[YT:], ((0, 0), (PADL, PADR)))
R, G = pad(red), pad(green); H, W = R.shape
rect = np.zeros_like(R); rect[:, PADL + 88 - 210: PADL + 3869 + 210] = True
cream = rect & ~R & ~G
build_multi([(G, GREEN), (R, RED)], W, H, 2550, f"{D}/casa_matchbook_cover_natural")            # cream = the natural tee
build_multi([(cream, CREAM), (G, GREEN), (R, RED)], W, H, 2550, f"{D}/casa_matchbook_cover_cream")

# ---------- 2) mark only: red panel + ribbon (no stripes) ----------
def scan(x):
    col = green[:, x]
    y = 3450
    while y < Y1 - 1 and not col[y]: y += 1
    arc_t = y
    y = 3150
    while y > 2500 and not col[y]: y -= 1
    while y > 2500 and col[y]: y -= 1
    while y > 2500 and not col[y]: y -= 1
    a_bot = y
    return arc_t, a_bot
xs = np.arange(1350, 3880, 10)
S = np.array([scan(x) for x in xs])
gap = np.array([green[S[i, 0]:S[i, 0] + 80, x].sum() < 60 for i, x in enumerate(xs)])      # columns with no stripe under the arc
arc_poly = np.polyfit(xs, S[:, 0], 4)
a_poly = np.polyfit(xs, S[:, 1], 4)
T_ARC = 46; T_A = 30
yy, xx = np.mgrid[:Y1, :W0]
arc_top = np.polyval(arc_poly, np.clip(xx, 1350, 3880)); a_top = np.polyval(a_poly, np.clip(xx, 1350, 3880)) - T_A
a_top = np.where(xx < 1400, a_top - 70, a_top)                  # the ribbon's folded left end rises higher
zone = (yy >= a_top - 4) & (yy <= arc_top + T_ARC + 4) & (xx >= 1060) & (xx <= 3910)
panel = fill_small_holes(red, 10**7)                            # panel silhouette incl. lettering
gm = green & zone
gm = remove_small(gm, 600)
rm = red
ys_, xs_ = np.where(rm | gm); y0, y1, x0, x1 = ys_.min(), ys_.max(), xs_.min(), xs_.max()
m = 60
rm, gm = rm[y0 - m:y1 + m, x0 - m:x1 + m], gm[y0 - m:y1 + m, x0 - m:x1 + m]
np.save(f"{D}/mark_zone.npy", zone[y0 - m:y1 + m, x0 - m:x1 + m])
Hm, Wm = rm.shape
build_multi([(gm, GREEN), (rm, RED)], Wm, Hm, 2700, f"{D}/casa_mark")                         # 9 in wide, natural/white tees
build_multi([(gm, GREEN), (rm, RED)], Wm, Hm, 1050, f"{D}/casa_mark_leftchest")              # 3.5 in left chest
np.save(f"{D}/mark_red.npy", rm); np.save(f"{D}/mark_green.npy", gm)
np.save(f"{D}/cover_red.npy", R); np.save(f"{D}/cover_green.npy", G)
print("cover", W, H, "mark", Wm, Hm, "gap cols", int(gap.sum()))
