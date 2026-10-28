"""ttest.py MASK sigma1,sigma2,... [alphamax] -> renders traced geometry for each sigma stacked, to SP/ttest.png"""
import sys, numpy as np
sys.path.insert(0, '/home/claude/print-assets/src/builds/sfv')
from w2lib import trace_geom
from PIL import Image, ImageDraw
from shapely.geometry import Polygon, MultiPolygon
m = np.array(Image.open(sys.argv[1]).convert('L')) > 127
sig = [float(s) if s != '0' else None for s in sys.argv[2].split(',')]
am = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
crop = [int(v) for v in sys.argv[4].split(',')] if len(sys.argv) > 4 else None
rows = []
for s in sig:
    g = trace_geom(m, alphamax=am, smooth_sigma=s)
    im = Image.new('L', (m.shape[1], m.shape[0]), 255); d = ImageDraw.Draw(im)
    for p in getattr(g, 'geoms', [g]):
        d.polygon(list(p.exterior.coords), fill=0)
        for h in p.interiors: d.polygon(list(h.coords), fill=255)
    if crop: im = im.crop(crop)
    rows.append(im)
W = max(r.width for r in rows); H = sum(r.height for r in rows) + 10 * len(rows)
out = Image.new('L', (W, H), 128); y = 0
for r in rows: out.paste(r, (0, y)); y += r.height + 10
out.save('/tmp/claude-0/-home-claude/3ad67d26-ad11-5829-ad96-2a5bc3109ee4/scratchpad/ttest.png')
