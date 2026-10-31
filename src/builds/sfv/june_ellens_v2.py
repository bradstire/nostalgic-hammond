"""June Ellen's v2 (HQ, 2026-10-31): the sign itself, not just its name.

Brad 10-31: the SFV redraws read dull at thumbnail size next to Hattiesburg; June Ellen's was a font-set script
and a locator line (7 sq in of ink). The 1972 photos of the boulevard (Rick McCloskey's Van Nuys Boulevard
series, posted to Facebook: contact sheet + 'Donuts' frame) show the whole storefront sign: the neon script
'June Ellen's' over six lit panels, one letter each, D O N U T S, a white face with a dark oval and a white
bold letter. Only the business's sign is drawn; nothing of the photographs is used.

- Panel row: one homography for the six coplanar panels, fitted on the panel corners (D, O, N full quads;
  U, T, S bottom corners), 1.4 px mean reprojection error; the fit gives panel 1 : 1.80 and gap 0.43 panel
  widths. x4 Real-ESRGAN (x4plus) before rectifying at 600 px per panel width.
- Ovals: measured on D, O, U (0.88-0.905 x 1.57-1.585 panel widths, centred) -> one ellipse 0.895 x 1.58,
  centred at 0.905. Panels and ovals constructed in those measured proportions (declared redrawn).
- Letters D O N U T: traced (R21; cap ~550 px in the rectified x4 frame, ~110-190 px in the photo), shading
  removed with a fitted surface (D O U T) or GrabCut (N); close/open r5 (0.9 % of cap), smoothing sigma 12
  (2.2 % of cap). Positions kept inside each panel (whole-face, no per-letter moves).
- S: the frame cuts the top of the S in the only legible source; the contact-sheet frames show it ~20 px
  -> re-set in Bebas Neue (best match to the five traced letters: mean IoU 0.904 over D O N U T), fitted
  to the traced letters' cap height and width ratio (R21 reason a).
- 'June Ellen's': Pacifico, as v1 (R21 reason a: the neon script is ~10-25 px cap in every frame).
- House line: VAN NUYS BLVD. (R21 rule 4).
Two inks on the black tee: cream faces/letters/script, red ovals.
"""
import json, math, os, sys
import numpy as np
from PIL import Image
from shapely.geometry import box, Point
from shapely.ops import unary_union
from shapely import affinity

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w2lib import *  # noqa
import vtype

IN = '/home/claude/print-assets/sfv/wave2/r21/inputs/je_v2'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/print-assets/sfv/wave2'
meta = json.load(open(IN + '/rect_meta.json'))
G, HP, SRC = meta['g'], meta['h'], meta['S']          # gap, panel height (panel widths), px per panel width in the traces
P = 380.0                                             # panel width in master px (300 dpi)
k = P / SRC
OW, OH, OCY = 0.895, 1.58, 0.905
CREAM, RED = '#F4ECDD', '#8B0000'

decl = {'typeset': [], 'exempt': [], 'redrawn': []}
def declare(kind, g, note, pad=6):
    b = g.bounds if hasattr(g, 'bounds') else g
    decl[kind].append([[b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad], note])

top = 0.0      # panel row top; the script goes above (negative y), shifted at the end
panels, ovals, letters = [], [], []
for i, ch in enumerate('DONUTS'):
    x0 = i * (1 + G) * P
    pan = box(x0, top, x0 + P, top + HP * P)
    ov = affinity.scale(Point(x0 + 0.5 * P, top + OCY * P).buffer(1.0, resolution=128), OW * P / 2, OH * P / 2)
    panels.append(pan); ovals.append(ov)
    if ch != 'S':
        m = np.array(Image.open(f'{IN}/letter_{ch}.png').convert('L')) > 127
        import cv2
        mm = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
        mm = cv2.morphologyEx(mm, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))) > 0
        lg = trace_geom(mm, alphamax=1.0, smooth_sigma=12)
        lg = affinity.scale(lg, k, k, origin=(0, 0))
        lg = affinity.translate(lg, x0, top)
        letters.append(lg)
    else:
        caps = [l.bounds[3] - l.bounds[1] for l in letters]
        ws = [l.bounds[2] - l.bounds[0] for l in letters]
        cap = float(np.median(caps)); wr = float(np.median([w / c for w, c in zip(ws, caps)]))
        sg, _ = T('S', 'BebasNeue-Regular.ttf', size=1000)
        sb = sg.bounds
        sg = affinity.scale(sg, wr * cap / (sb[2] - sb[0]), cap / (sb[3] - sb[1]), origin=(sb[0], sb[1]))
        ref = letters[0].bounds                           # same top/bottom as the traced row, centred in the panel
        tops = [l.bounds[1] for l in letters]; bots = [l.bounds[3] for l in letters]
        sg = move(sg, cx=x0 + 0.5 * P, y=float(np.median(tops)))
        letters.append(sg)
        declare('typeset', sg, "Bebas Neue (S only); R21 reason a: the S's top is cut off by the frame in the only source above the floor; fitted to the traced letters' cap height and width ratio")
row = unary_union(letters[:5])
declare('exempt', box(0, top, 6 * P + 5 * G * P, top + HP * P), 'DONUTS: D O N U T traced from the rectified 1972 photo, one homography for the coplanar panel row (R21)')
declare('redrawn', box(0, top, 6 * P + 5 * G * P, top + HP * P), "panels and ovals: constructed in the measured proportions (panel 1 : 1.80, oval 0.895 x 1.58 at 0.905; mean of D, O, U)")

rowW = 6 * P + 5 * G * P
cx = rowW / 2
# script above the row (R21 reason a), as v1
s1, adv1 = T_shaped("June Ellen", 'Pacifico-Regular.ttf', size=560)
s2, _ = T("’s", 'Pacifico-Regular.ttf', size=560, track=0.04)
sc = unary_union([s1, affinity.translate(s2, adv1 - 30, 0)])
sc = scale_to(sc, w=rowW * 0.86)
sc = move(sc, cx=cx, bottom=top - 0.22 * P)
declare('typeset', sc, "Pacifico (the Cruise Night script); R21 reason a: the neon script is ~10-25 px cap in every frame")
decl['exempt'].append([[sc.bounds[0] - 6, sc.bounds[1] - 6, sc.bounds[2] + 6, sc.bounds[3] + 6], "LEVEL only: font-set script on a level baseline; the raised apostrophe-s reads as a tilt to the gate"])
# house line
hl, _ = T('VAN NUYS BLVD.', 'Jost[wght].ttf', cap=100, var=[600], track=0.22)
hl = move(hl, cx=cx, y=top + HP * P + 0.30 * P)
declare('typeset', hl, 'Jost SemiBold (house locator line, R21 rule 4)')

face = unary_union(panels).difference(unary_union(ovals))
L = unary_union(letters)
cream = unary_union([face, L.intersection(unary_union(ovals)), sc, hl]).buffer(0)
red = unary_union(ovals).difference(L).buffer(0)

# frame + save (300 dpi, binary alpha), two inks
allg = unary_union([cream, red])
b = allg.bounds; pad = 30
ox, oy = math.floor(b[0]) - pad, math.floor(b[1]) - pad
W, H = math.ceil(b[2] - ox) + pad, math.ceil(b[3] - oy) + pad
cr = affinity.translate(cream, -ox, -oy); rd = affinity.translate(red, -ox, -oy)
im = vtype.raster([(cr, CREAM), (rd, RED)], W, H)
name = 'sfv_june_ellens_v2'
os.makedirs(OUT, exist_ok=True)
im.save(f'{OUT}/{name}.png', dpi=(300, 300))
open(f'{OUT}/{name}.svg', 'w').write(vtype.svg_doc([(cr, CREAM), (rd, RED)], W, H))
prov = {kk: [[[round(bb[0] - ox), round(bb[1] - oy), round(bb[2] - ox), round(bb[3] - oy)], n] for bb, n in v] for kk, v in decl.items()}
prov.update({'frame': {'scale': 1.0, 'ox': ox, 'oy': oy, 'trace_px_per_panel': SRC, 'panel_px': P},
             'rules': ['R21'], 'ink': [CREAM, RED], 'print_width_in': round(W / 300, 3), 'print_height_in': round(H / 300, 3),
             'source': "Rick McCloskey, 'Donuts' June Ellen's on Van Nuys Boulevard, 1972 (Facebook) + contact sheet; the sign only"})
json.dump(prov, open(f'{OUT}/{name}.prov.json', 'w'), indent=1)
a = np.array(im)[..., 3] > 0
print(f'{name}: {W}x{H}px = {W/300:.2f} x {H/300:.2f} in; ink {a.sum()/90000:.1f} sq in')
