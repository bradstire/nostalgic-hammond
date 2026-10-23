"""Knock out the white backgrounds of Printful mockups -> transparent PNG masters + WebP site sizes.
Garments/hats/socks: rembg isnet-general-use (handles white tees on white). Framed posters: rectangle of the frame."""
import os, sys, json
import numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session
SRC = 'src'; MASTER = 'master'; SITE = '/home/claude/nh-recovered/pixel-work/public/images/hb/products'
os.makedirs(MASTER, exist_ok=True); os.makedirs(SITE, exist_ok=True)
sess = new_session('isnet-general-use')
manifest = {}
for f in sorted(os.listdir(SRC)):
    base = f.rsplit('.', 1)[0]
    im = Image.open(os.path.join(SRC, f)).convert('RGBA')
    if im.getpixel((5, 5))[3] == 0:          # already transparent
        out = im
    elif 'framed-poster' in f:
        rgb = np.asarray(im.convert('RGB')).astype(int)
        dark = rgb.min(axis=2) < 200
        ys, xs = np.where(dark)
        x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        a = np.zeros(dark.shape, np.uint8); a[y0:y1, x0:x1] = 255
        out = im.copy(); out.putalpha(Image.fromarray(a))
    else:
        out = remove(im.convert('RGB'), session=sess, post_process_mask=True)
        # clean faint halo: alpha below 8 -> 0
        arr = np.asarray(out).copy(); arr[..., 3] = np.where(arr[..., 3] < 8, 0, arr[..., 3]); out = Image.fromarray(arr)
    # trim to content with a small even margin, keep square canvas
    bbox = out.split()[3].getbbox()
    c = out.crop(bbox); side = int(max(c.size) * 1.08)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0)); sq.alpha_composite(c, ((side - c.width) // 2, (side - c.height) // 2))
    sq.save(os.path.join(MASTER, base + '.png'), optimize=True)
    for w in (360, 540, 800, 1080):
        sq.resize((w, w), Image.LANCZOS).save(f'{SITE}/{base}-{w}.webp', 'WEBP', quality=86, method=6, alpha_quality=90)
    manifest[base] = f'/images/hb/products/{base}'
    print(f, flush=True)
json.dump(manifest, open('/home/claude/nh-recovered/pixel-work/src/v2/product-images.json', 'w'), indent=0)
print('done', len(manifest))
