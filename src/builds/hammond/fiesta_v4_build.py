#!/usr/bin/env python3
"""Fiesta Club logo v4 (HQ 2026-10-25, S9). Input: hammond/wave2/fiesta_club_logo_v3.png.
Found at upload: v3 was gated at 10 in, the width of the v1 file, but v3's canvas is narrower (the lounge line was
recentred, so the bbox shrank) at the same pixel scale. The live print keeps the letters' physical size, so v3 prints
at 2420 px / 300 ppi = 8.07 in. At that true size one gap failed: the FIESTA block's lower-right point sat 0.024 in
from the C of Club. Gaps are opened to the gate floor at the true print width; nothing else changes.
Usage: fiesta_v4_build.py V3.png OUT.png"""
import sys, os, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit'))
from vec import widen_gaps  # noqa: E402
PRINT_W_IN = 2420 / 300


def main(src, dst):
    a = np.asarray(Image.open(src).convert('RGBA')).copy()
    m = a[..., 3] > 128
    col = tuple(int(v) for v in np.median(a[m][:, :3], axis=0))
    ppi = a.shape[1] / PRINT_W_IN
    m2 = widen_gaps(m, ppi)
    print('pixels trimmed', int((m & ~m2).sum()))
    out = np.zeros_like(a); out[m2] = (*col, 255)
    Image.fromarray(out).save(dst, dpi=(300, 300), optimize=True)
    pv = json.load(open(os.path.splitext(src)[0] + '.prov.json'))
    json.dump(pv, open(os.path.splitext(dst)[0] + '.prov.json', 'w'), indent=1)
    print('wrote', dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
