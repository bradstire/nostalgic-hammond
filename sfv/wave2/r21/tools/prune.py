import numpy as np
from scipy import ndimage as nd
K8 = np.ones((3, 3), int)
def endpoints(S):
    n = nd.convolve(S.astype(int), K8, mode='constant') - S
    return S & (n == 1)
def prune(S, k):
    S = S.astype(bool); P = S.copy()
    for _ in range(k):
        P &= ~endpoints(P)
    for _ in range(k):
        E = endpoints(P)
        grow = nd.binary_dilation(E, structure=np.ones((3, 3))) & S & ~P
        if not grow.any(): break
        P |= grow
    return P


def straighten(S, max_dev=6.0, min_len=50):
    """Replace nearly straight skeleton branches with their fitted line (channel tubes are straight where the
    letter is straight; the wiggle is capture). Curved branches (P bowl, S...) are left as traced."""
    import cv2
    S = S.astype(bool)
    n = nd.convolve(S.astype(int), K8, mode='constant') - S
    junc = S & (n > 2)
    jd = nd.binary_dilation(junc, structure=np.ones((3, 3)))
    seg = S & ~jd
    lab, k = nd.label(seg, structure=np.ones((3, 3)))
    out = S.copy()
    for i in range(1, k + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_len:
            continue
        P = np.c_[xs, ys].astype(float); c = P.mean(0)
        u, s_, vt = np.linalg.svd(P - c, full_matrices=False)
        d = vt[0]; nrm = np.array([-d[1], d[0]])
        dev = np.abs((P - c) @ nrm)
        if dev.max() > max_dev:
            continue
        t = (P - c) @ d
        a, b = c + d * t.min(), c + d * t.max()
        out[lab == i] = False
        img = np.zeros(S.shape, np.uint8)
        cv2.line(img, (int(round(a[0])), int(round(a[1]))), (int(round(b[0])), int(round(b[1]))), 1, 1)
        out |= img.astype(bool)
    return out
