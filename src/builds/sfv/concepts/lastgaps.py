"""Finish S9 GAPS/COUNTERS after gatefix + unsplit without splitting shapes: a near-touch across empty ground is
bridged with a slim closing; across another ink, that separating ink is widened 1 px per pass into this ink."""
import sys, numpy as np, cv2
from PIL import Image; from scipy import ndimage
sys.path.insert(0, '/home/claude/print-assets/toolkit'); import art_qa as A
src, out, width_in = sys.argv[1], sys.argv[2], float(sys.argv[3])
a = np.array(Image.open(src).convert('RGBA')); ppi = a.shape[1] / width_in
op = a[..., 3] > 128
cols = [tuple(int(v) for v in c) for c, n in zip(*np.unique(a[op][:, :3].reshape(-1, 3), axis=0, return_counts=True)) if n > 50]
yy, xx = np.ogrid[:a.shape[0], :a.shape[1]]
def paint(m, c): a[m, :3] = c; a[m, 3] = 255
for it in range(10):
    op = a[..., 3] > 128; L = {c: op & np.all(a[..., :3] == c, -1) for c in cols}
    excl = A.halftone_zone(op, ppi); todo = []
    for c in cols:
        gs, _ = A.check_gaps(L[c], ppi, excl, (0.025 * ppi) ** 2); todo += [(c, g) for g in gs]
    cs, bad = A.check_counters(op, ppi, excl)
    for c in cols:
        cs2, bad2 = A.check_counters(L[c], ppi, excl); cs += cs2; bad |= bad2
    if bad.any():
        d = np.stack([ndimage.distance_transform_edt(~L[c]) for c in cols]); best = np.argmin(d, 0)
        for i, c in enumerate(cols): paint(bad & (best == i), c)
    print(it, 'gaps', len(todo), 'counters', len(cs), flush=True)
    if not todo and not cs: break
    for c, g in todo:
        y, x = g['y'], g['x']; d = (yy - y) ** 2 + (xx - x) ** 2 <= 30 * 30
        op = a[..., 3] > 128; L = {k: op & np.all(a[..., :3] == k, -1) for k in cols}
        k = int(np.ceil(g['floor_in'] * ppi / 2)) + 1
        cl = cv2.morphologyEx(L[c].astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))) > 0
        emp = cl & ~op & d
        if emp.any(): paint(emp, c); continue
        between = cl & ~L[c] & d                     # the other ink sitting in the gap
        others = [o for o in cols if o != c]
        if not others or not between.any(): continue
        sep = max(others, key=lambda o: (between & L[o]).sum())
        grow = (cv2.dilate(L[sep].astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & L[c] & d
        paint(grow, sep)
Image.fromarray(a, 'RGBA').save(out, dpi=(300, 300))
