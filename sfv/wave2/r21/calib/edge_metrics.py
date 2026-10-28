"""Edge metrics for traced lettering at print size (masters are 300 ppi at print size).
For each lettering box: every outline of the ink mask (outer edges and counters) is resampled at 1 px and compared
at two scales. Reported per region:
  wobble_mil   median distance between the outline lightly smoothed (sigma 1.5 px, removes pixel stairs) and the
               same outline smoothed at 0.03 in (sigma 9 px): the waviness a viewer reads as 'hand' or 'rough', in 1/1000 in.
               Corners (turn > 35 deg within +-0.02 in) are left out so a sharp serif isn't counted as wobble.
  wobble_p90   90th percentile of the same distance (how bad the worst stretches get).
  infl_per_in  curvature sign changes per inch of outline (above a small dead band): how often an edge changes
               direction. A font outline ~ 2-4; a raw photo trace 15+.
  speck_n      separate ink pieces under 0.02 in square inside the box (dust left in).
Usage: edge_metrics.py regions.json out.json"""
import json, sys, math
import numpy as np, cv2
from PIL import Image
from scipy.ndimage import gaussian_filter1d

PPI = 300.0


def contour_metrics(c):
    c = c[:, 0, :].astype(float)
    if len(c) < 60:
        return None
    # uniform resample at 1 px
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([c, c[:1]]), axis=0).T))]
    L = d[-1]
    if L < 0.3 * PPI:
        return None
    t = np.arange(0, L, 1.0)
    cc = np.vstack([c, c[:1]])
    x = np.interp(t, d, cc[:, 0]); y = np.interp(t, d, cc[:, 1])
    p1x, p1y = gaussian_filter1d(x, 1.5, mode='wrap'), gaussian_filter1d(y, 1.5, mode='wrap')
    p2x, p2y = gaussian_filter1d(x, 9, mode='wrap'), gaussian_filter1d(y, 9, mode='wrap')
    dev = np.hypot(p1x - p2x, p1y - p2y)
    # corners: direction change over +-6 px on the lightly smoothed outline
    k = 6
    ang = np.arctan2(np.roll(p1y, -k) - p1y, np.roll(p1x, -k) - p1x)
    angb = np.arctan2(p1y - np.roll(p1y, k), p1x - np.roll(p1x, k))
    turn = np.abs((ang - angb + np.pi) % (2 * np.pi) - np.pi)
    corner = turn > math.radians(35)
    corner = np.convolve(corner.astype(float), np.ones(2 * k + 1), mode='same') > 0
    keep = ~corner
    # curvature on sigma-3 outline
    sx, sy = gaussian_filter1d(x, 3, mode='wrap'), gaussian_filter1d(y, 3, mode='wrap')
    dx, dy = np.gradient(sx), np.gradient(sy); ddx, ddy = np.gradient(dx), np.gradient(dy)
    kap = (dx * ddy - dy * ddx) / np.maximum((dx * dx + dy * dy) ** 1.5, 1e-9)
    band = 1 / 60.0                                    # dead band: radius > 60 px (0.2 in) counts as straight
    s = np.where(kap > band, 1, np.where(kap < -band, -1, 0))
    s = s[s != 0]
    infl = int((s[1:] != s[:-1]).sum()) if len(s) > 1 else 0
    return dict(L=L, dev=dev[keep], infl=infl)


def region(path, box, color=None):
    im = np.asarray(Image.open(path).convert('RGBA'))
    x0, y0, x1, y1 = [int(v) for v in box]
    s = im[max(0, y0):y1, max(0, x0):x1]
    m = s[..., 3] > 128
    if color is not None:
        m &= np.abs(s[..., :3].astype(int) - np.array(color)).sum(2) < 40
    m = m.astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    devs, L, infl, specks = [], 0.0, 0, 0
    for c in cs:
        a = cv2.contourArea(c)
        if a < (0.02 * PPI) ** 2:
            specks += 1
            continue
        r = contour_metrics(c)
        if r is None:
            continue
        devs.append(r['dev']); L += r['L']; infl += r['infl']
    dev = np.concatenate(devs) if devs else np.zeros(1)
    mil = 1000.0 / PPI
    return dict(wobble_mil=round(float(np.median(dev)) * mil, 2), wobble_p90=round(float(np.percentile(dev, 90)) * mil, 2),
                infl_per_in=round(infl / (L / PPI), 2) if L else 0, outline_in=round(L / PPI, 1), speck_n=specks)


if __name__ == '__main__':
    regs = json.load(open(sys.argv[1]))
    out = []
    for r in regs:
        m = region(r['file'], r['box'], r.get('color'))
        m.update(town=r['town'], design=r['design'], what=r['what'], kind=r.get('kind', ''))
        out.append(m)
        print(f"{r['town']:12s} {r['design']:26s} {r['what'][:34]:34s} wobble {m['wobble_mil']:5.2f} mil  p90 {m['wobble_p90']:5.2f}  infl/in {m['infl_per_in']:6.2f}  specks {m['speck_n']:3d}  ({m['outline_in']} in)")
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
