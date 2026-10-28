"""Scale-free edge metrics for traced lettering (masters at 300 ppi, print size).
Each lettering box -> letter mask (ink, or the holes when the letters are knocked out of a panel) ->
  sw          median stroke width, in (2 x distance-to-edge along the letter skeleton)
  rough_pct   90th-percentile distance between the outline lightly smoothed (removes pixel stairs) and the outline
              smoothed at 0.35 x stroke width, as % of the stroke width; corners excluded. How far an edge wanders
              from a clean stroke edge, relative to how heavy the stroke is: 'clean' ~ <4 %, 'hand' ~ 4-10 %, rough > 10 %.
  infl_100sw  curvature direction changes per 100 stroke-widths of outline: how busy the edge is.
  wobble_p90_mil  the same p90 distance with a fixed 0.03 in smoothing, in 1/1000 in (absolute, viewing-distance check).
Usage: edge_metrics2.py regions.json out.json [maskdir]"""
import json, sys, math, os
import numpy as np, cv2
from PIL import Image
from scipy.ndimage import gaussian_filter1d, distance_transform_edt
from skimage.morphology import skeletonize

PPI = 300.0


def letter_mask(path, box, color=None, invert=None):
    im = np.asarray(Image.open(path).convert('RGBA'))
    x0, y0, x1, y1 = [int(v) for v in box]
    s = im[max(0, y0):y1, max(0, x0):x1]
    m = s[..., 3] > 128
    if color is not None:
        m &= np.abs(s[..., :3].astype(int) - np.array(color)).sum(2) < 40
    if invert is None:
        invert = False
    if invert:
        from scipy import ndimage as nd
        yy, xx = np.mgrid[-25:26, -25:26]
        hull = nd.binary_fill_holes(nd.binary_closing(np.pad(m, 30), structure=(xx * xx + yy * yy) <= 625))[30:-30, 30:-30]
        m = hull & ~m
        lab, n = nd.label(m)
        if n:
            sz = nd.sum(m, lab, range(1, n + 1)); keep = np.zeros(n + 1, bool); keep[1:] = sz > (0.03 * PPI) ** 2
            m = keep[lab]
    return m, invert


def contour_dev(c, sl, ss):
    c = c[:, 0, :].astype(float)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(np.vstack([c, c[:1]]), axis=0).T))]
    L = d[-1]
    if L < 4 * sl:
        return None
    t = np.arange(0, L, 1.0)
    cc = np.vstack([c, c[:1]])
    x = np.interp(t, d, cc[:, 0]); y = np.interp(t, d, cc[:, 1])
    p1x, p1y = gaussian_filter1d(x, ss, mode='wrap'), gaussian_filter1d(y, ss, mode='wrap')
    p2x, p2y = gaussian_filter1d(x, sl, mode='wrap'), gaussian_filter1d(y, sl, mode='wrap')
    dev = np.hypot(p1x - p2x, p1y - p2y)
    k = max(4, int(round(sl * 0.7)))
    ang = np.arctan2(np.roll(p1y, -k) - p1y, np.roll(p1x, -k) - p1x)
    angb = np.arctan2(p1y - np.roll(p1y, k), p1x - np.roll(p1x, k))
    turn = np.abs((ang - angb + np.pi) % (2 * np.pi) - np.pi)
    corner = np.convolve((turn > math.radians(35)).astype(float), np.ones(2 * k + 1), mode='same') > 0
    sx, sy = gaussian_filter1d(x, max(ss, 2.0), mode='wrap'), gaussian_filter1d(y, max(ss, 2.0), mode='wrap')
    dx, dy = np.gradient(sx), np.gradient(sy); ddx, ddy = np.gradient(dx), np.gradient(dy)
    kap = (dx * ddy - dy * ddx) / np.maximum((dx * dx + dy * dy) ** 1.5, 1e-9)
    band = 1 / (3.0 * sl / 0.35)                         # radius > 3 stroke widths counts as straight
    s = np.where(kap > band, 1, np.where(kap < -band, -1, 0)); s = s[s != 0]
    infl = int((s[1:] != s[:-1]).sum()) if len(s) > 1 else 0
    return dev[~corner], L, infl


def measure(m):
    dt = distance_transform_edt(m)
    sk = skeletonize(m)
    sw = float(np.median(dt[sk]) * 2) if sk.any() else 0
    sl, ss = 0.35 * sw, max(1.5, 0.03 * sw)
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    devs, L, infl, devabs = [], 0, 0, []
    for c in cs:
        if cv2.contourArea(c) < (0.02 * PPI) ** 2:
            continue
        r = contour_dev(c, sl, ss)
        if r is None:
            continue
        devs.append(r[0]); L += r[1]; infl += r[2]
        r2 = contour_dev(c, 9.0, 1.5)
        if r2 is not None:
            devabs.append(r2[0])
    dev = np.concatenate(devs) if devs else np.zeros(1)
    da = np.concatenate(devabs) if devabs else np.zeros(1)
    return dict(sw_in=round(sw / PPI, 3), rough_pct=round(float(np.percentile(dev, 90)) / sw * 100, 1) if sw else 0,
                infl_100sw=round(infl / (L / sw) * 100, 1) if L and sw else 0,
                wobble_p90_mil=round(float(np.percentile(da, 90)) * 1000 / PPI, 2), outline_in=round(L / PPI, 1))


if __name__ == '__main__':
    regs = json.load(open(sys.argv[1])); md = sys.argv[3] if len(sys.argv) > 3 else None
    out = []
    for r in regs:
        m, inv = letter_mask(r['file'], r['box'], r.get('color'), r.get('invert'))
        if md:
            os.makedirs(md, exist_ok=True)
            Image.fromarray((~m * 255).astype(np.uint8)).save(os.path.join(md, (r['design'] + '_' + r['what'])[:60].replace('/', '_').replace(' ', '_') + '.png'))
        q = measure(m); q.update(town=r['town'], design=r['design'], what=r['what'], knockout=bool(inv)); out.append(q)
        print(f"{r['town']:12s} {r['design']:24s} {r['what'][:30]:30s} sw {q['sw_in']:.3f} in  rough {q['rough_pct']:5.1f} %sw  infl {q['infl_100sw']:5.1f} /100sw  wob90 {q['wobble_p90_mil']:5.2f} mil {'(knockout)' if inv else ''}")
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
