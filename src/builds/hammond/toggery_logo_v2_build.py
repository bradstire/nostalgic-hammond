#!/usr/bin/env python3
"""Toggery Shop logotype v2 (HQ 2026-10-25, S9) -> left-chest master for the merged F/B tee.
Input: hammond/wave2/toggery_logo_address_wine.png (9 in master: traced logotype + typeset address).
v1 traced the logotype from a newspaper ad photographed ~5.5 deg rotated (the ad's body copy rises at the same angle),
so the logo inherited the skew; letters also carried trace lumps, and at 3.5 in the small 'the' touched and its e
nearly closed.
1. Level: rotate by the measured baseline tilt (round o's of Toggery and Shop, T foot, h foot; least squares).
2. Corner-preserving smoothing at full resolution (traced letterforms kept).
3. Downscale to 3.5 in (1050 px); at that print size open counters to 0.026 in and separate near-touching letters.
Usage: toggery_logo_v2_build.py IN_9in.png OUT_leftchest.png
"""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit'))
from vec import smooth_mask_corners, open_counters, widen_gaps  # noqa: E402
WINE = (110, 30, 42)


def main(src, dst):
    a = np.asarray(Image.open(src).convert('RGBA'))
    H, W = a.shape[:2]
    op = a[..., 3] > 128
    logo = op.copy(); logo[1400:, :] = False                      # address line (typeset, level) not part of the logo
    lab, n = ndimage.label(logo)
    # baseline points: bottoms of shapes that sit on the line (T, Toggery o, h, Shop o) = shapes whose bottom is
    # within the main band and that are not descenders (gg/y/p run far below)
    pts = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if (lab[sl] == i).sum() < 20000:
            continue
        pts.append(((sl[1].start + sl[1].stop) / 2, sl[0].stop, h, w, i))
    pts.sort()
    # descenders reach > 1250 px; the swash S starts at the very top: keep shapes ending between 780 and 1100
    base = [(x, y) for x, y, h, w, i in pts if 780 <= y <= 1100]
    xs = np.array([p[0] for p in base]); ys = np.array([p[1] for p in base])
    slope = np.polyfit(xs, ys, 1)[0]
    ang = np.degrees(np.arctan(slope))
    print('baseline points', base, 'tilt %.2f deg' % ang)
    SS = 2
    big = Image.fromarray((logo * 255).astype(np.uint8)).resize((W * SS, H * SS), Image.BILINEAR)
    big = big.rotate(ang, resample=Image.BICUBIC, expand=True)      # tilt<0 rises right -> rotate clockwise
    rot = np.asarray(big.resize((big.width // SS, big.height // SS), Image.LANCZOS)) >= 128
    ys_, xs_ = np.nonzero(rot)
    rot = rot[ys_.min():ys_.max() + 1, xs_.min():xs_.max() + 1]
    yy, xx = np.mgrid[-6:7, -6:7]; d6 = (xx ** 2 + yy ** 2) <= 36
    rot = ndimage.binary_opening(ndimage.binary_closing(rot, structure=d6), structure=d6)   # newspaper-ink lumps/notches
    rot = smooth_mask_corners(rot, sigma_px=14, corner_deg=42)
    # 3.5 in left chest
    tw = 1050 - 2 * 12
    th = int(rot.shape[0] * tw / rot.shape[1])
    small = np.asarray(Image.fromarray((rot * 255).astype(np.uint8)).resize((tw, th), Image.LANCZOS)) >= 128
    small = np.pad(small, 12)
    ppi = small.shape[1] / 3.5
    small = open_counters(small, ppi, 0.026)
    small = widen_gaps(small, ppi)
    out = np.zeros((*small.shape, 4), np.uint8); out[small] = (*WINE, 255)
    Image.fromarray(out).save(dst, dpi=(300, 300))
    json.dump({'typeset': [], 'exempt': [[[0, 0, small.shape[1], small.shape[0]],
               'Toggery logotype - hand-drawn display lettering (flared stems, wedge feet, swash curls are the design): traced from the store ad, levelled in the build by direct measurement (%+.2f deg, o/T/h feet), close/open r6 + corner-preserving smoothing s14; edges verified by eye' % -ang]]},
              open(os.path.splitext(dst)[0] + '.prov.json', 'w'), indent=1)
    print('wrote', dst, small.shape)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
