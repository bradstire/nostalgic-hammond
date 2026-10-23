"""Levelled 'CASA de FRESA' lettering mask from the traced matchbook panel (shared by hat + sock back)."""
import numpy as np, cv2
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/casa"
def name_mask(ang=-7.6):
    L = np.load(f"{D}/panel_letters.npy")
    n, lab, st, _ = cv2.connectedComponentsWithStats(L.astype(np.uint8), 8)
    top = np.isin(lab, [i for i in range(1, n) if st[i, 4] > 5000 and st[i, 1] < 1300])
    ys, xs = np.where(top); m = top[ys.min() - 50:ys.max() + 51, xs.min() - 50:xs.max() + 51].astype(np.uint8) * 255
    h, w = m.shape; M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
    c, s_ = abs(M[0, 0]), abs(M[0, 1]); nw, nh = int(h * s_ + w * c) + 4, int(h * c + w * s_) + 4
    M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
    r = cv2.warpAffine(m, M, (nw, nh)) > 127; ys, xs = np.where(r); return r[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
