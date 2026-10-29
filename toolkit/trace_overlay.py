#!/usr/bin/env python3
"""S9 part B for R21 traces (L46): draw the finished master's outline on the source photo it was traced from.

The master is mapped back through its .prov.json "frame" (master px = build units * scale - (ox, oy)) and an
optional build->source affine (x_src = sx * x_build + tx, y_src = sy * y_build + ty) onto the (rectified) source
image. Every traced element must be checked here at print zoom: a missing piece (Weber's W wedge), a drifted
word (Encino Coffee Shop) or a wrong frame shows as outline away from the photographed edge.

Usage: trace_overlay.py MASTER.png SOURCE.png OUT.png [sx sy tx ty] [--crop x0,y0,x1,y1 (source px)]..."""
import json, os, sys
import numpy as np, cv2
from PIL import Image

def main():
    args = sys.argv[1:]
    crops = []
    while '--crop' in args:
        i = args.index('--crop'); crops.append([int(v) for v in args[i + 1].split(',')]); del args[i:i + 2]
    master, source, out = args[:3]
    sx, sy, tx, ty = [float(v) for v in args[3:7]] if len(args) >= 7 else (1, 1, 0, 0)
    fr = json.load(open(os.path.splitext(master)[0] + '.prov.json'))['frame']
    k, ox, oy = fr['scale'], fr['ox'], fr['oy']
    m = np.asarray(Image.open(master).convert('RGBA'))[..., 3] > 127
    src = np.asarray(Image.open(source).convert('RGB')).copy()
    # master px -> build: b = (m + o) / k ; build -> source: s = S*b + t
    A = np.float32([[sx / k, 0, sx * ox / k + tx], [0, sy / k, sy * oy / k + ty]])
    w = cv2.warpAffine(m.astype(np.uint8) * 255, A, (src.shape[1], src.shape[0]), flags=cv2.INTER_LINEAR) > 127
    edge = w & ~cv2.erode(w.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    src[edge] = (255, 0, 255)
    im = Image.fromarray(src)
    if crops:
        tiles = [im.crop(c) for c in crops]
        H = max(t.height for t in tiles); Wd = sum(t.width for t in tiles) + 20 * (len(tiles) - 1)
        sheet = Image.new('RGB', (Wd, H), (30, 30, 30)); x = 0
        for t in tiles:
            sheet.paste(t, (x, 0)); x += t.width + 20
        im = sheet
    im.save(out)
    print(out, im.size)

if __name__ == '__main__':
    main()
