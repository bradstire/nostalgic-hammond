"""Galaxy Drive-In Theatre (309 Natchez St., Hammond; the Joy Twin Drive-In's later name; closed 1992) - the Courtesy Pass
as a print (IMG_7188, lower card; same photo as the Joy pass). Pipeline B: Real-ESRGAN x4 -> every printed line traced
(Palatino-style caps, the brush-script 'galaxy drive in theatre', the address line, the fill-in labels). Left off: the phone
number (its line is closed up). Fill-in rules redrawn level as clean vector (the card has curled ~0.8 deg); card outline is
a clean rectangle at the card's proportions."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
from hmlib import remove_small, fill_small_holes, build_multi
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/galaxy"
INK, CARD = (34, 31, 30), (241, 232, 200)
im = cv2.imread(f"{D}/galaxy_x4.png").astype(np.float32); g = im.mean(2)
bg = cv2.GaussianBlur(g, (0, 0), 60)
soft = np.clip((bg - g - 35) / 50.0, 0, 1)                     # soft ink coverage (edge-preserving for the trace)
soft = cv2.GaussianBlur(soft, (0, 0), 1.6)
ink = remove_small(soft > 0.5, 150)
ink[:, :200] = False; ink[:, 3150:] = False; ink[:200] = False; ink[1850:] = False
ink = fill_small_holes(ink, 60)

def comps(m):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8); return n, lab, st
H, W = ink.shape; c = np.zeros_like(ink)
c[370:550] |= ink[370:550]                                      # COURTESY PASS
band = ink[585:1015].copy(); n, lab, st = comps(band)
addr = np.zeros_like(band); script = np.zeros_like(band)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if y + 585 >= 893 and h < 130 and x > 700: addr[lab == i] = True     # address line glyphs (incl. the bullet)
    else: script[lab == i] = True
c[585:1015] |= script | addr
LAB_SHIFT = 120                                                  # phone line (y 1082-1171) left off: close the gap
lab_exp = ink[1250:1375, 300:770]; lab_app = ink[1480:1610, 300:840]
c[1250 - LAB_SHIFT:1375 - LAB_SHIFT, 300:770] |= lab_exp
c[1480 - LAB_SHIFT:1610 - LAB_SHIFT, 300:840] |= lab_app
cc = c.astype(np.uint8)
RULE = 9
cv2.line(cc, (781, 1350 - LAB_SHIFT), (2990, 1350 - LAB_SHIFT), 1, RULE)    # level, at the rule's own start (label baseline)
cv2.line(cc, (905, 1585 - LAB_SHIFT), (2990, 1585 - LAB_SHIFT), 1, RULE)
c = cc > 0
# card: the pass's own rectangle (view x 30-1070, y 40-635 -> x4), shortened by the closed-up line
x0, y0, x1, y1 = 90, 120, 3210, 1905 - LAB_SHIFT
card = np.zeros_like(c); card[y0:y1, x0:x1] = True
pad = 30
sl = (slice(y0 - pad, y1 + pad), slice(x0 - pad, x1 + pad))
inkc, cardc = c[sl], card[sl]
Hh, Ww = inkc.shape
build_multi([(cardc, CARD), (inkc, INK)], Ww, Hh, 2700, f"{D}/galaxy_pass_card")        # 9 in wide
ys, xs = np.where(inkc); ic = inkc[ys.min() - 20:ys.max() + 21, xs.min() - 20:xs.max() + 21]
build_multi([(ic, INK)], ic.shape[1], ic.shape[0], 2700, f"{D}/galaxy_pass_ink")
print(Ww, Hh, ic.shape)
