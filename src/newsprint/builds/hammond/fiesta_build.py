"""Fiesta Club (Town & Country Plaza, Hammond; 1970s nightclub) - the club's logotype from its newspaper ad (IMG_7202/7203).
Pipeline B: Real-ESRGAN x4 (anime model) -> the bottom FIESTA Club lockup traced (the ad's own display letters and swirl
ornaments) with 'Town & Country Plaza' under it. Left off: the sombrero caricature mascot, the phone number, and the
week's band listing (performers' names)."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
from hmlib import remove_small, fill_small_holes, build_multi
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/fiesta"
INK = (34, 30, 30)
im = cv2.imread(f"{D}/f7202_x4.png").astype(np.float32); g = im.mean(2)
bg = cv2.GaussianBlur(cv2.dilate(g, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (161, 161))), (0, 0), 30)   # paper level (big solid letters would pull a blur down)
soft = cv2.GaussianBlur(np.clip((bg - g - 50) / 60.0, 0, 1), (0, 0), 1.4)
ink = remove_small(soft > 0.5, 90)
x0, y0, x1, y1 = 700, 1560, 2580, 2150
reg = ink[y0:y1, x0:x1].copy()
n, lab, st, _ = cv2.connectedComponentsWithStats(reg.astype(np.uint8), 8)
out = np.zeros_like(reg)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if x + w > 1880 - x0 and y + y0 > 2030: continue            # the phone number (bottom right)
    if x < 25: continue                                         # anything entering from the mascot side
    if (w > 1500 or h > 500) and a / (w * h) < 0.06: continue   # the ad frame rule (thin), not the lettering
    out[lab == i] = True
# Town & Country Plaza (x 315-1560) sits left of the box start: take it from its own band
tc = ink[2030:2150, 300:1600].copy()
n2, lab2, st2, _ = cv2.connectedComponentsWithStats(tc.astype(np.uint8), 8)
tcm = np.zeros_like(tc)
for i in range(1, n2):
    x, y, w, h, a = st2[i]
    if w < 300 and 18 < h < 110: tcm[lab2 == i] = True          # letters (not stray rule fragments)
canvas = np.zeros((y1 - y0 + 40, max(x1, 1600) - 300 + 40), bool)
canvas[0:y1 - y0, x0 - 300:x1 - 300] |= out
canvas[2030 - y0:2150 - y0, 0:1300] |= tcm
canvas = fill_small_holes(canvas, 50)
canvas = cv2.GaussianBlur(canvas.astype(np.float32), (0, 0), 1.0) > 0.5
canvas = np.pad(canvas, 40); ys, xs = np.where(canvas); canvas = canvas[ys.min() - 25:ys.max() + 26, xs.min() - 25:xs.max() + 26]
Hh, Ww = canvas.shape
build_multi([(canvas, INK)], Ww, Hh, 3000, f"{D}/fiesta_club_logo", turd=12)       # 10 in wide
print(Ww, Hh)
