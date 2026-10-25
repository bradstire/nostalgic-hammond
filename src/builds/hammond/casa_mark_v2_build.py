#!/usr/bin/env python3
"""Casa de Fresa mark (front of the F/B tee) v2 (HQ 2026-10-25, S9). Input: hammond/wave2/casa_mark.png (v1).
1. Knockout lettering (CASA de FRESA / hotel, cream = the shirt) is the matchbook's own hand lettering: traced letters
   kept; notches/spurs removed (close/open) and corner-preserving smoothing. Its rise to the right is the matchbook's
   design (logged exemption, not a defect).
2. Slivers of bare shirt (< 0.025 in) trapped between the red panel and the green ribbon are filled red.
HAMMOND, LA. (red, passes) and the panel/ribbon shapes are kept.
Usage: casa_mark_v2_build.py IN.png OUT.png PRINT_WIDTH_IN
"""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit'))
from vec import smooth_mask_corners  # noqa: E402
RED, GREEN = (206, 32, 46), (10, 104, 86)


def near(a, c, t=60):
    return (a[..., 3] > 128) & (np.abs(a[..., :3].astype(int) - np.array(c)).sum(2) < t)


def disk(r):
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; return (xx ** 2 + yy ** 2) <= r * r


def main(src, dst, width_in):
    a = np.asarray(Image.open(src).convert('RGBA'))
    H, W = a.shape[:2]; ppi = W / width_in
    red = near(a, RED); green = near(a, GREEN)
    # knockout letters = holes in the red panel that are not green, large enough to be letters
    holes = ndimage.binary_fill_holes(red) & ~red & ~green
    hl, hn = ndimage.label(holes)
    letters = np.zeros_like(red)
    for j, sl in enumerate(ndimage.find_objects(hl), 1):
        if (hl[sl] == j).sum() > (0.06 * ppi) ** 2:
            letters |= hl == j
    # clean the letters (as shapes)
    lc = ndimage.binary_opening(ndimage.binary_closing(letters, structure=disk(5)), structure=disk(5))
    lc = smooth_mask_corners(lc, sigma_px=0.04 * ppi, corner_deg=45)
    red2 = (red | letters) & ~lc
    # bare-shirt slivers between red and green
    union = red2 | green
    gaps = ndimage.binary_fill_holes(union) & ~union & ~lc
    gl, gn = ndimage.label(gaps)
    dt = ndimage.distance_transform_edt(gaps)
    filled = 0
    for j in range(1, gn + 1):
        reg = gl == j
        if 2 * dt[reg].max() < 0.025 * ppi:
            red2 |= reg; filled += 1
    # specks of green trapped inside the red (< 0.025 in) -> red
    gl2, gn2 = ndimage.label(green)
    dtg = ndimage.distance_transform_edt(green)
    green2 = green.copy()
    for j, sl in enumerate(ndimage.find_objects(gl2), 1):
        reg = gl2 == j
        if 2 * dtg[reg].max() < 0.025 * ppi and reg.sum() < (0.05 * ppi) ** 2:
            green2 &= ~reg; red2 |= reg
    green = green2
    out = np.zeros_like(a)
    out[red2] = (*RED, 255); out[green] = (*GREEN, 255)
    Image.fromarray(out).save(dst, dpi=(300, 300))
    top_of_ribbon = np.nonzero(green.any(1))[0].min()
    lab_l, _ = ndimage.label(lc)
    keep = np.zeros_like(lc)
    for j, sl in enumerate(ndimage.find_objects(lab_l), 1):
        if sl[0].stop <= top_of_ribbon + 20 and (sl[0].stop - sl[0].start) > 0.15 * ppi:
            keep |= lab_l == j
    ys, xs = np.nonzero(keep)
    json.dump({'typeset': [], 'exempt': [[[int(xs.min()) - 30, int(ys.min()) - 30, int(xs.max()) + 30, int(ys.max()) + 30],
               'matchbook hand lettering CASA de FRESA / hotel: set on a deliberate rise (matchbook design); traced, cleaned (close/open r5 + corner-preserving smoothing)']]},
              open(os.path.splitext(dst)[0] + '.prov.json', 'w'), indent=1)
    print('wrote', dst, 'slivers filled', filled)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
