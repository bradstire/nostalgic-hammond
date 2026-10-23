"""Toggery Shop — embroidery hat front from the ad logotype (traced). Small 'the' + its left flourish left off:
at hat size the 'the' sits at ~0.16 in x-height and its e-eye closes when stitched. Printful dad hat front <= 5.5 x 2.0 in."""
import sys, numpy as np, cv2
from PIL import Image
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/lib"); sys.path.insert(0, f"{HB}/hats")
from build_v3 import prep, fit, smooth, THREAD, DPI, GAP, enforce_gaps, bridge_gaps
from embcheck import check
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/toggery"
m0 = np.load(f"{D}/logo_mask.npy")
n, lab, st, _ = cv2.connectedComponentsWithStats(m0.astype(np.uint8), 8)
drop = [i for i in range(1, n) if (1350 < st[i, 0] < 1750 and st[i, 1] < 120 and st[i, 3] < 300) or (st[i, 0] < 700 and st[i, 1] < 140 and st[i, 2] > 600)]
m = m0 & ~np.isin(lab, drop)
ys, xs = np.where(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
m = fit(m, w_in=4.6, h_in=1.92)
m = prep(m); m = smooth(m); m = enforce_gaps(m, GAP)     # where two letters come closer than 0.06 in, the smaller is trimmed back
ys, xs = np.where(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
sc = m.shape[0] / 1558
r = check(m, "front", [("Toggery Shop", 348 * sc / DPI, m.shape[1] / DPI)])
for thread in ("maroon", "white"):
    c = THREAD[thread]; rgba = np.zeros((*m.shape, 4), np.uint8)
    rgba[m, :3] = [int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)]; rgba[m, 3] = 255
    Image.fromarray(rgba, "RGBA").save(f"{D}/hat_toggery_{thread}.png", dpi=(DPI, DPI))
print("PASS" if r["pass"] else "CHECK", r, "dropped", drop)
