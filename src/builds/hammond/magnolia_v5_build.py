#!/usr/bin/env python3
"""Magnolia Inn sign v5 (HQ 2026-10-25, S9). Input: hammond/wave2/magnolia_sign_hammond_v4.png.
v4 (built in-session 10-25, before the build-script rule; its sidecar was the record): RESTAURANT and INN re-set in
Bevan, address in League Spartan 600, the 'Magnolia' script cleaned and levelled, board/frame/posts rebuilt as true
geometry (0.7 deg skew, uneven 38-58 px frame and short post fixed), flower returned to the traced petal geometry (the v2 redraw had deviated).
v5 change, found by the SURVIVAL compare against v1: the cleanup left the script's i-dot at 60 % of the traced dot's
area; the postcard's dot is about the stem width. The dot is scaled back to the traced area about its own centre.
Everything else is v4 unchanged.
Usage: magnolia_v5_build.py V4.png V1.png OUT.png"""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter
RED = (222, 66, 40)


def layer(a, c):
    return (a[..., 3] > 128) & (np.abs(a[..., :3].astype(int) - np.array(c)).sum(2) < 40)


def idot(m):
    """The i-dot = the smallest red component in the script's upper right (the only small free-standing red shape)."""
    lab, n = ndimage.label(m)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    j = int(np.argmin(sizes)) + 1
    return lab == j, ndimage.find_objects(lab)[j - 1]


def main(v4, v1, dst):
    a = np.asarray(Image.open(v4).convert('RGBA')).copy()
    H, W = a.shape[:2]
    red4 = layer(a, RED); red1 = layer(np.asarray(Image.open(v1).convert('RGBA')), RED)
    d4, sl4 = idot(red4); d1, _ = idot(red1)
    k = (d1.sum() / d4.sum()) ** 0.5
    cy, cx = ndimage.center_of_mass(d4)
    # scale the dot's own shape about its centre (supersampled), paint red where it grows, white where it was
    SS = 4; pad = 40
    y0, y1, x0, x1 = sl4[0].start - pad, sl4[0].stop + pad, sl4[1].start - pad, sl4[1].stop + pad
    crop = Image.fromarray((d4[y0:y1, x0:x1] * 255).astype(np.uint8)).resize(((x1 - x0) * SS, (y1 - y0) * SS), Image.BILINEAR)
    ccx, ccy = (cx - x0) * SS, (cy - y0) * SS
    crop = crop.filter(ImageFilter.GaussianBlur(SS * 1.2))          # melt the pixel staircase before scaling (smooth edge)
    big = crop.transform(crop.size, Image.AFFINE, (1 / k, 0, ccx - ccx / k, 0, 1 / k, ccy - ccy / k), resample=Image.BICUBIC)
    new = np.asarray(big.resize((x1 - x0, y1 - y0), Image.LANCZOS)) >= 128
    region = a[y0:y1, x0:x1]
    bg = region[~d4[y0:y1, x0:x1] & (region[..., 3] > 128)]
    bgc = tuple(int(v) for v in np.median(bg[:, :3], axis=0)) if len(bg) else (255, 255, 255)
    region[d4[y0:y1, x0:x1]] = (*bgc, 255)
    region[new] = (*RED, 255)
    Image.fromarray(a).save(dst, dpi=(300, 300))
    print(f'i-dot area {int(d4.sum())} -> {int(new.sum())} px (traced v1 dot {int(d1.sum())}), scale {k:.3f}')
    # provenance: v4's declarations + what moved by design vs v1
    pv = json.load(open(os.path.splitext(v4)[0] + '.prov.json'))
    inn = [b for b, f in pv['typeset'] if 'INN' in f][0]
    script = red4.copy(); script[inn[1]:inn[3], inn[0]:inn[2]] = False
    ys, xs = np.nonzero(script)
    sbox = [int(xs.min()) - 20, int(ys.min()) - 20, int(xs.max()) + 20, int(ys.max()) + 20]
    flower = [b for b, r in pv['exempt'] if 'flower' in r.lower()][0]
    pv['redrawn'] = [
        [sbox, "'Magnolia' script: traced letters cleaned, levelled as one unit, i-dot restored to the traced area (letters move by design)"],
        [flower, 'flower: v4 returned to the traced petal geometry after the v2 redraw deviated (Brad 10-25, judgement call); outlines cleaned'],
    ]
    json.dump(pv, open(os.path.splitext(dst)[0] + '.prov.json', 'w'), indent=1)
    print('wrote', dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
