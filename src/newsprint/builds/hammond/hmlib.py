"""Hammond wave helpers: mask cleanup, multi-ink potrace vectorizing, binary-alpha RGBA renders."""
import sys, io, re, numpy as np, cv2
from PIL import Image
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import vectorize

def remove_small(m, min_area, conn=8):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), conn)
    keep = np.zeros(n, bool); keep[1:] = st[1:, 4] >= min_area
    return keep[lab]

def fill_small_holes(m, max_area):
    inv = ~m
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv.astype(np.uint8), 4)
    H, W = m.shape; out = m.copy()
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a <= max_area and x > 0 and y > 0 and x + w < W and y + h < H: out[lab == i] = True
    return out

def disk(r):
    r = max(1, int(r)); return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))

def path_d(mask, turdsize=40, alphamax=1.0, opttolerance=0.2):
    svg = vectorize(mask, turdsize=turdsize, alphamax=alphamax, opttolerance=opttolerance)
    return re.search(r' d="([^"]*)"', svg).group(1)

def hexc(rgb): return "#%02X%02X%02X" % tuple(rgb)

def svg_doc(layers, W, H):
    """layers: list of (d, rgb) painted in order."""
    body = "".join(f'<path fill="{hexc(c)}" fill-rule="evenodd" d="{d}"/>' for d, c in layers)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'

def render_layer(d, W, H, out_w, out_h):
    import cairosvg
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><path fill="#000" fill-rule="evenodd" d="{d}"/></svg>'
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=out_w, output_height=out_h, background_color="white")
    return np.array(Image.open(io.BytesIO(png)).convert("L")) < 128

def compose_rgba(layer_masks):
    """layer_masks: list of (bool mask, rgb) in paint order -> RGBA with binary alpha, exact colours."""
    H, W = layer_masks[0][0].shape; out = np.zeros((H, W, 4), np.uint8)
    for m, c in layer_masks:
        out[m, :3] = c; out[m, 3] = 255
    return Image.fromarray(out, "RGBA")

def build_multi(masks_colors, W, H, out_w, stem, turd=40, alphamax=1.0):
    """Vectorize each mask, write <stem>.svg (true vector) and <stem>.png (out_w wide, 300 dpi, binary alpha)."""
    out_h = int(round(H * out_w / W)); layers = []; rl = []
    for m, c in masks_colors:
        d = path_d(m, turdsize=turd, alphamax=alphamax); layers.append((d, c))
        rl.append((render_layer(d, W, H, out_w, out_h), c))
    open(stem + ".svg", "w").write(svg_doc(layers, W, H))
    im = compose_rgba(rl); im.save(stem + ".png", dpi=(300, 300)); return im
