#!/usr/bin/env python3
"""Casa de Fresa socks v2 (HQ 2026-10-25, S9). Inputs: hammond/wave2/socks/sock_casadefresa_{front,back}.png
(4.49 x 18.9 in sublimation panels, 3 inks + stripes). The traced matchbook lettering on the calf carried trace
lumps and near-touching letters. In the lettering zone only (stripes untouched): each ink layer cleaned
(close/open r3 + corner-preserving smoothing), near-touching shapes opened to the gate floor. The front lettering's
rise is the matchbook design (logged exemption, as on the F/B front).
Usage: socks_v2_build.py OUTDIR"""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit'))
from vec import smooth_mask_corners, widen_gaps, open_counters  # noqa: E402
SOCKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'hammond', 'wave2', 'socks')
INKS = [(10, 104, 86), (206, 32, 46), (243, 233, 207)]


def disk(r):
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; return (xx ** 2 + yy ** 2) <= r * r


def run(name, out_dir, zone, exempt=None):
    a = np.asarray(Image.open(os.path.join(SOCKS, name)).convert('RGBA')).copy()
    H, W = a.shape[:2]; ppi = W / (1347 / 300)
    y0, y1 = zone
    sub = a[y0:y1].copy()
    op = sub[..., 3] > 128
    idx = np.full(op.shape, -1)
    for k, c in enumerate(INKS):
        idx[op & (np.abs(sub[..., :3].astype(int) - np.array(c)).sum(2) < 60)] = k
    out = sub.copy()
    # clean each ink (as shapes); paint in order green, red, cream so letters keep their colour on top
    cleaned = []; trimmed = []
    for k in range(len(INKS)):
        m = idx == k
        if m.sum() == 0:
            cleaned.append(m); trimmed.append(m); continue
        # gentle: at sock scale strokes are 10-15 px - an opening pass erases real letter parts (rejected 10-25)
        m2 = ndimage.binary_closing(m, structure=disk(2))
        m2 = smooth_mask_corners(m2, sigma_px=4, corner_deg=40)
        if k == 1:
            m2 = open_counters(m2, ppi, 0.026)      # small red letters' eyes (HAMMOND, LA. on the ribbon)
        hl_, hn_ = ndimage.label(ndimage.binary_fill_holes(m2) & ~m2)     # pinholes the cleanup left in a layer
        for j_, sl_ in enumerate(ndimage.find_objects(hl_), 1):
            if (hl_[sl_] == j_).sum() < (0.015 * ppi) ** 2:
                m2[sl_] |= hl_[sl_] == j_
        before = m2.copy()
        m2 = widen_gaps(m2, ppi)
        trimmed.append(before & ~m2)            # opened gaps take the ink behind the letter (below)
        cleaned.append(m2 & op)          # never paint outside the original art
    fill = np.zeros(op.shape, bool)
    for k in (0, 1, 2):
        out[cleaned[k]] = (*INKS[k], 255); fill |= cleaned[k]
    # gap-opening trims: red lettering sits on cream, cream knockouts sit on red
    for k, bgk in ((1, 2), (2, 1), (0, 2)):
        t = trimmed[k] & op & ~fill
        out[t] = (*INKS[bgk], 255); fill |= t
    # any other pixel that lost every ink keeps its original colour (no holes introduced)
    out[op & ~fill] = sub[op & ~fill]
    # specks of one ink trapped inside another (< 0.015 in) take the surrounding ink
    for k, c in enumerate(INKS):
        mk = (np.abs(out[..., :3].astype(int) - np.array(c)).sum(2) < 30) & (out[..., 3] > 128)
        hl_, _ = ndimage.label(ndimage.binary_fill_holes(mk) & ~mk)
        for j_, sl_ in enumerate(ndimage.find_objects(hl_), 1):
            reg = hl_[sl_] == j_
            if reg.sum() < (0.015 * ppi) ** 2:
                out[sl_][reg] = (*c, 255)
    a[y0:y1] = out
    dst = os.path.join(out_dir, name.replace('.png', '_v2.png'))
    Image.fromarray(a).save(dst, dpi=(300, 300))
    json.dump({'typeset': [], 'exempt': [exempt] if exempt else []}, open(dst.replace('.png', '.prov.json'), 'w'), indent=1)
    print('wrote', dst)


if __name__ == '__main__':
    out = sys.argv[1]
    run('sock_casadefresa_front.png', out, (1900, 2800),
        exempt=[[300, 1980, 1060, 2600], 'matchbook hand lettering (CASA de FRESA / hotel on a deliberate rise; HAMMOND, LA. on the ribbon): traced, cleaned (close r2 + corner-preserving smoothing s4, eyes opened); sublimation on knit'])
    run('sock_casadefresa_back.png', out, (1880, 2200),
        exempt=[[290, 1920, 1060, 2160], 'matchbook hand lettering CASA de FRESA: traced, cleaned (close r2 + corner-preserving smoothing s4); irregular widths are the lettering own; sublimation on knit'])
