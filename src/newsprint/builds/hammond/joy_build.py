"""Joy Drive-In Theatre (Hammond, La.; opened 1968, closed 1992) — the Driver's Courtesy Pass as a print (IMG_7188).
Pipeline B: Real-ESRGAN x4 -> traced type for every clean line (the pass is set in a Memphis/Stymie-style slab family);
'- This Pass Not Transferable -' re-typeset (the manager's signature runs through it) in TeX Gyre Schola Bold (GUST).
Left off: the phone number (reassigned numbers) and the signature (a private person's). Beaded border and fill-in
rules redrawn as clean vector at the card's proportions."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from hmlib import remove_small, fill_small_holes, build_multi, disk
from newsprint import render_text, roughen
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/joy"
INK, CARD = (34, 31, 30), (241, 232, 200)
im = cv2.imread(f"{D}/joy_x4.png").astype(np.float32); gray = im.mean(2)
bg = cv2.GaussianBlur(gray, (0, 0), 50)
ink = gray < bg - 55
ink = fill_small_holes(remove_small(cv2.morphologyEx(ink.astype(np.uint8), cv2.MORPH_OPEN, disk(1)) > 0, 120), 80)
K = 4                                                   # crop px -> x4 px
def cut(x0, y0, x1, y1, keep_small=False):
    m = ink[y0 * K:y1 * K, x0 * K:x1 * K].copy()
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n > 1 and not keep_small:
        hmax = st[1:, 3].max()
        for i in range(1, n):                            # drop slivers of the neighbouring line caught by the box
            if (st[i, 1] == 0 or st[i, 1] + st[i, 3] >= m.shape[0]) and st[i, 3] < 0.45 * hmax: m[lab == i] = False
    ys, xs = np.where(m); return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
L_courtesy = cut(255, 145, 595, 183)
L_joy = cut(170, 185, 685, 235)
L_hammond = cut(185, 233, 399, 266, keep_small=True)   # "Hammond, La." (the "- Phone 345-4433" is left off)
L_admit = cut(235, 270, 620, 318)
L_issued = cut(132, 333, 272, 368)
L_void = cut(132, 383, 294, 418)
L_by = cut(132, 457, 182, 492)
# re-typeset the bottom line (signature runs through it)
a, (x0, y0, x1, y1) = render_text("— This Pass Not Transferable —", "texgyreschola-bold.otf", 300, None, 0.0)
nt = a[y0:y1, x0:x1]
s = (L_hammond.shape[0] * 0.88) / nt.shape[0]          # cap-height match to the small lines
nt = roughen(np.pad(cv2.resize(nt, (int(nt.shape[1] * s), int(nt.shape[0] * s)), interpolation=cv2.INTER_AREA), 8).astype(np.float32), 1.2, 0.12)
ys, xs = np.where(nt); nt = nt[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

# ---- compose at x4 crop scale, using the card's own positions ----
Wc, Hc = (790 - 70) * K, (585 - 80) * K; ox, oy = 70 * K, 80 * K
c = np.zeros((Hc, Wc), bool)
def place(m, cx=None, x=None, ybase=None, ytop=None):
    xx = int(cx * K - ox - m.shape[1] / 2) if cx is not None else int(x * K - ox)
    yy = int(ytop * K - oy) if ytop is not None else int(ybase * K - oy - m.shape[0])
    c[yy:yy + m.shape[0], xx:xx + m.shape[1]] |= m
CX = 428                                                # card centre (crop px)
place(L_courtesy, cx=CX, ytop=150)
place(L_joy, cx=CX, ytop=190)
place(L_hammond, cx=CX, ytop=238)
place(L_admit, cx=CX, ytop=276)
place(L_issued, x=136, ybase=364); place(L_void, x=136, ybase=414); place(L_by, x=136, ybase=488)
place(nt, cx=CX + 6, ytop=503)
cc = c.astype(np.uint8)
RULE = int(2.2 * K)
for xs_, y in ((272, 357), (294, 406), (182, 481)):     # fill-in rules (start after the label)
    cv2.line(cc, ((xs_ + 3) * K - ox, y * K - oy), (718 * K - ox, y * K - oy), 1, RULE)
# beaded border: thin rule with round beads every ~9 crop px, as printed
x0b, y0b, x1b, y1b = 106 * K - ox, 120 * K - oy, 752 * K - ox, 545 * K - oy
cv2.rectangle(cc, (x0b, y0b), (x1b, y1b), 1, int(1.6 * K))
step = 9.0 * K; br = int(2.3 * K)
for (xa, ya, xb, yb) in ((x0b, y0b, x1b, y0b), (x0b, y1b, x1b, y1b), (x0b, y0b, x0b, y1b), (x1b, y0b, x1b, y1b)):
    n = int(round(max(abs(xb - xa), abs(yb - ya)) / step))
    for i in range(n + 1):
        t = i / n; cv2.circle(cc, (int(xa + (xb - xa) * t), int(ya + (yb - ya) * t)), br, 1, -1)
c = cc > 0
card = np.zeros_like(c); cv2.rectangle(card.view(np.uint8), (x0b - 40 * K, y0b - 38 * K), (x1b + 40 * K, y1b + 38 * K), 1, -1)
card = card.astype(bool) & ~c
ys, xs = np.where(c | card); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
c, card = c[y0:y1, x0:x1], card[y0:y1, x0:x1]
Hh, Ww = c.shape
build_multi([(c, INK)], Ww, Hh, 2700, f"{D}/joy_pass_ink")                     # 9 in wide, natural/cream/white tees
build_multi([(card, CARD), (c, INK)], Ww, Hh, 2700, f"{D}/joy_pass_card")       # with the cream card (any tee colour)
print(Ww, Hh)
