#!/usr/bin/env python3
"""Toggery Shop blade sign v2 (HQ 2026-10-25, S9). Input: hammond/wave2/toggery_sign_1color_wine.png (5 x 11.6 in).
The thin cream keylines inside the sign (column and SHOP panel borders) were ~0.013 in at print size: DTG ink spread
closes lines that fine and the keylines would vanish. Every gap between ink shapes is opened to the gate floor (up to 0.03 in) by
trimming the smaller shape's edge; letters (Playfair, set type) and geometry otherwise unchanged.
Usage: toggery_sign_v2_build.py IN.png OUT.png"""
import sys, os, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit'))
from vec import widen_gaps
a = np.asarray(Image.open(sys.argv[1]).convert('RGBA'))
op = a[..., 3] > 128
col = a[op][:, :3].mean(0).astype(np.uint8)
m = widen_gaps(op, a.shape[1] / 5.0)   # same rule as the gate: 6 % of height, 0.012-0.03 in
out = np.zeros_like(a); out[m] = (*col, 255)
Image.fromarray(out).save(sys.argv[2], dpi=(300, 300))
json.dump({'typeset': [[[0, 0, a.shape[1], a.shape[0]], 'Playfair Display (TOGGERY / SHOP letters, set type)']], 'exempt': []},
          open(os.path.splitext(sys.argv[2])[0] + '.prov.json', 'w'), indent=1)
print('wrote', sys.argv[2], 'px trimmed', int((op & ~m).sum()))
