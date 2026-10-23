"""Fix Printful sock mockups for the site: the front sock is rendered toe-up, so rotate it upright.
Output: public/images/hb/socks/<handle>-{360,540,800,1080}.webp"""
import json, urllib.request, io
import numpy as np
from PIL import Image
OUT = '/home/claude/nh-recovered/pixel-work/public/images/hb/socks'
d = json.load(open('/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/catalog.json'))
for n in d['data']['products']['nodes']:
    if not n['handle'].endswith('-socks'): continue
    u = n['images']['nodes'][0]['url']
    im = Image.open(io.BytesIO(urllib.request.urlopen(u + ('&' if '?' in u else '?') + 'width=2000').read())).convert('RGB')
    a = np.asarray(im).astype(int)
    nonwhite = (a.min(axis=2) < 235)
    cols = nonwhite.any(axis=0); rows = nonwhite.any(axis=1)
    xs = np.where(cols)[0]
    # split into the two sock blobs at the widest gap
    gaps = np.diff(xs); g = gaps.argmax()
    l0, l1 = xs[0], xs[g] + 1
    ys = np.where(nonwhite[:, l0:l1].any(axis=1))[0]; t0, t1 = ys[0], ys[-1] + 1
    sock = im.crop((l0, t0, l1, t1)).rotate(180)
    out = im.copy(); out.paste((255, 255, 255), (l0, t0, l1, t1)); out.paste(sock, (l0, t0))
    # warm the white background to the site card colour so it sits on the page
    arr = np.asarray(out).astype(np.float32); bg = np.array([251, 248, 242], np.float32)
    w = (arr.min(axis=2, keepdims=True) > 247).astype(np.float32)
    arr = arr * (1 - w) + bg * w
    out = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    for W in (360, 540, 800, 1080):
        out.resize((W, W), Image.LANCZOS).save(f"{OUT}/{n['handle']}-{W}.webp", quality=84, method=6)
    print(n['handle'], (l0, l1, t0, t1))
