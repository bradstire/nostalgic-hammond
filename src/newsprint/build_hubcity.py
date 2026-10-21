import sys, os, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import *

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/hubcity"
gray = cv2.imread(f"{D}/sr_gray_3150.png", 0).astype(np.float32) / 255.0
H_CUT = 3340
gray = gray[:H_CUT]
base = gray < (140 / 255.0)            # SR type, hard threshold
H, W = base.shape

# ---- regions to rebuild (white-out in SR layer)
PHOTO_L = (99, 812, 1492, 2013)
PHOTO_R = (1689, 799, 3070, 2022)
wipe = [(0, 2128, W, 2356), (0, 2393, W, 2612), (0, 2806, W, 2957), (0, 3122, W, 3203), (0, 3228, W, 3330)]
keep = base.copy()
for (x0, y0, x1, y1) in wipe + [PHOTO_L, PHOTO_R]:
    keep[max(0,y0-8):y1+8, max(0,x0-8):x1+16] = False

# ---- re-typeset small copy (Futura-family match: Jost)
BODY = "Jost[wght].ttf"
TR = 0.035
txt = np.zeros((H, W), np.float32)
cap_lines = [
    ("Wickersham Ford, Orange, Texas.", 270, 1272, 2137, 2202),
    ("1965 fuel injected Ford Mustang,", 270, 1270, 2206, 2273),
    ("altered wheelbase. 10.00, 137.00", 279, 1262, 2282, 2346),
    ("1966 Chevrolet Corvair, 396 cu. in.", 1855, 2928, 2137, 2202),
    ("fuel injected, altered wheelbase, 9.90", 1829, 2993, 2206, 2273),
    ("140.00, Memphis, Tennessee.", 1972, 2810, 2282, 2346),
]
AX = {"wght": 640}
fits = [fit_xscale(t, BODY, x1 - x0, y1 - y0, AX, TR) for t, x0, x1, y0, y1 in cap_lines]
print("caption fits", [(round(a, 1), round(b, 2)) for a, b in fits])
s_med = float(np.median([f[0] for f in fits])); xs_med = float(np.median([f[1] for f in fits]))
for (t, x0, x1, y0, y1) in cap_lines:
    cx0, cx1 = (99, 1492) if x0 < 1500 else (1689, 3070)
    place(txt, t, BODY, s_med, AX, cx0, y0, cx1, align="center", tracking=TR, xscale=xs_med)

para = [
    'Would you believe!?! The Corvair has the 396 Chevy engine in the middle?? Joe will be running',
    'a special blend of "Tennessee Tonic" in his Chevy to turn back the "Funny Ford." Chester says,',
    '"Sorry \'bout that . . . Joe\'ll be on the trailer in three!"',
]
P_AX = {"wght": 560}
for i, line in enumerate(para):
    y0 = 2401 + i * 67
    if i < 2: place(txt, line, BODY, s_med * 0.96, P_AX, 69, y0, justify_w=3087 - 69, tracking=TR, xscale=xs_med)
    else:     place(txt, line, BODY, s_med * 0.96, P_AX, 69, y0, tracking=TR, xscale=xs_med)

ent = [("JOE CABIRAN'S B-M Sports Prod. 1957 T-Bird,", 73, 2815, 1480),
       ("427 cu. in., New Orleans, La.", 73, 2881, None),
       ("DOODY RUPERT'S C-MP 1965 Facon 289 cu.", 1679, 2815, 3087),
       ("in. New Orleans, La.", 1679, 2881, None)]
for t, x0, y0, x1 in ent:
    place(txt, t, BODY, s_med, {"wght": 560}, x0, y0, tracking=TR, xscale=xs_med)

xm = BULLET + " Christmas Tree Starting System"
s_x, xs_x = fit_xscale(xm, BODY, 2040 - 1030, 3197 - 3132, {"wght": 760}, 0.02)
place(txt, xm, BODY, s_x, {"wght": 760}, 1030, 3132, 2040, align="center", tracking=0.02, xscale=xs_x)
ahra = "AHRA Sanctioned " + BULLET + " GATES OPEN AT 8:00 A.M.—ELIMINATIONS AT 2:00 P.M. " + BULLET + " NHRA Rules"
s_a, xs_a = fit_xscale(ahra, BODY, 3066 - 82, 64, {"wght": 780}, 0.03)
place(txt, ahra, BODY, s_a, {"wght": 780}, 82, 3246, tracking=0.03, xscale=xs_a)
print("footer fits", round(s_x, 1), round(xs_x, 2), round(s_a, 1), round(xs_a, 2))

txt_ink = roughen(txt, spread=1.3, grain=0.22)

# ---- photos: re-screened halftone from photo-model upscale
ph = cv2.imread(f"{D}/photos_x4plus.png", 0)
photo_ink = np.zeros((H, W), bool)
if ph is not None:
    phf = ph.astype(np.float32) / 255.0
    # photos_raw was raw rows 270..730 at full width 1115; x4 -> map raw coords to 3150 space
    sx = W / 1115.0
    for (x0, y0, x1, y1) in (PHOTO_L, PHOTO_R):
        rx0, rx1 = x0 / sx, x1 / sx
        ry0, ry1 = y0 / sx - 270, y1 / sx - 270
        sub = phf[int(ry0 * 4):int(ry1 * 4), int(rx0 * 4):int(rx1 * 4)]
        sub = cv2.resize(sub, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
        sub = cv2.GaussianBlur(sub, (0, 0), 1.2)               # descreen residue
        lo, hi = np.percentile(sub, 2), np.percentile(sub, 98)  # stretch tones
        sub = np.clip((sub - lo) / (hi - lo + 1e-6), 0, 1)
        dots = halftone(sub, cell=8.0, angle=45, gamma=1.05)
        photo_ink[y0:y1, x0:x1] = dots
        # keep a crisp 3px keyline like the original photo frames
        photo_ink[y0:y0 + 3, x0:x1] = True; photo_ink[y1 - 3:y1, x0:x1] = True
        photo_ink[y0:y1, x0:x0 + 3] = True; photo_ink[y0:y1, x1 - 3:x1] = True
else:
    print("WARN no photo upscale yet; using SR threshold for photos")
    for (x0, y0, x1, y1) in (PHOTO_L, PHOTO_R):
        photo_ink[y0:y1, x0:x1] = base[y0:y1, x0:x1]

final = keep | txt_ink | photo_ink
out = f"{D}/hubcity_ad_front_v2.png"
to_rgba_ink(final).save(out, dpi=(300, 300))
cv2.imwrite(f"{D}/hubcity_v2_view.jpg", mock(final, width=1100), [cv2.IMWRITE_JPEG_QUALITY, 90])
# detail crops at 100% for proofing
cv2.imwrite(f"{D}/hubcity_v2_detail.png", np.where(final[2040:2960, 0:1600], 0, 255).astype(np.uint8))
print("saved", out, final.shape, "in:", round(W / 300, 2), "x", round(H / 300, 2))
