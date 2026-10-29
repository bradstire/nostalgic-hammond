import numpy as np, json
from scipy.optimize import minimize
St, Sb = np.array([1774.0, 1472.0]), np.array([1867.0, 1819.0])
T = {'L': np.array([1264.0, 1600.0]), 'R': np.array([2346.0, 1656.0])}
out = json.load(open('enc_outline.json'))
def homog(src, dst):
    A = []
    for (X, Y, W), (x, y, w) in zip(src, dst):
        P = np.array([X, Y, W], float)
        A.append(np.r_[np.zeros(3), -w * P, y * P]); A.append(np.r_[w * P, np.zeros(3), -x * P])
    _, _, vt = np.linalg.svd(np.array(A)); return vt[-1].reshape(3, 3)
def Himg2plane(face, Vh):
    s = -1.0 if face == 'L' else 1.0
    Hp2i = homog([(0, -1, 1), (0, 1, 1), (s, 0, 1), (s, 0, 0)], [(*St, 1), (*Sb, 1), (*T[face], 1), (*Vh, 1)])
    return np.linalg.inv(Hp2i)
def apply(H, pts):
    P = np.c_[pts, np.ones(len(pts))] @ H.T; return P[:, :2] / P[:, 2:3]
def asym(face, Vh):
    H = Himg2plane(face, Vh)
    pts = np.array(out[face]); pts = pts[pts[:, 0] > 1300] if face == 'L' else pts
    q = apply(H, pts); x = np.abs(q[:, 0]); y = q[:, 1]
    top, bot = q[y < 0], q[y > 0]
    xs = np.linspace(0.08, 0.85, 40); err = []
    for xv in xs:
        a = top[np.abs(np.abs(top[:, 0]) - xv) < 0.02]; b = bot[np.abs(np.abs(bot[:, 0]) - xv) < 0.02]
        if len(a) and len(b): err.append(a[:, 1].mean() + b[:, 1].mean())
    return np.mean(np.square(err)) if err else 1e9, len(err)
res = {}
for face, guess in (('L', (-2000.0, 1450.0)), ('R', (5000.0, 1800.0))):
    f = lambda v: asym(face, v)[0]
    best = None
    for gx in (np.linspace(-20000, 900, 40) if face == 'L' else np.linspace(2400, 30000, 40)):
        for gy in np.linspace(1000, 2600, 17):
            v = f((gx, gy))
            if best is None or v < best[0]: best = (v, (gx, gy))
    r = minimize(lambda v: f(v), best[1], method='Nelder-Mead', options=dict(xatol=1, fatol=1e-9, maxiter=4000))
    print(face, 'Vh', np.round(r.x, 1), 'asym rms', np.sqrt(r.fun).round(4), 'samples', asym(face, r.x)[1])
    res[face] = r.x.tolist()
json.dump(res, open('enc_Vh.json', 'w'))
