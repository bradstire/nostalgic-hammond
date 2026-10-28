import json, sys, math, numpy as np, cv2
sys.path.insert(0, '.')
import edge_metrics2 as e2
from scipy.ndimage import gaussian_filter1d
def micro(m, sl=6.0, ss=1.2):
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    devs = []
    for c in cs:
        if cv2.contourArea(c) < 36: continue
        c = c[:, 0, :].astype(float)
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([c, c[:1]]), axis=0).T))]; L = d[-1]
        if L < 60: continue
        t = np.arange(0, L, 1.0); cc = np.vstack([c, c[:1]])
        x = np.interp(t, d, cc[:, 0]); y = np.interp(t, d, cc[:, 1])
        p1 = np.c_[gaussian_filter1d(x, ss, mode='wrap'), gaussian_filter1d(y, ss, mode='wrap')]
        p2 = np.c_[gaussian_filter1d(x, sl, mode='wrap'), gaussian_filter1d(y, sl, mode='wrap')]
        # local curvature radius on p2: exclude tight curves (R < 0.06 in) and corners
        dx, dy = np.gradient(p2[:, 0]), np.gradient(p2[:, 1]); ddx, ddy = np.gradient(dx), np.gradient(dy)
        kap = np.abs(dx * ddy - dy * ddx) / np.maximum((dx * dx + dy * dy) ** 1.5, 1e-9)
        k = 8
        a1 = np.arctan2(np.roll(p1[:, 1], -k) - p1[:, 1], np.roll(p1[:, 0], -k) - p1[:, 0])
        a0 = np.arctan2(p1[:, 1] - np.roll(p1[:, 1], k), p1[:, 0] - np.roll(p1[:, 0], k))
        turn = np.abs((a1 - a0 + np.pi) % (2 * np.pi) - np.pi)
        bad = (turn > math.radians(30)) | (kap > 1 / 18.0)
        bad = np.convolve(bad.astype(float), np.ones(2 * k + 1), mode='same') > 0
        dv = np.hypot(*(p1 - p2).T)[~bad]
        devs.append(dv)
    dv = np.concatenate(devs) if devs else np.zeros(1)
    return float(np.median(dv)) * 1000 / 300, float(np.percentile(dv, 90)) * 1000 / 300
for fn in sys.argv[1:]:
    for r in json.load(open(fn)):
        m, _ = e2.letter_mask(r['file'], r['box'], r.get('color'), r.get('invert'))
        a, b = micro(m)
        print(f"{r['town']:12s} {r['design'][:22]:22s} {r['what'][:30]:30s} micro p50 {a:5.2f} mil  p90 {b:5.2f} mil")
