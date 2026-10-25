#!/usr/bin/env python3
"""Hammond embroidered hats v2 (HQ 2026-10-25, S9 + embroidery floors).
- Toggery hat: lettering inherited the store-ad photo skew (~6 deg, rising right) -> levelled by direct measurement
  (feet of T, o, h, o). No smoothing: stitch paths don't carry trace micro-lumps, and smoothing thins strokes.
- Casa hat: already level -> v1 kept.
Embroidery floors checked after: strokes >= 0.05 in, enclosed spaces >= 0.03 in, lettering >= 0.25 in.
NOTE: re-uploading an embroidery file makes Printful re-digitize it - Brad's call before any upload.
Usage: hats_v2_build.py OUTDIR"""
import sys, os, json
import numpy as np
from scipy import ndimage
from skimage.morphology import skeletonize
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit'))
from vec import smooth_mask_corners  # noqa: E402
W2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'hammond', 'wave2', 'hats')


def disk(r):
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; return (xx ** 2 + yy ** 2) <= r * r


def clean(m, r=3, sig=4):
    m = ndimage.binary_opening(ndimage.binary_closing(m, structure=disk(r)), structure=disk(r))
    return smooth_mask_corners(m, sigma_px=sig, corner_deg=42)


def level(m, pts):
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    ang = np.degrees(np.arctan(np.polyfit(xs, ys, 1)[0]))
    H, W = m.shape; SS = 2
    big = Image.fromarray((m * 255).astype(np.uint8)).resize((W * SS, H * SS), Image.BILINEAR)
    big = big.rotate(ang, resample=Image.BICUBIC, expand=True)
    r = np.asarray(big.resize((big.width // SS, big.height // SS), Image.LANCZOS)) >= 128
    ys_, xs_ = np.nonzero(r)
    return np.pad(r[ys_.min():ys_.max() + 1, xs_.min():xs_.max() + 1], 6), ang


def emb_check(m, ppi):
    dt = ndimage.distance_transform_edt(m); sk = skeletonize(m)
    nb = ndimage.convolve(sk.astype(int), np.ones((3, 3), int), mode='constant') - 1
    tipz = ndimage.binary_dilation(sk & (nb <= 1), iterations=int(0.05 * ppi))
    w = 2 * dt[sk & ~tipz]
    holes = ndimage.binary_fill_holes(m) & ~m; hl, hn = ndimage.label(holes)
    dth = ndimage.distance_transform_edt(holes)
    hmin = min([2 * dth[hl == j].max() for j in range(1, hn + 1)] or [99])
    return dict(min_stroke_in=round(float(np.percentile(w, 1)) / ppi, 3), min_counter_in=round(hmin / ppi, 3))


def run(name, width_in, out_dir, pts=None, do_clean=False):
    a = np.asarray(Image.open(os.path.join(W2, name)).convert('RGBA'))
    m = a[..., 3] > 128; col = a[m][:, :3].mean(0).astype(np.uint8)
    ppi = a.shape[1] / width_in
    ang = 0.0
    if pts:
        m, ang = level(m, pts)
    if do_clean:
        m = clean(m)
    out = np.zeros((*m.shape, 4), np.uint8); out[m] = (*col, 255)
    stem = os.path.join(out_dir, name.replace('.png', '_v2.png'))
    Image.fromarray(out).save(stem, dpi=(300, 300))
    w_in = m.shape[1] / ppi; h_in = m.shape[0] / ppi
    ec = emb_check(m, ppi)
    print(f'{name}: levelled {-ang:+.2f} deg; {w_in:.2f} x {h_in:.2f} in; embroidery {ec}')
    return stem


if __name__ == '__main__':
    out = sys.argv[1]
    # Toggery: feet of T, o, h, o (x centre, bottom) from the v1 master
    run('hat_toggery_maroon.png', 3.67, out, pts=[(84.5, 423), (160.5, 411), (771, 360), (967, 328)])
    run('hat_toggery_white.png', 3.67, out, pts=[(84.5, 423), (160.5, 411), (771, 360), (967, 328)])
    # Casa hat: v1 kept (level already; trace micro-lumps don't survive digitizing, and cleanup thinned the
    # thinnest stroke under the 0.05 in stitch floor) - measured here for the record only
    for n_ in ('hat_casadefresa_hammond_red.png',):
        a_ = np.asarray(Image.open(os.path.join(W2, n_)).convert('RGBA')); m_ = a_[..., 3] > 128
        print(n_, 'v1 kept; embroidery', emb_check(m_, a_.shape[1] / 4.74))
