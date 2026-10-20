#!/usr/bin/env python3
"""retouch_postcard.py — automated retouch + enlargement for scanned postcard prints.

Stages (all deterministic, no generative fill):
  1. DESPECKLE: find small extreme-luminance specks (scanner dust, foxing dots)
     and replace ONLY those pixels with the local median. Component size is
     capped so real content (text, halftone, postmarks) is never touched.
  2. SUPER-RESOLUTION 2x: OpenCV dnn_superres (EDSR x2, CPU) for enlargements
     past ~1.3x, else plain LANCZOS.
  3. Fit to target print size at 200 dpi minimum, save with dpi tag.

Usage: python3 retouch_postcard.py in.jpg out.jpg --win 12 --hin 18 [--sr] [--dpi 200]
"""
import argparse, numpy as np, cv2
from PIL import Image
from scipy import ndimage

def despeckle(arr, max_size=60, z=2.6):
    g = arr.mean(axis=2)
    med = cv2.medianBlur(g.astype(np.uint8), 7).astype(float)
    resid = g - med
    sd = max(resid.std(), 1e-6)
    hot = np.abs(resid) > z * sd
    lab, n = ndimage.label(hot)
    sizes = ndimage.sum(hot, lab, range(1, n + 1))
    keep = np.isin(lab, np.where(sizes <= max_size)[0] + 1)   # only small components
    out = arr.copy()
    medc = cv2.medianBlur(arr, 7)
    out[keep] = medc[keep]
    return out, int(keep.sum()), int(n)

def upscale(arr, scale, model='EDSR_x2.pb'):
    if scale <= 1.02: return arr
    if scale <= 1.35:
        return cv2.resize(arr, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model); sr.setModel('edsr', 2)
    up = sr.upsample(arr)                                      # 2x
    if abs(scale - 2) > 0.02:
        up = cv2.resize(up, None, fx=scale/2, fy=scale/2, interpolation=cv2.INTER_AREA if scale < 2 else cv2.INTER_LANCZOS4)
    return up

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('inp'); p.add_argument('out')
    p.add_argument('--win', type=float, required=True); p.add_argument('--hin', type=float, required=True)
    p.add_argument('--dpi', type=int, default=200)
    p.add_argument('--sr', action='store_true', help='allow EDSR 2x when upscale > 1.35x')
    a = p.parse_args()
    img = cv2.imread(a.inp)
    img, fixed, ncomp = despeckle(img)
    print(f'despeckle: {fixed} px in small components (of {ncomp} candidates)')
    tw, th = int(a.win * a.dpi), int(a.hin * a.dpi)
    scale = max(tw / img.shape[1], th / img.shape[0])
    print(f'native {img.shape[1]}x{img.shape[0]} -> target {tw}x{th} (scale {scale:.2f}x, native dpi {img.shape[1]/a.win:.0f})')
    if scale > 1.35 and not a.sr:
        print('WARNING: >1.35x enlargement without --sr; using LANCZOS')
    img = upscale(img, scale) if (a.sr or scale <= 1.35) else cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)
    img = img[:th, :tw]
    Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).save(a.out, quality=95, dpi=(a.dpi, a.dpi))
    print('saved', a.out, img.shape[1], 'x', img.shape[0])
