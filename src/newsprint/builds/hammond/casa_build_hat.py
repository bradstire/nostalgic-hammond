"""Casa de Fresa — embroidery hat front (Printful dad hat 6245CM: front <= 5.5 x 2.0 in, letters >= 0.25 in,
details >= 0.05 in, Printful thread palette). The matchbook's own lettering (traced), levelled (the matchbook sets it
on a ~7.6 deg rise), 'CASA de FRESA' on one line (two lines would put 'de' under 0.25 in). Red thread #CC3333 on a stone/khaki or white hat."""
import sys, numpy as np, cv2
from PIL import Image
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/lib"); sys.path.insert(0, f"{HB}/hats")
from build_v3 import prep, fit, smooth, respace, THREAD, DPI, GAP
from embcheck import check
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/casa"

L = np.load(f"{D}/panel_letters.npy")
n, lab, st, _ = cv2.connectedComponentsWithStats(L.astype(np.uint8), 8)
big = [i for i in range(1, n) if st[i, 4] > 5000]
top = np.isin(lab, [i for i in big if st[i, 1] < 1300])            # CASA de FRESA
bot = np.isin(lab, [i for i in big if st[i, 1] >= 1300])           # hotel
def level(m, ang=-7.6):
    ys, xs = np.where(m); m = m[ys.min() - 50:ys.max() + 51, xs.min() - 50:xs.max() + 51].astype(np.uint8) * 255
    h, w = m.shape; M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
    c, s_ = abs(M[0, 0]), abs(M[0, 1]); nw, nh = int(h * s_ + w * c) + 4, int(h * c + w * s_) + 4
    M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
    r = cv2.warpAffine(m, M, (nw, nh)) > 127; ys, xs = np.where(r); return r[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
# level both lines together so 'hotel' keeps its place under the name
both = level(top | bot)
n2, lab2, st2, _ = cv2.connectedComponentsWithStats(both.astype(np.uint8), 8)
ytop = np.isin(lab2, [i for i in range(1, n2) if st2[i, 1] + st2[i, 3] / 2 < both.shape[0] * 0.62])
name, hotel = both & ytop, both & ~ytop
crop = lambda a: a[np.where(a.any(1))[0].min():np.where(a.any(1))[0].max() + 1, np.where(a.any(0))[0].min():np.where(a.any(0))[0].max() + 1]
gap_rows = np.where(hotel.any(1))[0].min() - np.where(name.any(1))[0].max()
name, hotel = crop(name), crop(hotel)
# 'hotel' centred under 'de FRESA' as on the matchbook: keep the traced horizontal offset
nx0 = np.where(both.any(0))[0].min()
hx = np.where((both & ~ytop).any(0))[0].min() - nx0
gap = max(int(0.10 * name.shape[0] / 0.95 * 0), 0)
# single line: at hat size the two-line lockup puts 'de' under 0.25 in; the name alone runs 4.8 in wide
m = fit(name, w_in=4.7)
m = respace(prep(m), GAP)                 # every letter >= 0.06 in apart (stitch merge), strokes >= 0.05 in
if m.shape[1] > 5.3 * DPI: m = fit(m, w_in=5.3)
m = smooth(m); ys, xs = np.where(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
s = m.shape[0] / name.shape[0]
de_h = 203 * (m.shape[1] / name.shape[1]) / DPI; cap_h = 620 * (m.shape[1] / name.shape[1]) / DPI
r = check(m, "front", [("CASA FRESA", cap_h, m.shape[1] / DPI), ("de", de_h, 0.5)])
for thread in ("red", "white"):
    c = THREAD[thread]; rgba = np.zeros((*m.shape, 4), np.uint8)
    rgba[m, :3] = [int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)]; rgba[m, 3] = 255
    Image.fromarray(rgba, "RGBA").save(f"{D}/hat_casadefresa_{thread}.png", dpi=(DPI, DPI))
print("PASS" if r["pass"] else "CHECK", r)
