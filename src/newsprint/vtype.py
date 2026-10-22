"""Vector type helpers: font -> polygons (via high-res raster + potrace, sub-pixel accurate) -> shapely geometry,
true mitred offsets for keylines/inlines, SVG output, binary-alpha raster at any DPI.
Used for lettering that must stay crisp (Camelot inline wordmark, embroidery files)."""
import io, numpy as np
from PIL import Image, ImageDraw, ImageFont
import potrace, cairosvg
from shapely.geometry import Polygon, MultiPolygon, box
from shapely.ops import unary_union
from shapely import affinity

FONTDIRS = ["/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/fonts_bl",
            "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts"]

def _font(name, size, var=None):
    import os
    for d in FONTDIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            if var:
                f.set_variation_by_axes(var)
            return f
    f = ImageFont.truetype(name, size)
    if var: f.set_variation_by_axes(var)
    return f

def text_mask(text, font, size=1400, var=None, tracking=0.0):
    """High-res raster of a text line (raqm layout = kerning). tracking in em, applied per glyph."""
    f = _font(font, size, var)
    if tracking == 0:
        bb = f.getbbox(text); W, H = bb[2] - bb[0] + size, bb[3] - bb[1] + size
        im = Image.new("L", (W, H), 0); ImageDraw.Draw(im).text((size // 2 - bb[0], size // 2 - bb[1]), text, font=f, fill=255)
    else:
        adv = [f.getlength(text[:i + 1]) - f.getlength(text[:i]) for i in range(len(text))]
        W = int(sum(adv) + tracking * size * len(text) + 2 * size); H = int(size * 2.4)
        im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); x = size
        for i, ch in enumerate(text):
            kern = (f.getlength(text[:i + 1]) - f.getlength(text[:i])) if i else adv[0]
            d.text((x, size * 0.4), ch, font=f, fill=255); x += kern + tracking * size
    a = np.array(im) > 127
    ys, xs = np.where(a); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def mask_to_geom(mask, alphamax=0.55, samples=12):
    """potrace the mask, sample curves into rings, even-odd XOR -> shapely geometry in pixel units (y down)."""
    bm = potrace.Bitmap(~mask.astype(bool))   # potracer polarity: trace the inverse to get ink paths
    plist = bm.trace(turdsize=4, alphamax=alphamax, opticurve=True, opttolerance=0.1)
    geom = None
    for curve in plist:
        pts = [(curve.start_point.x, curve.start_point.y)]; p0 = curve.start_point
        for seg in curve.segments:
            if seg.is_corner:
                pts += [(seg.c.x, seg.c.y), (seg.end_point.x, seg.end_point.y)]
            else:
                c1, c2, e = seg.c1, seg.c2, seg.end_point
                for t in np.linspace(0, 1, samples + 1)[1:]:
                    x = (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * c1.x + 3 * (1 - t) * t ** 2 * c2.x + t ** 3 * e.x
                    y = (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * c1.y + 3 * (1 - t) * t ** 2 * c2.y + t ** 3 * e.y
                    pts.append((x, y))
            p0 = seg.end_point
        if len(pts) < 3: continue
        poly = Polygon(pts).buffer(0)
        geom = poly if geom is None else geom.symmetric_difference(poly)
    return geom

def text_geom(text, font, size=1000, var=None, tracking=0.0):
    """Geometry of a text run with the baseline at y=0 and the pen starting at x=0 (pixel units at `size`).
    Per-glyph placement with font advances + raqm pair kerning; tracking in em. Returns (geom, advance)."""
    f = _font(font, size, var)
    pad = size
    W = int(f.getlength(text) + tracking * size * len(text) + 2 * pad); H = int(size * 3)
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im); x = pad; base = int(size * 1.8)
    for i, ch in enumerate(text):
        d.text((x, base), ch, font=f, fill=255, anchor="ls")
        nxt = text[i:i + 2]
        adv = (f.getlength(nxt) - f.getlength(text[i + 1:i + 2])) if len(nxt) == 2 else f.getlength(ch)   # includes kerning
        x += adv + tracking * size
    a = np.array(im) > 127
    g = mask_to_geom(a)
    return affinity.translate(g, -pad, -base), x - pad - tracking * size

def run(parts):
    """parts: list of (text, font, size, var, tracking, gap_after_em). Concatenate on one baseline."""
    out = []; x = 0
    for text, font, size, var, tr, gap in parts:
        g, adv = text_geom(text, font, size, var, tr)
        out.append(affinity.translate(g, x, 0)); x += adv + gap * size
    return unary_union(out)

def offset(g, d, mitre=2.5):
    return g.buffer(d, join_style="mitre", mitre_limit=mitre) if d > 0 else g.buffer(d, join_style="mitre", mitre_limit=mitre)

def inline_word(g, keyline, channel, mitre=2.5):
    """Bag construction: solid letter g + white channel + outer keyline (all one ink). Returns ink geometry."""
    ch = offset(g, channel, mitre); kl = offset(g, channel + keyline, mitre)
    return unary_union([g, kl.difference(ch)])

def geom_bounds(g): return g.bounds

def place(g, x, y, scale=1.0):
    """scale about origin then move so the geometry's top-left bbox corner lands at (x, y)."""
    g = affinity.scale(g, scale, scale, origin=(0, 0))
    minx, miny, _, _ = g.bounds
    return affinity.translate(g, x - minx, y - miny)

def to_svg_path(g):
    polys = [g] if isinstance(g, Polygon) else list(getattr(g, "geoms", []))
    parts = []
    for p in polys:
        if p.is_empty: continue
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords); parts.append("M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in c) + " Z")
    return " ".join(parts)

def svg_doc(layers, W, H):
    """layers: list of (geometry, '#rrggbb'). Units = px of the design canvas."""
    body = "".join(f'<path fill="{c}" fill-rule="evenodd" d="{to_svg_path(g)}"/>' for g, c in layers if g is not None and not g.is_empty)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'

def raster(layers, W, H, out_w=None, out_h=None):
    """Render layers to RGBA with binary alpha (anti-aliasing thresholded): returns PIL RGBA."""
    out_w = out_w or W; out_h = out_h or H
    svg = svg_doc(layers, W, H)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=out_w, output_height=out_h)
    im = np.array(Image.open(io.BytesIO(png)).convert("RGBA"))
    a = im[..., 3] >= 128; im[..., 3] = np.where(a, 255, 0)
    # un-premultiply edge colors: snap every inked pixel to its nearest layer color
    cols = np.array([[int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)] for _, c in layers])
    if len(cols):
        px = im[..., :3][a].astype(int); idx = np.argmin(((px[:, None, :] - cols[None]) ** 2).sum(-1), 1)
        rgb = im[..., :3].copy(); rgb[a] = cols[idx]; im[..., :3] = rgb
    im[~a, :3] = 0
    return Image.fromarray(im, "RGBA")
