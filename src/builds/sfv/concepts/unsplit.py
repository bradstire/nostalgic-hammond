"""After gatefix: revert the ink-over-ink bridges that split a shape of the source master (S9 SURVIVAL),
one blob at a time, keeping every bridge that splits nothing."""
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, '/home/claude/print-assets/toolkit'); import art_qa as Q
src, fixed, out, width_in = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
A = np.array(Image.open(src).convert('RGBA')); B = np.array(Image.open(fixed).convert('RGBA'))
ppi = B.shape[1] / width_in
chg = (A[..., 3] > 128) & (B[..., 3] > 128) & np.any(A[..., :3] != B[..., :3], -1)
lab, n = ndimage.label(chg, structure=np.ones((3, 3)))
score = lambda s: sum(max(0, x["pieces"] - 1) + (x["area_kept"] < 0.8) for x in s)
base = Q.survival(src, B, ppi, [])
print("blobs", n, "survival fails", len(base), "score", score(base))
def fails_near(cur, boxes):
    return len(Q.survival(src, cur, ppi, []))
cur = B.copy(); nb = score(base)
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    m = lab[sl] == i
    trial = cur.copy(); t = trial[sl]; t[m] = A[sl][m]; trial[sl] = t
    nf = score(Q.survival(src, trial, ppi, []))
    if nf < nb:
        cur = trial; nb = nf; print('reverted blob', i, 'at', sl[1].start, sl[0].start, '->', nf, flush=True)
        if nb == 0: break
Image.fromarray(cur, 'RGBA').save(out, dpi=(300, 300)); print('done, survival fails', nb)
