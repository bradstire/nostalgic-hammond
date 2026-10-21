"""Newsprint rebuild toolkit (HQ, 2026-10-21).

Pipeline B for FB-screenshot-quality newspaper ads:
  1. Real-ESRGAN x4 (anime model) for large type  -> keep authentic letterforms
  2. Re-typeset small copy in a matched face, metrics fitted to the original
     line boxes (same string => same ink height/width)                 -> legible
  3. Roughen rebuilt type (ink spread + edge grain) so it sits with the SR type
  4. Photos: Real-ESRGAN x4plus -> grayscale -> deliberate re-screened halftone
  5. Composite -> 1-bit, binary-alpha PNG at 300 dpi (+ potrace SVG downstream)
"""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

FONTS = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts"
SS = 3  # supersample factor for text rendering


def vfont(name, size, axes=None):
    f = ImageFont.truetype(f"{FONTS}/{name}", int(size))
    if axes:
        names = [a["name"].decode() if isinstance(a["name"], bytes) else a["name"] for a in f.get_variation_axes()]
        vals = []
        for a, n in zip(f.get_variation_axes(), names):
            key = {"Weight": "wght", "Width": "wdth", "Optical size": "opsz"}.get(n, n)
            vals.append(axes.get(key, a["default"]))
        f.set_variation_by_axes(vals)
    return f


BULLET = "●"


def render_text(text, fontname, size, axes=None, tracking=0.0, xscale=1.0):
    """Render text to a float ink mask (1=ink) at SS x size; returns (mask, ink_bbox).
    BULLET (U+25CF) is drawn as a filled circle sized to the cap height.
    xscale squeezes/stretches horizontally (for condensed faces without a width axis)."""
    f = vfont(fontname, size * SS, axes)
    S = size * SS
    cap = f.getbbox("H")[3] - f.getbbox("H")[1]
    top_cap = f.getbbox("H")[1]
    blen = cap * 0.95
    w = int(sum((blen if ch == BULLET else f.getlength(ch)) for ch in text) + abs(tracking) * S * len(text) + S * 2)
    h = int(S * 2.2)
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    x = S * 0.5; y = S * 0.4
    for ch in text:
        if ch == BULLET:
            r = cap * 0.36; cy = y + top_cap + cap / 2; cx = x + blen / 2
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
            x += blen + tracking * S
        else:
            d.text((x, y), ch, font=f, fill=255)
            x += f.getlength(ch) + tracking * S
    a = np.asarray(im, np.float32) / 255.0
    if xscale != 1.0:
        a = cv2.resize(a, (max(1, int(a.shape[1] * xscale)), a.shape[0]), interpolation=cv2.INTER_AREA)
    ys, xs = np.where(a > 0.5)
    return a, (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)


def fit_xscale(text, fontname, box_w, box_h, axes=None, tracking=0.0, xs_range=(0.55, 1.2)):
    """Fit size by ink height, then horizontal scale by ink width. Returns (size, xscale)."""
    lo, hi = 4.0, 400.0
    for _ in range(26):
        mid = (lo + hi) / 2
        _, (x0, y0, x1, y1) = render_text(text, fontname, mid, axes, tracking)
        if (y1 - y0) / SS > box_h: hi = mid
        else: lo = mid
    _, (x0, y0, x1, y1) = render_text(text, fontname, lo, axes, tracking)
    xs = box_w / ((x1 - x0) / SS)
    return lo, float(np.clip(xs, *xs_range))


def fit_line(text, fontname, box_w, box_h, axes=None, wdth_range=None, tracking=0.0):
    """Find size (by ink height) then width axis (by ink width) to match a measured box."""
    axes = dict(axes or {})
    # size from height
    lo, hi = 4.0, 400.0
    for _ in range(30):
        mid = (lo + hi) / 2
        _, (x0, y0, x1, y1) = render_text(text, fontname, mid, axes, tracking)
        if (y1 - y0) / SS > box_h: hi = mid
        else: lo = mid
    size = lo
    if wdth_range:
        lo_w, hi_w = wdth_range
        for _ in range(18):
            midw = (lo_w + hi_w) / 2
            axes["wdth"] = midw
            _, (x0, y0, x1, y1) = render_text(text, fontname, size, axes, tracking)
            if (x1 - x0) / SS > box_w: hi_w = midw
            else: lo_w = midw
        axes["wdth"] = lo_w
    return size, axes


def place(canvas_ink, text, fontname, size, axes, x0, y0, x1=None, align="left", justify_w=None, tracking=0.0, xscale=1.0):
    """Composite rendered text into canvas_ink (float, 1=ink). y0 = top of ink box."""
    if justify_w:
        words = text.split(" ")
        rendered = [render_text(w_, fontname, size, axes, tracking, xscale) for w_ in words]
        widths = [(bb[2] - bb[0]) / SS for _, bb in rendered]
        gap = (justify_w - sum(widths)) / max(1, len(words) - 1)
        # common vertical reference: render full line once to get its top
        _, fbb = render_text(text, fontname, size, axes, tracking, xscale)
        x = x0
        for (a, bb), wpx in zip(rendered, widths):
            # align each word on the full-line baseline: words share the same drawing origin y,
            # so offset by (bb_top_word - full_top)
            sub = a[fbb[1]:fbb[3], bb[0]:bb[2]]
            _blit(canvas_ink, sub, x, y0)
            x += wpx + gap
        return
    a, bb = render_text(text, fontname, size, axes, tracking, xscale)
    sub = a[bb[1]:bb[3], bb[0]:bb[2]]
    wpx = sub.shape[1] / SS
    if align == "center" and x1 is not None:
        x0 = x0 + ((x1 - x0) - wpx) / 2
    elif align == "right" and x1 is not None:
        x0 = x1 - wpx
    _blit(canvas_ink, sub, x0, y0)


def _blit(canvas, sub_ss, x0, y0):
    h = max(1, int(round(sub_ss.shape[0] / SS))); w = max(1, int(round(sub_ss.shape[1] / SS)))
    small = cv2.resize(sub_ss, (w, h), interpolation=cv2.INTER_AREA)
    x0 = int(round(x0)); y0 = int(round(y0))
    H, W = canvas.shape
    ys, xs = slice(max(0, y0), min(H, y0 + h)), slice(max(0, x0), min(W, x0 + w))
    canvas[ys, xs] = np.maximum(canvas[ys, xs], small[ys.start - y0: ys.stop - y0, xs.start - x0: xs.stop - x0])


def roughen(ink, spread=0.8, grain=0.10, seed=7):
    """Ink spread + edge grain on a float ink layer; returns boolean ink."""
    rng = np.random.default_rng(seed)
    b = cv2.GaussianBlur(ink, (0, 0), spread)
    lowf = cv2.GaussianBlur(rng.standard_normal(ink.shape).astype(np.float32), (0, 0), 2.5)
    lowf /= (lowf.std() + 1e-6)
    hif = rng.standard_normal(ink.shape).astype(np.float32)
    v = b + grain * (0.6 * lowf + 0.4 * hif) * (b * (1 - b) * 4)  # noise only near edges
    return v > 0.45


def halftone(gray, cell=7.0, angle=45.0, gamma=1.0):
    """Round-dot AM halftone. gray: float 0..1 (1 = white). Returns boolean ink."""
    H, W = gray.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.deg2rad(angle)
    u = (xx * np.cos(t) + yy * np.sin(t)) / cell
    v = (-xx * np.sin(t) + yy * np.cos(t)) / cell
    du = u - np.floor(u) - 0.5; dv = v - np.floor(v) - 0.5
    d = np.sqrt(du * du + dv * dv)  # 0 center .. ~0.707 corner
    darkness = np.clip(1.0 - gray, 0, 1) ** gamma
    # dot radius so that covered area fraction ~= darkness (circle up to r=0.5, then merges)
    r = np.sqrt(darkness / np.pi)
    return d < r


def to_rgba_ink(ink_bool, rgb=(0, 0, 0)):
    H, W = ink_bool.shape
    out = np.zeros((H, W, 4), np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = rgb
    out[..., 3] = np.where(ink_bool, 255, 0)
    return Image.fromarray(out)


def mock(ink_bool, bg=(255, 255, 255), fg=(0, 0, 0), width=1000):
    H, W = ink_bool.shape
    m = np.empty((H, W, 3), np.uint8); m[:] = bg; m[ink_bool] = fg
    return cv2.resize(cv2.cvtColor(m, cv2.COLOR_RGB2BGR), (width, int(H * width / W)), interpolation=cv2.INTER_AREA)


def vectorize(mask, turdsize=2, alphamax=1.0, opttolerance=0.2):
    """potrace (pure-python potracer) -> SVG path string sized to mask (px units).
    Note: potracer needs bool input; earlier testing showed polarity must be checked per run."""
    import potrace
    bm = potrace.Bitmap(~mask.astype(bool))  # potracer polarity: trace the inverse to get ink paths
    plist = bm.trace(turdsize=turdsize, alphamax=alphamax, opticurve=True, opttolerance=opttolerance)
    parts = []
    for curve in plist:
        s = curve.start_point
        d = [f"M{s.x:.2f},{s.y:.2f}"]
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f"L{seg.c.x:.2f},{seg.c.y:.2f}L{seg.end_point.x:.2f},{seg.end_point.y:.2f}")
            else:
                d.append(f"C{seg.c1.x:.2f},{seg.c1.y:.2f} {seg.c2.x:.2f},{seg.c2.y:.2f} {seg.end_point.x:.2f},{seg.end_point.y:.2f}")
        d.append("Z"); parts.append("".join(d))
    H, W = mask.shape
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path fill="#000" fill-rule="evenodd" d="{" ".join(parts)}"/></svg>')


def render_svg(svg, W, H):
    import cairosvg, io
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=W, output_height=H, background_color="white")
    im = np.array(Image.open(io.BytesIO(png)).convert("L"))
    return im < 128
