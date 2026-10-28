"""SFV wave 2 build library (HQ, 2026-10-27).

Vector-first: every master is shapely geometry in 300-dpi pixel units, rasterised once by cairosvg with
binary alpha (DTG rule, NT_TOOLKIT). Type comes straight from OFL fonts (vtype.text_geom: font -> potrace ->
polygons), never traced or roughened (S9 build rules 1-2, L31). Traced elements (hand lettering, illustration)
go through trace_geom() (Real-ESRGAN upscale outside, threshold, corner-preserving smoothing, potrace) and are
declared as exemptions with a reason. Every typeset run is declared in the .prov.json sidecar for the S9 gate.
"""
import json, math, os, sys
import numpy as np
from PIL import Image
from shapely.geometry import Polygon, MultiPolygon, box, Point, LineString
from shapely.ops import unary_union
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'newsprint'))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'toolkit'))
import vtype  # noqa: E402

FONTDIRS = ['/home/claude/sfv/fonts2', '/home/claude/sfv/fonts']
DPI = 300

# Drive colour bank (NT_TOOLKIT) + light inks for dark garments
INK = dict(red='#8B0000', gold='#B8860B', navy='#003366', green='#006B3F', purple='#3A1055',
           black='#1A1A1A', charcoal='#262220', cream='#F4ECDD', white='#FFFFFF')


def fpath(name):
    for d in FONTDIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)


_cap_cache = {}


def cap_ratio(font, var=None):
    """cap height / font size, measured on 'H'."""
    k = (font, str(var))
    if k not in _cap_cache:
        g, _ = vtype.text_geom('H', fpath(font), 1000, var)
        _cap_cache[k] = (g.bounds[3] - g.bounds[1]) / 1000.0
    return _cap_cache[k]


def T(text, font, cap=None, size=None, var=None, track=0.0):
    """Text geometry, baseline at y=0, pen at x=0. cap = cap height in px (300 dpi), or size = font px.
    track in em. Rendered at 1000 px and scaled (vector), so small sizes stay exact."""
    if cap is not None:
        size = cap / cap_ratio(font, var)
    g, adv = vtype.text_geom(text, fpath(font), 1000, var, track)
    s = size / 1000.0
    return affinity.scale(g, s, s, origin=(0, 0)), adv * s


def bounds(g):
    return g.bounds


def width(g):
    b = g.bounds
    return b[2] - b[0]


def height(g):
    b = g.bounds
    return b[3] - b[1]


def move(g, x=None, y=None, cx=None, cy=None, right=None, bottom=None):
    """Move so that the bbox left/top (x/y), centre (cx/cy), right edge or bottom lands at the value."""
    b = g.bounds
    dx = dy = 0
    if x is not None: dx = x - b[0]
    if cx is not None: dx = cx - (b[0] + b[2]) / 2
    if right is not None: dx = right - b[2]
    if y is not None: dy = y - b[1]
    if cy is not None: dy = cy - (b[1] + b[3]) / 2
    if bottom is not None: dy = bottom - b[3]
    return affinity.translate(g, dx, dy)


def scale_to(g, w=None, h=None, xs=None):
    """Uniform scale to width w or height h (about bbox origin); xs = extra horizontal-only factor."""
    b = g.bounds
    s = (w / (b[2] - b[0])) if w else (h / (b[3] - b[1]))
    g = affinity.scale(g, s, s, origin=(b[0], b[1]))
    if xs:
        g = affinity.scale(g, xs, 1, origin=(b[0], b[1]))
    return g


def hscale(g, f):
    b = g.bounds
    return affinity.scale(g, f, 1, origin=((b[0] + b[2]) / 2, b[1]))


def rrect(x0, y0, x1, y1, r):
    return box(x0 + r, y0 + r, x1 - r, y1 - r).buffer(r, join_style='round', resolution=32) if r > 0 else box(x0, y0, x1, y1)


def ring(g, w, inner_offset=0.0, mitre=3.0):
    """A keyline of width w following g's outline, starting `inner_offset` outside it (negative = inside)."""
    a = g.buffer(inner_offset + w, join_style='mitre', mitre_limit=mitre) if inner_offset + w != 0 else g
    b = g.buffer(inner_offset, join_style='mitre', mitre_limit=mitre) if inner_offset != 0 else g
    return a.difference(b)


def stroke_line(pts, w, cap='round'):
    return LineString(pts).buffer(w / 2, cap_style=cap, join_style='round', resolution=24)


def regular_polygon(cx, cy, rx, ry, n, rot=0.0):
    return Polygon([(cx + rx * math.cos(rot + 2 * math.pi * i / n), cy + ry * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)])


def star(cx, cy, r, inner=0.42, n=5):
    pts = []
    for i in range(2 * n):
        a = -math.pi / 2 + i * math.pi / n
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return Polygon(pts)


def arc_text(text, font, size, cx, cy, radius, centre_deg=-90, var=None, track=0.0, outward=True, xs=1.0, anchor=None):
    """Glyphs set along a circle of `radius` (baseline on the circle), centred at angle centre_deg (-90 = top).
    Each glyph is its own font geometry, rotated about its own baseline centre: still typeset, never traced."""
    glyphs = []
    advs = []
    from PIL import ImageFont
    pf = ImageFont.truetype(fpath(font), 1000)
    if var:
        pf.set_variation_by_axes(var)
    s = size / 1000.0
    for ch in text:
        if not ch.strip():
            glyphs.append(None)
            advs.append(pf.getlength(ch) * s * xs + track * size)
            continue
        g, adv = vtype.text_geom(ch, fpath(font), 1000, var, 0)
        glyphs.append(affinity.scale(g, s * xs, s, origin=(0, 0)) if (g is not None and not g.is_empty) else None)
        advs.append(adv * s * xs + track * size)
    total = sum(advs) - track * size
    ang_total = total / radius
    if anchor is not None:
        # put the centre of character `anchor` (e.g. a word space) at centre_deg instead of the run's centre
        pos = sum(advs[:anchor]) + advs[anchor] / 2
        centre_deg = centre_deg + math.degrees((total / 2 - pos) / radius) * (1 if outward else -1)
    a = math.radians(centre_deg) - ang_total / 2 if outward else math.radians(centre_deg) + ang_total / 2
    out = []
    for g, adv in zip(glyphs, advs):
        mid = a + (adv / 2) / radius * (1 if outward else -1)
        if g is not None:
            # centre glyph advance on x=0, baseline y=0; rotate to tangent; place on circle
            g2 = affinity.translate(g, -(adv - track * size) / 2, 0)
            rot = math.degrees(mid) + 90 if outward else math.degrees(mid) - 90
            g2 = affinity.rotate(g2, rot, origin=(0, 0))
            g2 = affinity.translate(g2, cx + radius * math.cos(mid), cy + radius * math.sin(mid))
            out.append(g2)
        a += adv / radius * (1 if outward else -1)
    return unary_union(out)


def trace_geom(mask, alphamax=0.9, smooth_sigma=None, corner_deg=40):
    """Bool mask (ink=True) -> clean geometry. Optional corner-preserving smoothing first (toolkit/vec.py)."""
    if smooth_sigma:
        import vec
        mask = vec.smooth_mask_corners(mask, sigma_px=smooth_sigma, corner_deg=corner_deg)
    return vtype.mask_to_geom(mask, alphamax=alphamax).buffer(0)


class Art:
    """Ordered ink/knockout operations on one ink colour, plus S9 declarations."""

    def __init__(self, name):
        self.name = name
        self.ops = []
        self.decl = {'typeset': [], 'exempt': [], 'redrawn': []}

    def add(self, g, kind=None, note=''):
        self.ops.append(('+', g))
        if kind:
            self.declare(kind, g, note)
        return g

    def cut(self, g, kind=None, note=''):
        self.ops.append(('-', g))
        if kind:
            self.declare(kind, g, note)
        return g

    def declare(self, kind, g, note, pad=6):
        b = g.bounds if hasattr(g, 'bounds') else g
        self.decl[kind].append([[b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad], note])
        if kind == 'typeset' and hasattr(g, 'buffer'):
            self.__dict__.setdefault('type_geoms', []).append(g)      # kept crisp through print-clean (L31)

    def geom(self):
        g = Polygon()
        for op, h in self.ops:
            g = g.union(h) if op == '+' else g.difference(h)
        return g.buffer(0)

    def save(self, outdir, ink='black', pad=30, extra=None, max_w_in=10.5, max_h_in=13.5, clean=False):
        os.makedirs(outdir, exist_ok=True)
        g = self.geom()
        b = g.bounds
        f = min(1.0, (max_w_in * DPI - 2 * pad) / (b[2] - b[0]), (max_h_in * DPI - 2 * pad) / (b[3] - b[1]))
        tg = unary_union(getattr(self, 'type_geoms', [])) if getattr(self, 'type_geoms', None) else None
        if f < 1.0:
            g = affinity.scale(g, f, f, origin=(0, 0))
            if tg is not None:
                tg = affinity.scale(tg, f, f, origin=(0, 0))
            for k in self.decl:
                self.decl[k] = [[[v * f for v in bb], n] for bb, n in self.decl[k]]
            b = g.bounds
            print(f'  scaled x{f:.3f} to fit {max_w_in} x {max_h_in} in')
        ox, oy = math.floor(b[0]) - pad, math.floor(b[1]) - pad
        W, H = math.ceil(b[2] - ox) + pad, math.ceil(b[3] - oy) + pad
        g = affinity.translate(g, -ox, -oy)
        im = vtype.raster([(g, INK.get(ink, ink))], W, H)
        if clean:
            import numpy as np
            a = np.array(im)
            m0 = a[..., 3] > 0
            m = print_clean(m0, DPI, **(clean if isinstance(clean, dict) else {}))
            if tg is not None:
                # type renders straight from the font: print-clean never touches typeset glyphs (L31, R21)
                tz = np.array(vtype.raster([(affinity.translate(tg.buffer(4), -ox, -oy), '#000000')], W, H))[..., 3] > 0
                m = np.where(tz, m0, m)
            h = INK.get(ink, ink)
            a[..., :3] = [int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)]
            a[..., 3] = np.where(m, 255, 0)
            a[~m, :3] = 0
            im = Image.fromarray(a, 'RGBA')
            print('  print-clean pass applied at 300 ppi')
        path = os.path.join(outdir, self.name + '.png')
        im.save(path, dpi=(DPI, DPI))
        prov = {}
        for k, lst in self.decl.items():
            prov[k] = [[[round(bb[0] - ox), round(bb[1] - oy), round(bb[2] - ox), round(bb[3] - oy)], n] for bb, n in lst]
        prov['rules'] = ['R21']          # trace-first: every typeset line must carry its R21 reason (S9 SOURCE)
        prov['ink'] = INK.get(ink, ink)
        prov['print_width_in'] = round(W / DPI, 3)
        prov['print_height_in'] = round(H / DPI, 3)
        if extra:
            prov.update(extra)
        json.dump(prov, open(os.path.join(outdir, self.name + '.prov.json'), 'w'), indent=1)
        # vector source alongside (re-render / embroidery digitizer)
        open(os.path.join(outdir, self.name + '.svg'), 'w').write(vtype.svg_doc([(g, INK.get(ink, ink))], W, H))
        print(f"{self.name}: {W}x{H}px = {W / DPI:.2f} x {H / DPI:.2f} in, ink {ink}")
        return path


def recolor(png_path, ink, out_path):
    """Same master, another ink (colourway): identical geometry, only the colour changes."""
    im = Image.open(png_path).convert('RGBA')
    a = np.array(im)
    h = INK.get(ink, ink)
    rgb = [int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)]
    a[a[..., 3] > 0, :3] = rgb
    Image.fromarray(a).save(out_path, dpi=(DPI, DPI))
    j = json.load(open(png_path[:-4] + '.prov.json'))
    j['ink'] = h
    json.dump(j, open(out_path[:-4] + '.prov.json', 'w'), indent=1)


def _catmull(pts, n=24):
    import numpy as np
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = [np.array(P[j], float) for j in (i - 1, i, i + 1, i + 2)]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(np.array(pts[-1], float))
    return out


def brush(pts, widths, n=24):
    """A brush stroke through control points (Catmull-Rom), width interpolated along the control points.
    Built as a union of discs + the hulls between neighbours, so the outline is smooth."""
    import numpy as np
    from shapely.geometry import MultiPoint
    path = _catmull(pts, n)
    m = len(path)
    k = len(widths)
    ws = np.interp(np.linspace(0, k - 1, m), np.arange(k), widths)
    discs = [Point(p[0], p[1]).buffer(w / 2, resolution=24) for p, w in zip(path, ws)]
    parts = [discs[0]]
    for a_, b_ in zip(discs[:-1], discs[1:]):
        parts.append(a_.union(b_).convex_hull)
    return unary_union(parts)


def _disk(r):
    import numpy as np
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    return (xx ** 2 + yy ** 2) <= r * r


def print_clean(mask, ppi, speck_in=0.04, hole_in=0.035, hair_in=0.02, counter_in=0.028, gap_in=0.03):
    """Print-prep for textured art (woodcut, worn print) at its final ppi, sliced per object so it stays fast:
    drop specks and pinholes below the floors, lift hairlines on their centreline, open narrow counters,
    and trim slivers that sit closer than the gap floor to a bigger neighbour (S9 floors)."""
    import numpy as np
    from scipy import ndimage as nd
    from skimage.morphology import skeletonize
    m = mask.copy()

    def drop_specks(m):
        lab, n = nd.label(m)
        if n:
            areas = nd.sum(m, lab, range(1, n + 1))
            small = np.zeros(n + 1, bool); small[1:] = areas < (speck_in * ppi) ** 2
            m[small[lab]] = False
        return m

    m = drop_specks(m)
    holes = nd.binary_fill_holes(m) & ~m
    hl, hn = nd.label(holes)
    if hn:
        ha = nd.sum(holes, hl, range(1, hn + 1))
        fill = np.zeros(hn + 1, bool); fill[1:] = ha < (hole_in * ppi) ** 2
        m[fill[hl]] = True
    # hairlines: grow thin skeleton segments to the target width
    dt = nd.distance_transform_edt(m)
    sk = skeletonize(m)
    tgt = hair_in * ppi
    thin = sk & (2 * dt < tgt)
    if thin.any():
        grow = nd.binary_dilation(thin, structure=_disk(int(np.ceil(tgt / 2))))
        holes0 = nd.binary_fill_holes(m) & ~m
        hl0, hn0 = nd.label(holes0)
        if hn0:
            ha0 = nd.sum(holes0, hl0, range(1, hn0 + 1))
            smallh = np.zeros(hn0 + 1, bool); smallh[1:] = ha0 < (0.15 * ppi) ** 2
            holes0 = smallh[hl0]
        m = m | (grow & ~holes0)            # never grow into a small counter
    # counters: carve ink around enclosed spaces narrower than the floor (per hole, sliced)
    holes = nd.binary_fill_holes(m) & ~m
    hl, hn = nd.label(holes)
    need = counter_in * ppi
    for j, sl in enumerate(nd.find_objects(hl), 1):
        if sl is None:
            continue
        r = int(np.ceil(need / 2)) + 2
        y0, y1 = max(0, sl[0].start - r), min(m.shape[0], sl[0].stop + r)
        x0, x1 = max(0, sl[1].start - r), min(m.shape[1], sl[1].stop + r)
        reg = hl[y0:y1, x0:x1] == j
        if reg.sum() > (0.2 * ppi) ** 2:
            continue
        w = 2 * nd.distance_transform_edt(reg).max()
        if w >= need:
            continue
        rr = int(np.ceil((need - w) / 2)) + 1
        grown = nd.binary_dilation(reg, structure=_disk(rr)) & m[y0:y1, x0:x1]
        m[y0:y1, x0:x1][grown] = False
    # gaps: trim the smaller shape where it sits inside the floor distance of a neighbour
    lab, n = nd.label(m)
    objs = nd.find_objects(lab)
    areas = nd.sum(m, lab, range(1, n + 1)) if n else []
    floor = gap_in * ppi + 1
    pad = int(floor) + 2
    for i in range(1, n + 1):
        sl = objs[i - 1]
        y0, y1 = max(0, sl[0].start - pad), min(m.shape[0], sl[0].stop + pad)
        x0, x1 = max(0, sl[1].start - pad), min(m.shape[1], sl[1].stop + pad)
        sub = lab[y0:y1, x0:x1]
        others = (sub > 0) & (sub != i)
        if not others.any():
            continue
        js = [j for j in np.unique(sub[others]) if areas[j - 1] >= areas[i - 1]]
        if not js:
            continue
        d = nd.distance_transform_edt(~np.isin(sub, js))
        close = (sub == i) & (d < floor)
        if close.any():
            m[y0:y1, x0:x1][close] = False
    return drop_specks(m)


def T_shaped(text, font, size, var=None):
    """Whole-string shaping (raqm: ligatures, contextual joins) for connecting scripts. Rendered at 1200 px,
    traced (font outline at high res), scaled to `size`. Baseline at y=0, pen at x=0."""
    from PIL import ImageFont, ImageDraw
    big = 1200
    f = ImageFont.truetype(fpath(font), big)
    if var:
        f.set_variation_by_axes(var)
    W = int(f.getlength(text) + 2 * big)
    H = int(big * 3)
    im = Image.new('L', (W, H), 0)
    ImageDraw.Draw(im).text((big, int(big * 1.8)), text, font=f, fill=255, anchor='ls')
    import numpy as np
    g = vtype.mask_to_geom(np.array(im) > 127)
    g = affinity.translate(g, -big, -int(big * 1.8))
    s = size / big
    return affinity.scale(g, s, s, origin=(0, 0)), f.getlength(text) * s
