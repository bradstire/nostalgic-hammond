"""Camelot Music v3 (Brad 10-22: "tighten up — reference signage, bag; outlines weak").
Letterforms matched to the 1970s bag + 1974 Cloverleaf sign: Old English swash C (Manufacturing Consent, OFL)
+ heavy textura lowercase / three-stem M (Grenze Gotisch Black, OFL) at natural width (v2 wrongly compressed it).
Bag construction rebuilt as TRUE vector offsets (mitred): red fill | open channel | red keyline — no raster rings.
Groove arcs are vector rings. Locator = bag's bold oblique grotesque (TeX Gyre Heros Bold, GUST licence, 12deg).
Everything 300 dpi, binary alpha; SVG masters saved alongside.
Brad 10-22 13:34: the outline stays ONLY on the 1970s bag arch; sign + tri-stripe outlined versions are superseded (_outlined)."""
import sys, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from vtype import run, text_geom, inline_word, raster, svg_doc, affinity, unary_union
from shapely.geometry import Point, box
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/camelot"
DPI = 300
RED, BLUE, WHITE, YEL, CYAN = "#C62832", "#2E49B8", "#FAFAFA", "#F2C230", "#2FA7D8"
G, GV, MC = "GrenzeGotisch[wght].ttf", [900], "ManufacturingConsent-Regular.ttf"
HEROS = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts/texgyreheros-bold.otf"
TR = 0.09   # tracking (em) so every letter keeps its own keyline, as on the bag

def camelot():  return run([("C", MC, 1180, None, 0, 0.02), ("amelot", G, 1000, GV, TR, 0)])
def music():    return run([("Music", G, 1000, GV, TR, 0)])
def oneline():  return run([("C", MC, 1180, None, 0, 0.02), ("amelot", G, 1000, GV, TR, 0.30), ("Music", G, 1000, GV, TR, 0)])

def fit(g, width_px=None, height_px=None):
    b = g.bounds; s = min(width_px / (b[2] - b[0]) if width_px else 1e9, height_px / (b[3] - b[1]) if height_px else 1e9)
    g = affinity.scale(g, s, s, origin=(0, 0)); b = g.bounds
    return affinity.translate(g, -b[0], -b[1])

def at(g, x, y):   # top-left of bbox to (x, y)
    b = g.bounds; return affinity.translate(g, x - b[0], y - b[1])

def centered(g, cx, y):
    b = g.bounds; return affinity.translate(g, cx - (b[0] + b[2]) / 2, y - b[1])

def locator(text, width_px):
    g, _ = text_geom(text, HEROS, 400, None, 0.06)
    g = affinity.skew(g, xs=-12, origin=(0, 0))          # oblique like the bag's tagline
    return fit(g, width_px=width_px)

def save(layers, W, H, name):
    raster(layers, W, H).save(f"{D}/{name}.png", dpi=(DPI, DPI))
    open(f"{D}/{name}.svg", "w").write(svg_doc(layers, W, H))
    print(f"{name}: {W / DPI:.2f} x {H / DPI:.2f} in")

def arcs(cx, cy, radii, widths):
    rings = []
    for r, w in zip(radii, widths):
        rings.append(Point(cx, cy).buffer(r + w / 2, 256).difference(Point(cx, cy).buffer(r - w / 2, 256)))
    return unary_union(rings).intersection(box(cx - 1e5, cy - 1e5, cx + 1e5, cy))   # upper half, square cut ends

def inline(g, k_in, c_in):  return inline_word(g, keyline=k_in * DPI, channel=c_in * DPI)

if __name__ == "__main__":
    W = int(10.5 * DPI)
    # A) 1970s BAG: stacked inline wordmark inside blue groove arcs + bag-style locator
    cam = fit(camelot(), width_px=int(6.6 * DPI)); mus = fit(music(), width_px=int(5.3 * DPI))
    cam_i = inline(cam, 0.040, 0.045); mus_i = inline(mus, 0.040, 0.045)
    cx = W / 2; top = int(0.15 * DPI)
    R0 = int(4.6 * DPI); cy = top + R0 + int(0.12 * DPI)
    rad = [R0 - i * int(0.42 * DPI) for i in range(3)]; wid = [int(0.24 * DPI)] * 3
    A = arcs(cx, cy, rad, wid)
    y_word = cy - int(2.55 * DPI)
    cam_i = centered(cam_i, cx, y_word); b = cam_i.bounds
    mus_i = centered(mus_i, cx, b[3] + int(0.10 * DPI)); b2 = mus_i.bounds
    loc = centered(locator("CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974", int(6.4 * DPI)), cx, max(b2[3], cy) + int(0.28 * DPI))
    H = int(loc.bounds[3] + 0.15 * DPI)
    word = unary_union([cam_i, mus_i])
    A = A.difference(word.buffer(0.09 * DPI, join_style="mitre", mitre_limit=2.5))   # grooves pass BEHIND the lettering, as on the bag
    save([(A, BLUE), (unary_union([word, loc]), RED)], W, H, "camelot_v3_bag1974")

    # B) 1974 SIGN: one line, inline red wordmark + locator (blue for light tees, white for dark)
    one = fit(oneline(), width_px=int(10.0 * DPI)); one_i = at(inline(one, 0.035, 0.040), int(0.25 * DPI), int(0.1 * DPI))
    ob = one_i.bounds
    loc2 = centered(locator("CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974", int(6.8 * DPI)), (ob[0] + ob[2]) / 2, ob[3] + int(0.22 * DPI))
    H2 = int(loc2.bounds[3] + 0.1 * DPI); W2 = int(ob[2] + 0.25 * DPI)
    save([(one_i, RED), (loc2, BLUE)], W2, H2, "camelot_v3_sign_red_blue_outlined")
    save([(one_i, RED), (loc2, WHITE)], W2, H2, "camelot_v3_sign_red_white_outlined")

    # C) 1990s tri-stripe nod: inline wordmark over yellow / cyan / red bars + locator
    sw = ob[2] - ob[0]; x0 = ob[0]; y0 = ob[3] + int(0.16 * DPI); bh = int(0.17 * DPI); gap = int(0.07 * DPI)
    bars = [(box(x0, y0 + i * (bh + gap), x0 + sw, y0 + i * (bh + gap) + bh), c) for i, c in enumerate((YEL, CYAN, RED))]
    loc3 = centered(locator("CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974", int(6.8 * DPI)), (ob[0] + ob[2]) / 2, y0 + 3 * (bh + gap) + int(0.12 * DPI))
    H3 = int(loc3.bounds[3] + 0.1 * DPI)
    save([(bars[0][0], YEL), (bars[1][0], CYAN), (unary_union([one_i, bars[2][0], loc3]), RED)], W2, H3, "camelot_v3_tristripe_outlined")
