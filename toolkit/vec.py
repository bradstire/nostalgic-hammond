"""Vector-cleanup helpers for traced print masters.
smooth_mask: re-draws a binary mask from Gaussian-smoothed contours (removes trace wobble, keeps letterforms).
"""
import numpy as np, cv2
from scipy.ndimage import gaussian_filter1d

def _resample(c, step=2.0):
    c = c.reshape(-1, 2).astype(float)
    c = np.vstack([c, c[:1]])
    seg = np.hypot(*np.diff(c, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    L = s[-1]
    if L < step * 6:
        return c[:-1]
    t = np.arange(0, L, step)
    return np.stack([np.interp(t, s, c[:, 0]), np.interp(t, s, c[:, 1])], 1)

def smooth_mask(mask, sigma_px=10, step=2.0, ss=4, min_area=40):
    """mask: bool HxW. sigma_px: smoothing length along the outline in pixels."""
    H, W = mask.shape
    m8 = (mask.astype(np.uint8) * 255)
    cs, hier = cv2.findContours(m8, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = np.zeros((H * ss, W * ss), np.uint8)
    if hier is None:
        return mask.copy()
    hier = hier[0]
    sig = sigma_px / step
    polys_outer, polys_hole = [], []
    for i, c in enumerate(cs):
        if cv2.contourArea(c) < min_area:
            continue
        p = _resample(c, step)
        if len(p) > 8:
            p = np.stack([gaussian_filter1d(p[:, 0], sig, mode='wrap'),
                          gaussian_filter1d(p[:, 1], sig, mode='wrap')], 1)
        pts = np.round(p * ss).astype(np.int32).reshape(-1, 1, 2)
        (polys_hole if hier[i][3] >= 0 else polys_outer).append(pts)
    cv2.fillPoly(out, polys_outer, 255, lineType=cv2.LINE_8)
    cv2.fillPoly(out, polys_hole, 0, lineType=cv2.LINE_8)
    out = cv2.resize(out, (W, H), interpolation=cv2.INTER_AREA)
    return out >= 128

def roughness(mask, sigma_px=10):
    """Ratio of traced perimeter to smoothed perimeter (1.0 = perfectly clean)."""
    def per(m):
        cs, _ = cv2.findContours(m.astype(np.uint8) * 255, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        return sum(cv2.arcLength(c, True) for c in cs if cv2.contourArea(c) > 40)
    p0 = per(mask)
    p1 = per(smooth_mask(mask, sigma_px))
    return p0 / max(p1, 1)


def _turning(p, k):
    a = np.roll(p, k, axis=0) - p
    b = np.roll(p, -k, axis=0) - p
    ca = np.arctan2(a[:, 1], a[:, 0]); cb = np.arctan2(b[:, 1], b[:, 0])
    ang = np.abs(np.degrees(np.angle(np.exp(1j * (cb - ca)))))
    return 180 - ang          # 0 = straight, large = sharp corner


def smooth_mask_corners(mask, sigma_px=6, corner_deg=40, k_px=None, step=1.0, ss=4, min_area=30):
    """Corner-preserving cleanup of traced outlines: corners (serif tips, stem/bar junctions) are detected by
    turning angle and pinned; each run between corners is Gaussian-smoothed with its ends fixed. Slabs stay
    sharp, stems/bowls lose the trace wobble."""
    H, W = mask.shape
    m8 = (mask.astype(np.uint8) * 255)
    cs, hier = cv2.findContours(m8, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    out = np.zeros((H * ss, W * ss), np.uint8)
    if hier is None:
        return mask.copy()
    hier = hier[0]
    k = k_px or max(3, int(sigma_px * 1.2))
    outer, holes = [], []
    for i, c in enumerate(cs):
        if cv2.contourArea(c) < min_area:
            continue
        p = _resample(c, step)
        n = len(p)
        if n < 4 * k:
            q = p
        else:
            t = _turning(p, k)
            # local maxima of turning above threshold = corners
            cand = np.nonzero(t > corner_deg)[0]
            corners = []
            for j in cand:
                lo, hi = j - k, j + k
                idx = np.arange(lo, hi + 1) % n
                if t[j] >= t[idx].max():
                    if not corners or (j - corners[-1]) > k:
                        corners.append(j)
            if len(corners) < 2:
                q = np.stack([gaussian_filter1d(p[:, 0], sigma_px / step, mode='wrap'),
                              gaussian_filter1d(p[:, 1], sigma_px / step, mode='wrap')], 1)
            else:
                q = p.copy()
                cc = corners + [corners[0] + n]
                for a_, b_ in zip(cc[:-1], cc[1:]):
                    idx = np.arange(a_, b_ + 1) % n
                    seg = p[idx]
                    if len(seg) < 5:
                        continue
                    # smooth with ends pinned: subtract the chord, smooth the residual with reflected padding
                    t_ = np.linspace(0, 1, len(seg))[:, None]
                    chord = seg[0] * (1 - t_) + seg[-1] * t_
                    r = seg - chord
                    pad = min(len(seg) - 1, int(3 * sigma_px / step))
                    rp = np.vstack([-r[pad:0:-1], r, -r[-2:-pad - 2:-1]]) if pad > 0 else r
                    rs = np.stack([gaussian_filter1d(rp[:, 0], sigma_px / step), gaussian_filter1d(rp[:, 1], sigma_px / step)], 1)
                    rs = rs[pad:pad + len(seg)] if pad > 0 else rs
                    rs[0] = 0; rs[-1] = 0
                    q[idx[1:-1]] = (chord + rs)[1:-1]
        pts = np.round(q * ss).astype(np.int32).reshape(-1, 1, 2)
        (holes if hier[i][3] >= 0 else outer).append(pts)
    cv2.fillPoly(out, outer, 255)
    cv2.fillPoly(out, holes, 0)
    out = cv2.resize(out, (W, H), interpolation=cv2.INTER_AREA)
    return out >= 128


def level_lines(mask, lines, ss=4):
    """Rotate each detected text line about its own centre so its baseline is level.
    lines: list of (bool region mask, tilt_deg). Returns new mask."""
    from PIL import Image
    H, W = mask.shape
    out = mask.copy()
    for reg, ang in lines:
        if abs(ang) < 0.05:
            continue
        ys, xs = np.nonzero(reg)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        pad = int(0.02 * (x1 - x0)) + 20
        Y0, Y1, X0, X1 = max(0, y0 - pad), min(H, y1 + pad), max(0, x0 - pad), min(W, x1 + pad)
        sub = reg[Y0:Y1, X0:X1]
        im = Image.fromarray((sub * 255).astype(np.uint8)).resize(((X1 - X0) * ss, (Y1 - Y0) * ss), Image.BILINEAR)
        im = im.rotate(ang, resample=Image.BICUBIC)       # PIL: +deg = counter-clockwise; tilt<0 rises right
        rot = np.asarray(im.resize((X1 - X0, Y1 - Y0), Image.LANCZOS)) >= 128
        out[Y0:Y1, X0:X1] &= ~sub
        out[Y0:Y1, X0:X1] |= rot
    return out


def widen_gaps(mask, ppi, floor_in=0.03, rel=0.06, min_in=0.012, min_area_in=0.025):
    """Open near-touching pairs of shapes to the art gate's gap floor by trimming the smaller shape's sliver
    that sits inside the floor distance of its neighbour. Returns new mask."""
    from scipy import ndimage as nd
    m = mask.copy()
    lab, n = nd.label(m)
    if n < 2:
        return m
    objs = nd.find_objects(lab)
    areas = nd.sum(m, lab, range(1, n + 1))
    for i in range(1, n + 1):
        if areas[i - 1] < (min_area_in * ppi) ** 2:
            continue
        sl = objs[i - 1]; h_i = sl[0].stop - sl[0].start
        pad = int(floor_in * ppi) + 2
        y0, y1 = max(0, sl[0].start - pad), min(m.shape[0], sl[0].stop + pad)
        x0, x1 = max(0, sl[1].start - pad), min(m.shape[1], sl[1].stop + pad)
        sub = lab[y0:y1, x0:x1]
        others = (sub > 0) & (sub != i)
        if not others.any():
            continue
        for j in np.unique(sub[others]):
            if areas[j - 1] < (min_area_in * ppi) ** 2:
                continue
            h_j = objs[j - 1][0].stop - objs[j - 1][0].start
            floor = min(floor_in, max(min_in, rel * min(h_i, h_j) / ppi)) * ppi + 2
            dj = nd.distance_transform_edt(sub != j)
            close = (sub == i) & (dj < floor)
            if close.any() and areas[i - 1] <= areas[j - 1]:
                m[y0:y1, x0:x1][close] = False
    return m


def thicken_thin(mask, ppi, target_in=0.017, protect_counters_in=0.025):
    """Hairline boost: strokes thinner than target get thickened around their own centreline to ~target width.
    Counters are protected: new ink never closes an enclosed space below protect_counters_in."""
    from scipy import ndimage as nd
    from skimage.morphology import skeletonize
    m = mask.copy()
    dt = nd.distance_transform_edt(m)
    sk = skeletonize(m)
    tgt = target_in * ppi
    thin = sk & (2 * dt < tgt)
    if not thin.any():
        return m
    r = int(np.ceil(tgt / 2))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    grow = nd.binary_dilation(thin, structure=(xx ** 2 + yy ** 2) <= r * r)
    new = m | grow
    # protect counters: any enclosed space of the original that would shrink under the floor keeps its pixels
    holes = nd.binary_fill_holes(m) & ~m
    hl, hn = nd.label(holes)
    for j in range(1, hn + 1):
        reg = hl == j
        left = reg & ~new
        if not left.any() or 2 * nd.distance_transform_edt(left).max() < protect_counters_in * ppi:
            new[reg] = m[reg]      # restore this counter untouched
    return new


def open_counters(mask, ppi, floor_in=0.026):
    """Print-prep counter opening: every small enclosed space narrower than floor is grown to the floor by carving
    the surrounding ink (same move as opening the Casa hat 'e' for stitching). Re-run the gate after: STROKES
    catches any stroke this thins too far."""
    from scipy import ndimage as nd
    m = mask.copy()
    holes = nd.binary_fill_holes(m) & ~m
    hl, hn = nd.label(holes)
    if hn == 0:
        return m
    dth = nd.distance_transform_edt(holes)
    for j, sl in enumerate(nd.find_objects(hl), 1):
        reg = hl == j
        w = 2 * dth[reg].max()
        need = floor_in * ppi
        if w >= need or reg.sum() > (0.2 * ppi) ** 2:
            continue
        r = int(np.ceil((need - w) / 2)) + 1
        yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
        grown = nd.binary_dilation(reg, structure=(xx ** 2 + yy ** 2) <= r * r) & m
        m[grown] = False
    return m
