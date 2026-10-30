# Inputs: the 35 white-background JPG mockups of SFV wave 1, downloaded from Shopify into ./src; masters to ./master.
# Site sizes + og.jpg: see the commit "SFV: wave-1 product photos as cut-outs". Same method as Hattiesburg (print-assets hattiesburg/site-tools/knockout.py), native framing kept.
"""SFV wave-1 Printful mockups (white JPG) -> transparent PNG masters, native framing kept (matches wave 2's PNGs).
Garments/hats: rembg isnet-general-use; framed print: the frame rectangle (as Hattiesburg's knockout.py)."""
import os, sys
import numpy as np
from PIL import Image
from rembg import remove, new_session
sess = new_session('isnet-general-use')
for f in sorted(os.listdir('src')):
    base = f.rsplit('.', 1)[0]; out_p = f'master/{base}.png'
    if os.path.exists(out_p): continue
    im = Image.open(f'src/{f}').convert('RGBA')
    if 'framed-poster' in f:
        rgb = np.asarray(im.convert('RGB')).astype(int); dark = rgb.min(axis=2) < 200
        ys, xs = np.where(dark); a = np.zeros(dark.shape, np.uint8); a[ys.min():ys.max() + 1, xs.min():xs.max() + 1] = 255
        out = im.copy(); out.putalpha(Image.fromarray(a))
    else:
        out = remove(im.convert('RGB'), session=sess, post_process_mask=True)
        arr = np.asarray(out).copy(); arr[..., 3] = np.where(arr[..., 3] < 8, 0, arr[..., 3]); out = Image.fromarray(arr)
    out.save(out_p, optimize=True); print(f, flush=True)
