"""Nostalgic San Fernando Valley, wave 2 masters (HQ, 2026-10-27/28).

Selection and evidence: sfv2/SCORING.md (Brad's brief 10-27 22:10). Each function builds one master from
its sources (listed in the docstring) with w2lib: font-set type, constructed sign geometry, and traced
elements only where the source is hand lettering or illustration (declared as exemptions).

Usage: python3 wave2_build.py OUTDIR [name ...]
"""
import math, os, sys
from shapely.geometry import Polygon, LineString, box, Point
from shapely.ops import unary_union
from shapely import affinity

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w2lib import *  # noqa

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/print-assets/sfv/wave2'
ONLY = set(sys.argv[2:])
BUILDS = {}
WORK = '/home/claude/sfv2/work'
# R21 cleanup budget, calibrated on the traced lettering in Hattiesburg + Hammond v2 (sfv2/calib/CLEANUP_BUDGET.md):
# notches/spurs out with close/open at <= ~1.5 % of cap height, corner-preserving smoothing sigma ~3 % of cap
# (Hammond v2 used 2.8-5.0 %; Hattiesburg ads 0 %: SR + threshold only), ceiling 5 %. Values below are px of each
# trace mask, with that mask's cap height in the comment.
SMOOTH = dict(fm=10,          # cap ~350 px (F) -> 2.9 %
              gemco=8,        # cap 274 px (E) -> 2.9 %, after close/open r4 (1.5 %)
              pizza=7,        # cap ~222 px -> 3.2 %
              dons_lines=2.5, # cap ~85 px -> 2.9 %
              leons_pillows=4, leons_letters=3,   # pillow letters cap ~95 px -> 3.2 %
              leons_cs=2,     # COFFEE SHOP cap ~62 px -> 3.2 %
              vplaza=6,       # letter cap ~365 px -> 1.6 % (edges are already the clipped channel)
              enc_bowl=9,     # BOWL cap ~312 px -> 2.9 %
              enc_encino=3,   # ENCINO cap ~110 px -> 2.7 %
              enc_cs=6,       # Coffee cap ~360 px (per-face rectified) -> 1.7 %
              zodys=10,       # cap ~790 px -> 1.3 % (rectified at 2.2x the x4 scale)
              devon=5,        # cap ~210 px (x4) -> 2.4 %, after close/open r3
              devon_script=4, # script cap ~150 px (x4) -> 2.7 %
              web_W=12,       # W cap ~900 px -> 1.3 %
              web_place=3,    # PLACE cap ~160 px -> 1.9 %
              web_eber=18)    # eber's ascender ~650 px -> 2.8 % (paint chips on the b stem)


def build(fn):
    BUILDS[fn.__name__] = fn
    return fn


# ------------------------------------------------------------------ monoline deco letters (sign geometry)
def _stroke(pts, w):
    return LineString(pts).buffer(w / 2, cap_style=2, join_style=2, mitre_limit=6)


def deco_letter(ch, H, w, Wd):
    """Monoline condensed deco capital, constructed (not traced): cap height H, stroke w, outer width Wd.
    Baseline y=0, left edge x=0, y up is negative. Returns geometry."""
    band = box(-w * 2, -H, Wd + w * 2, 0)
    hw = w / 2
    ext = w * 3
    if ch == 'V' or ch == 'A':
        # exact polygons: outer triangle minus the inner triangle whose legs are offset w inward
        al = math.atan2(Wd / 2, H)
        dx = w / math.cos(al)                 # horizontal stroke thickness
        dy = w / math.sin(al)                 # vertical offset of the parallel inner apex
        outer = Polygon([(0, -H), (Wd, -H), (Wd / 2, 0)])
        inner = Polygon([(dx, -H - 1), (Wd - dx, -H - 1), (Wd / 2, -dy)])
        g = outer.difference(inner)
        if ch == 'A':
            g = affinity.scale(g, 1, -1, origin=(0, -H / 2))
            yb = -H * 0.22
            g = g.union(box(0, yb - w * 0.40, Wd, yb + w * 0.40).intersection(Polygon([(0, 0), (Wd / 2, -H), (Wd, 0)])))
        return g
    if ch == 'L':
        return unary_union([box(0, -H, w, 0), box(0, -w, Wd, 0)])
    if ch == 'E':
        return unary_union([box(0, -H, w, 0), box(0, -H, Wd, -H + w), box(0, -w, Wd, 0),
                            box(0, -H * 0.47 - w / 2 + H*0.0, Wd * 0.82, -H * 0.47 + w / 2)])
    if ch == 'Y':
        jy = -H * 0.42
        half = (Wd - w) / 2
        p1 = [(hw - (half / (H + jy)) * ext * 0, -H - ext), (Wd / 2, jy)]
        arms = _stroke([(hw, -H - ext * 0.5), (Wd / 2, jy), (Wd - hw, -H - ext * 0.5)], w)
        g = unary_union([arms, box(Wd / 2 - hw, jy - w, Wd / 2 + hw, 0)]).intersection(band)
        return g
    if ch == 'P':
        bh = H * 0.56
        rx = min(bh / 2, Wd * 0.62)
        def dshape(x0, y0, x1, y1, rxx):
            ry = (y1 - y0) / 2
            cx, cy = x1 - rxx, (y0 + y1) / 2
            pts = [(x0, y0), (cx, y0)] + [(cx + rxx * math.sin(t), cy - ry * math.cos(t)) for t in [i * math.pi / 60 for i in range(61)]] + [(cx, y1), (x0, y1)]
            return Polygon(pts)
        outer = dshape(0, -H, Wd, -H + bh, rx)
        inner = dshape(w * 0.5, -H + w, Wd - w, -H + bh - w, max(rx - w, 1))
        return unary_union([box(0, -H, w, 0), outer.difference(inner)])
    if ch == 'Z':
        top = box(0, -H, Wd, -H + w)
        bot = box(0, -w, Wd, 0)
        diag = _stroke([(Wd - w * 0.55, -H + w * 0.5), (w * 0.55, -w * 0.5)], w * 1.05)
        return unary_union([top, bot, diag]).intersection(box(0, -H, Wd, 0))
    raise ValueError(ch)


def deco_word(word, H, w, widths, gap):
    x = 0
    parts = []
    for ch in word:
        Wd = widths[ch] * H
        parts.append(affinity.translate(deco_letter(ch, H, w, Wd), x, 0))
        x += Wd + gap
    return unary_union(parts), x - gap


# ------------------------------------------------------------------ C33 Valley Plaza
@build
def valley_plaza():
    """Valley Plaza sign, Laurel Canyon & Victory, North Hollywood (centre opened Aug 12 1951; demolition
    began Oct 29 2025; VRM saved the sign). Source: LAist file photo (src/C33). Redrawn as constructed
    geometry: the stepped-crown panel, the double deco inline border, and the monoline channel letters with
    their neon inline. One ink: panel in ink, letters and border knocked out (the sign was cream with dark
    letters, so cream ink on a dark tee reads the way the sign did)."""
    a = Art('sfv_valley_plaza')
    PW = 2700.0                      # panel width = 9.0 in
    body_top, body_bot = 330.0, 330.0 + PW * 0.93
    crown_x0, crown_x1 = PW * 0.17, PW * 0.83
    crown_top = 0.0
    # panel: body + crown with a shallow arched top
    arc = [(crown_x0 + (crown_x1 - crown_x0) * t, crown_top + 70 * (1 - math.sin(math.pi * t)) ** 1.0)
           for t in [i / 60 for i in range(61)]]
    crown = Polygon([(crown_x0, body_top + 10)] + arc + [(crown_x1, body_top + 10)])
    body = box(0, body_top, PW, body_bot)
    panel = unary_union([body, crown.buffer(0)])
    panel = panel.buffer(-14, join_style=1).buffer(14, join_style=1)   # eased corners like the cast panel
    a.add(panel)
    a.declare('redrawn', panel, 'sign panel: constructed geometry after the LAist photo')
    # double inline border: ziggurat top (two steps each side) - centreline path, then two knocked-out lines
    ins = PW * 0.055
    yt = body_top + PW * 0.075
    s1, s2 = PW * 0.045, PW * 0.04
    path = [(ins, body_bot - ins), (ins, yt), (crown_x0 + PW * 0.03, yt), (crown_x0 + PW * 0.03, yt - s1),
            (crown_x0 + PW * 0.03 + s2, yt - s1), (crown_x0 + PW * 0.03 + s2, yt - 2 * s1)]
    mid = PW / 2
    mirror = [(2 * mid - x, y) for x, y in reversed(path)]
    path = path + mirror
    outline = Polygon(path)
    lw, gap = 24.0, 30.0
    line1 = ring(outline, lw, inner_offset=0)
    line2 = ring(outline, lw, inner_offset=-(lw + gap))
    a.cut(line1)
    a.cut(line2)
    a.declare('redrawn', outline.buffer(10), 'double inline border: constructed (two 0.08 in lines, 0.10 in apart)')
    # letters
    H1 = PW * 0.30
    w = H1 * 0.12
    widths = dict(V=0.40, A=0.42, L=0.27, E=0.30, Y=0.42, P=0.31, Z=0.35)
    v, vw = deco_word('VALLEY', H1, w, widths, H1 * 0.075)
    p, pw = deco_word('PLAZA', H1, w, widths, H1 * 0.085)
    inner_l, inner_r = ins + lw * 2 + gap, PW - ins - lw * 2 - gap
    lead = H1 * 0.30
    inner_top = yt + lw * 2 + gap
    inner_bot = body_bot - ins - lw * 2 - gap
    block = H1 * 2 + lead
    y0 = inner_top + (inner_bot - inner_top - block) / 2 + H1 * 0.02
    v = move(v, cx=mid, y=y0)
    p = move(p, cx=mid, y=y0 + H1 + lead)
    for word in (v, p):
        a.cut(word)
        # neon inline: a thin ink line along each stroke's centre (inset to a 0.03 in tube)
        tube = word.buffer(-(w / 2 - 9), join_style=2, mitre_limit=6)
        a.add(tube)
    a.declare('redrawn', v, 'VALLEY: monoline channel letters constructed from the sign photo (R21 reason d: dimensional channel letters, L45)')
    a.declare('redrawn', p, 'PLAZA: monoline channel letters constructed from the sign photo (R21 reason d: dimensional channel letters, L45)')
    # pole stub
    pole = box(mid - 70, body_bot - 2, mid + 70, body_bot + 150)
    a.add(pole)
    # caption
    cap, _ = T('NORTH HOLLYWOOD  ·  1951', 'Jost[wght].ttf', cap=95, var=[600], track=0.16)
    cap = move(cap, cx=mid, y=body_bot + 230)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    return a


# ------------------------------------------------------------------ C50 Zodys
def vhex(cx, y0, w, h, tip):
    x0, x1 = cx - w / 2, cx + w / 2
    return Polygon([(cx, y0), (x1, y0 + tip), (x1, y0 + h - tip), (cx, y0 + h), (x0, y0 + h - tip), (x0, y0 + tip)])


@build
def zodys():
    """Zodys, 8201 Topanga Canyon Blvd, Canoga Park (opened Sept 27 1962; chain closed 1986). Source: LAPL
    Valley Times photo 00057938 'Radio wave opens doors of Zodys' (src/C50; Brad's pull s2204-25 is the same
    canopy), x4 Real-ESRGAN. R21 pass 2: each of the five hexagon letter boxes is rectified on its own six corners
    to one common hexagon (the photo's own proportions, 2.65 : 1), and the letter on it is traced: the canopy's own
    condensed slab-serif Z O D Y S (~90 px cap in the source; v1 re-set them in Kameron). The S box runs off the
    photo's edge, so it is rectified on its four visible corners and its residual scale/shear matched to the O.
    Boxes are constructed as plain faces (as on the canopy); letters knocked out."""
    a = Art('sfv_zodys')
    TW, TH, tip, gap = 408.0, 1080.0, 110.0, 110.0
    xs = [TW / 2 + i * (TW + gap) for i in range(5)]
    for cx, ch in zip(xs, 'ZODYS'):
        hx = vhex(cx, 0, TW, TH, tip)
        a.add(hx)                                                # plain white face, as on the canopy (v1's keyline retired)
        g = mask_geom(WORK + f'/r21/zod_{ch}.png', smooth=SMOOTH['zodys'])
        g = affinity.translate(g, cx - TW / 2, 0)                 # traced in the box's own canonical frame
        a.cut(g)
    a.declare('exempt', box(0, 0, xs[-1] + TW / 2, TH), 'ZODYS: the canopy letters traced, one rectified box at a time (R21)')
    a.declare('redrawn', box(0, 0, xs[-1] + TW / 2, TH), 'hexagon boxes: constructed in the photo proportions (plain faces; v1 keylines retired)')
    mid = (xs[0] + xs[-1]) / 2
    cap, _ = T('CANOGA PARK  ·  1962', 'Jost[wght].ttf', cap=100, var=[600], track=0.18)
    cap = move(cap, cx=mid, y=TH + 120)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    return a


# ------------------------------------------------------------------ C49 White Front
def ellipse_pt(cx, cy, rx, ry, t):
    return cx + rx * math.cos(t), cy - ry * math.sin(t)


def ellipse_normal_deg(rx, ry, t):
    # outward normal of x=rx cos t, y=-ry sin t ; rotation (deg, shapely ccw in y-down coords) to align "up" with it
    nx, ny = math.cos(t) / rx, -math.sin(t) / ry
    ang = math.degrees(math.atan2(ny, nx))      # direction of the normal in image coords
    return ang + 90                               # 'up' (0,-1) is at -90 deg


@build
def white_front():
    """White Front, 21300 Roscoe Blvd, Canoga Park (the chain's ninth store, opened May 1963; chain closed
    1974). Source: Brad's VRM post of the early-1970s photo (src/C49) - the parabolic entrance shell with a
    letter box for each letter of WHITE FRONT standing along its crown. Shell and boxes are our own drawing;
    letters set in Rokkitt Bold; 'Canoga Park' set in Yellowtail after the photo's script caption."""
    a = Art('sfv_white_front')
    cx, cy = 1600.0, 1500.0
    rx, ry = 1400.0, 800.0
    outer = Polygon([ellipse_pt(cx, cy, rx, ry, math.pi * i / 300) for i in range(301)])
    inner = Polygon([ellipse_pt(cx, cy + 2, rx - 250, ry - 95, math.pi * i / 300) for i in range(301)])
    shell = outer.difference(inner)
    a.add(shell)
    # rim highlight knocked out just inside the shell's front edge
    rim_o = Polygon([ellipse_pt(cx, cy, rx - 34, ry - 34, math.pi * i / 300) for i in range(301)])
    rim_i = Polygon([ellipse_pt(cx, cy, rx - 50, ry - 50, math.pi * i / 300) for i in range(301)])
    a.cut(rim_o.difference(rim_i).difference(box(0, cy - 60, 9999, 9999)))
    # footings + ground line
    a.add(box(cx - rx - 30, cy - 4, cx - rx + 280, cy + 36))
    a.add(box(cx + rx - 280, cy - 4, cx + rx + 30, cy + 36))
    a.add(box(cx - rx - 260, cy + 70, cx + rx + 260, cy + 92))
    a.declare('redrawn', box(cx - rx - 260, cy - ry - 10, cx + rx + 260, cy + 95), 'entrance shell, ribs, footings: our own drawing after the photo')
    # letter boxes along the crown
    letters = list('WHITE') + [None] + list('FRONT')
    t0, t1 = math.radians(163), math.radians(17)
    n = len(letters)
    TWb, THb = 210.0, 250.0
    lift = THb / 2 + 26
    for i, ch in enumerate(letters):
        if ch is None:
            continue
        t = t0 + (t1 - t0) * i / (n - 1)
        x, y = ellipse_pt(cx, cy, rx, ry, t)
        nx, ny = math.cos(t) / rx, -math.sin(t) / ry
        L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
        px, py = x + nx * lift, y + ny * lift
        rot = math.degrees(math.atan2(ny, nx)) + 90
        tile = box(px - TWb / 2, py - THb / 2, px + TWb / 2, py + THb / 2)
        frame = ring(tile, 22, inner_offset=-22)
        g, _ = T(ch, 'Rokkitt[wght].ttf', cap=150, var=[800])
        if width(g) > TWb - 70:
            g = hscale(g, (TWb - 70) / width(g))
        g = move(g, cx=px, cy=py)
        a.add(affinity.rotate(frame, rot, origin=(px, py)))
        gl = affinity.rotate(g, rot, origin=(px, py))
        a.add(gl)
        a.declare('typeset', gl, 'Rokkitt ExtraBold, rotated to the arch (per-glyph); R21 reason a: arch letters ~12 px cap in the photo')
        # post from the box down to the shell
        a.add(affinity.rotate(box(px - 9, py + THb / 2 - 4, px + 9, py + lift + 10), rot, origin=(px, py)))
    # script + address
    sc, _ = T('Canoga Park', 'Yellowtail-Regular.ttf', size=430)
    sc = move(sc, cx=cx, y=cy + 170)
    a.add(sc, 'typeset', 'Yellowtail; R21 reason a: the photo caption script is ~18 px cap')
    ad, _ = T('21300 ROSCOE BLVD.  ·  OPENED 1963', 'Jost[wght].ttf', cap=88, var=[600], track=0.16)
    ad = move(ad, cx=cx, y=sc.bounds[3] + 110)
    a.add(ad, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'red'
    return a


# ------------------------------------------------------------------ C28 GEMCO
@build
def gemco():
    """GEMCO membership card (Gemco, the members-only department store chain, 1959-1986; Valley stores
    incl. Granada Hills). Source: the membership card on the Roy Hooper Gemco tribute site (src/C28, crop
    only: oval logo, 'DEPARTMENT STORES AND SUPERMARKETS', the diagonal MEMBERSHIP band) + the 1986 VRM
    storefront photo. Card, oval and band are constructed; GEMCO traced from the store sign (R21 pass 2; the
    card shows the same roman); the card's sans lines re-set in Jost Bold / Medium (they are ~6-9 px in the only
    card image: R21 reason a). No member name/number. Tees only: a pending IC025
    caps/footwear application exists (SCORING.md), so no hat."""
    a = Art('sfv_gemco_membership')
    CW, CH = 3000.0, 1890.0
    card = rrect(0, 0, CW, CH, 120)
    a.add(ring(card, 26, inner_offset=-26))
    a.declare('redrawn', card, 'card outline: constructed')
    interior = card.buffer(-60)
    # oval logo
    ov = Point(0, 0).buffer(1, resolution=128)
    ov = affinity.scale(ov, 760, 315)
    ov = affinity.translate(ov, 960, 600)
    a.add(ov)
    # R21: GEMCO is the chain's own letters, traced from the store sign in Brad's pull (s2148-51, ~37 px cap;
    # x4 upscale, perspective rectified, faces only) and set in the card's tight spacing (the card itself is
    # ~13 px cap, below the trace floor). Was Libre Caslon Text Bold.
    gl = mask_geom(WORK + '/r21/gemco_letters_rect_co.png', smooth=SMOOTH['gemco'])
    letters = sorted(getattr(gl, 'geoms', [gl]), key=lambda p: p.bounds[0])
    assert len(letters) == 5, len(letters)
    capk = 205.0 / 274.0                       # E height in the rectified mask = 274 px
    gap = 0.05 * 205
    x = 0.0
    placed = []
    for p in letters:
        p = affinity.scale(p, capk, capk, origin=(0, 0))
        placed.append(affinity.translate(p, x - p.bounds[0], 0))
        x = placed[-1].bounds[2] + gap
    g = unary_union(placed)
    g = move(g, cx=960, cy=600)
    assert g.buffer(40).within(ov), 'GEMCO crowds the oval'
    a.cut(g)
    a.declare('exempt', g.envelope, 'GEMCO: the store-sign letters, traced (R21), spaced as on the membership card')
    # diagonal band with MEMBERSHIP, clipped to the card interior; text centred on the visible band
    ang = -26.0
    bc = (1960, 1250)
    band = box(bc[0] - 2600, bc[1] - 160, bc[0] + 2600, bc[1] + 160)
    band = affinity.rotate(band, ang, origin=bc).intersection(interior)
    a.add(band)
    vc = band.centroid
    vc = Point(vc.x + 150 * math.cos(math.radians(ang)), vc.y + 150 * math.sin(math.radians(ang)))
    m, _ = T('MEMBERSHIP', 'Jost[wght].ttf', cap=175, var=[700], track=0.12)
    m = affinity.rotate(move(m, cx=vc.x, cy=vc.y), ang, origin=(vc.x, vc.y))
    assert m.buffer(30).within(band), 'MEMBERSHIP runs off the band'
    a.cut(m, 'typeset', 'Jost Bold (rotated with the band); R21 reason a: ~9 px cap on the only card image')
    st, _ = T('DEPARTMENT STORES AND SUPERMARKETS', 'Jost[wght].ttf', cap=68, var=[500], track=0.14)
    st = move(st, cx=vc.x - 260, cy=vc.y - 160 - 80)
    st = affinity.rotate(st, ang, origin=(vc.x, vc.y))
    assert st.buffer(30).within(interior), 'small line leaves the card'
    a.add(st, 'typeset', 'Jost Medium (rotated with the band); R21 reason a: ~6 px cap on the only card image')
    a.declare('exempt', unary_union([band, st]).envelope, "LEVEL only: band lettering runs on the card's printed diagonal (deliberate angle)")
    pl, _ = T('SAN FERNANDO VALLEY', 'Jost[wght].ttf', cap=95, var=[600], track=0.2)
    pl = move(pl, cx=CW / 2, y=CH + 130)
    a.add(pl, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'navy'
    return a


# ------------------------------------------------------------------ C51 Leon's
def superellipse(cx, cy, a, b, n=3.5, N=160):
    pts = []
    for i in range(N):
        t = 2 * math.pi * i / N
        c, s_ = math.cos(t), math.sin(t)
        x = a * math.copysign(abs(c) ** (2 / n), c)
        y = b * math.copysign(abs(s_) ** (2 / n), s_)
        pts.append((cx + x, cy + y))
    return Polygon(pts)


@build
def leons():
    """Leon's Steak House & Coffee Shop, 10945 Victory Blvd at Vineland, North Hollywood (opened 1945 by Leon
    Grown; closed July 2003; now a CVS). Source: Brad's two VRM pulls of the pole sign (dup = emphasis); R21 pass 2
    works from s2205-50 (Greyledge photo, the larger of the two: LEONS ~22 px, STEAK HOUSE ~40 px, COFFEE SHOP
    ~21 px cap), x4 Real-ESRGAN, perspective rectified on the STEAK/HOUSE box corners (sfv2/work/r21/leons50_rect.png).
    Traced: the five letter pillows and their letters, the COFFEE SHOP brush letters and the shield (outline smoothed,
    debris on its top edge removed). STEAK HOUSE is re-set (R21 reason c): the channel letters are broken by exposed
    neon tubes and missing faces, so a trace falls apart; each letter is Antonio fitted to its own measured box on
    the rectified photo (position, width, height), not a line of type. Pole, light windows, rail, brackets and the two
    boxes are constructed at their measured positions. Built in rectified-photo px x K."""
    a = Art('sfv_leons')
    K = 3.0
    def S(g):
        return affinity.scale(g, K, K, origin=(0, 0))
    def B(x0, y0, x1, y1):
        return box(x0 * K, y0 * K, x1 * K, y1 * K)
    # pole, side rail, light windows
    a.add(B(286, 22, 334, 1300))
    a.add(Polygon([(282 * K, 22 * K), (338 * K, 8 * K), (338 * K, 26 * K), (282 * K, 34 * K)]))   # slanted cap
    a.add(B(268, 160, 281, 900))
    for y in (199, 303, 408, 513, 619, 725, 830, 934):
        a.cut(B(291, y, 317, y + 22))
    a.declare('redrawn', B(260, 0, 345, 1300), 'pole, cap, rail, light windows: constructed at their measured positions')
    # pillows (traced) as rings, letters (traced) in ink, brackets to the rail
    pil = S(mask_geom(WORK + '/r21/leons_pillows_co.png', smooth=SMOOTH['leons_pillows']))
    for p_ in getattr(pil, 'geoms', [pil]):
        a.add(ring(Polygon(p_.exterior), 26, inner_offset=-26))
    a.declare('redrawn', pil.envelope, 'LEONS pillows: outlines traced, then smoothed as the convex fittings they are')
    let = S(mask_geom(WORK + '/r21/leons_pletters_co.png', smooth=SMOOTH['leons_letters']))
    a.add(let)
    a.declare('exempt', let.envelope, 'LEONS letters: traced from the sign (R21)')
    for yb, xr in ((161, 225), (333, 221), (502, 220), (675, 219), (845, 219)):
        a.add(B(xr - 6, yb, 281, yb + 12))
    # STEAK / HOUSE boxes: ink, letters knocked out (fitted re-set, R21 reason c)
    a.add(B(333, 272, 770, 498))
    a.add(B(333, 530, 768, 752))
    a.add(B(318, 300, 334, 312)); a.add(B(318, 470, 334, 482)); a.add(B(318, 560, 334, 572)); a.add(B(318, 720, 334, 732))
    fit = []
    for word, xs, y0, y1 in (('STEAK', [(380, 430), (461, 516), (530, 582), (602, 665), (692, 740)], 302, 452),
                             ('HOUSE', [(370, 422), (452, 502), (527, 580), (607, 660), (687, 742)], 560, 710)):
        for ch, (x0, x1) in zip(word, xs):
            g, _ = T(ch, 'Antonio[wght].ttf', cap=(y1 - y0) * K, var=[300])
            g = affinity.scale(g, (x1 - x0) * K / width(g), 1, origin=(0, 0))
            g = move(g, x=x0 * K, bottom=y1 * K)
            a.cut(g)
            fit.append(g)
    a.declare('typeset', unary_union(fit).envelope, 'Antonio Light, each letter fitted to its measured box on the rectified sign (R21 reason c: trace broken by exposed neon)')
    # COFFEE SHOP shield (traced outline, smoothed) with the traced brush letters knocked out
    sh = S(mask_geom(WORK + '/r21/leons_shield_smooth.png', smooth=None))
    a.add(sh)
    a.declare('redrawn', sh, 'COFFEE SHOP shield: outline traced, debris on the top edge opened out, smoothed as the convex panel it is')
    cs = S(mask_geom(WORK + '/r21/leons_cs.png', smooth=SMOOTH['leons_cs']))
    a.cut(cs)
    a.declare('exempt', cs.envelope, 'COFFEE SHOP: brush letters traced from the sign (R21)')
    cap, _ = T('NORTH HOLLYWOOD  ·  1945', 'Jost[wght].ttf', cap=88, var=[600], track=0.16)
    cap = move(cap, cx=(68 + 770) / 2 * K, y=1300 * K + 120)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'red'
    return a


# ------------------------------------------------------------------ C32 Dutton's Books
def books_on_shelf(x0, y_shelf, w):
    """Our own simple drawing of the sign's centre motif: books between two bookends on a shelf."""
    H = w * 0.36
    specs = [(0.085, 0.70), (0.07, 0.86), (0.06, 0.78), (0.075, 0.95), (0.06, 0.82), (0.07, 0.74), (0.075, 0.88)]
    gap = 22.0
    total = sum(w * b for b, _ in specs) - gap
    r = w * 0.075
    be_h = H * 0.55
    cx = x0 + w / 2
    xs = cx - total / 2
    bk = []
    x = xs
    for bw_, bh_ in specs:
        bw, bh = w * bw_, H * bh_
        bk.append(box(x, y_shelf - bh, x + bw - gap, y_shelf))
        x += bw
    books = unary_union(bk)
    q = Point(0, 0).buffer(r, resolution=48).intersection(box(-r, -r, 0, 0))
    le = affinity.translate(q, xs - gap, y_shelf)
    le = affinity.scale(le, 1, be_h / r, origin=(xs - gap, y_shelf))
    re_ = affinity.scale(le, -1, 1, origin=(cx - gap / 2, 0))
    shelf = box(cx - total / 2 - r - 160, y_shelf, cx + total / 2 + r + 160 - gap, y_shelf + 34)
    g = unary_union([shelf, books, le, re_])
    cuts = []
    for b in bk:
        bb = b.bounds
        for yy in (H * 0.30, H * 0.20):
            cuts.append(box(bb[0] + 14, y_shelf - yy, bb[2] - 14, y_shelf - yy + 16))
    return g, unary_union(cuts)


@build
def duttons():
    """Dutton's Books, Laurel Canyon & Magnolia, North Hollywood (opened New Year's Day 1961 by Bill and
    Thelma Dutton; closed 2006). Source: Brad's VRM storefront photo (src/C32) - the rooftop sign
    'DUTTON'S BOOKS AND ART / New-Old & Rare / Bought & Sold' with books between bookends. Panel and books
    are our own drawing; headline in Kameron Bold (narrowed), side lines in Fredoka SemiBold, re-set from the
    photo (cap height there is under 150 px, so nothing is traced)."""
    a = Art('sfv_duttons_books')
    PW, PH = 3000.0, 1060.0
    panel = rrect(0, 0, PW, PH, 70)
    a.add(ring(panel, 30, inner_offset=-30))
    a.add(ring(panel, 12, inner_offset=-84))
    a.declare('redrawn', panel, 'sign panel + inner rule: constructed')
    h1, _ = T("DUTTON'S BOOKS", 'Kameron[wght].ttf', cap=200, var=[700], track=0.03)
    h2, _ = T('AND', 'Kameron[wght].ttf', cap=96, var=[700], track=0.06)
    h3, _ = T('ART', 'Kameron[wght].ttf', cap=200, var=[700], track=0.03)
    gap = 60
    total = width(h1) + gap + width(h2) + gap + width(h3)
    f = min(0.80, (PW - 300) / total)                  # narrow like the sign's condensed letters, fit the panel
    h1, h2, h3 = hscale(h1, f), hscale(h2, f), hscale(h3, f)
    gap *= f
    total = width(h1) + gap + width(h2) + gap + width(h3)
    x0 = (PW - total) / 2
    base = 170 + 200
    h1 = move(h1, x=x0, bottom=base); h2 = move(h2, x=h1.bounds[2] + gap, bottom=base - 56); h3 = move(h3, x=h2.bounds[2] + gap, bottom=base)
    for g in (h1, h2, h3):
        a.add(g, 'typeset', f'Kameron Bold (x{f:.2f}); R21 reason a: sign letters ~10-12 px cap in the photo')
    a.declare('exempt', unary_union([h2, h3]), 'LEVEL only: the small AND sits raised before ART as on the sign (the gate reads a line through their counters)')
    sl = []
    for txt, cx, y in (('New-Old', 520, 560), ('& Rare', 520, 760), ('Bought', 2480, 560), ('& Sold', 2480, 760)):
        g, _ = T(txt, 'Fredoka[wdth,wght].ttf', cap=118, var=[600, 100], track=0.03)
        g = move(g, cx=cx, y=y)
        a.add(g, 'typeset', 'Fredoka SemiBold; R21 reason a: ~6 px cap in the photo')
    books, cuts = books_on_shelf(PW / 2 - 560, 900, 1120)
    a.add(books)
    a.cut(cuts)
    a.declare('redrawn', books.buffer(10), 'books + bookends: our own drawing of the sign motif')
    cap, _ = T('NORTH HOLLYWOOD  ·  1961', 'Jost[wght].ttf', cap=92, var=[600], track=0.16)
    cap = move(cap, cx=PW / 2, y=PH + 140)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'green'
    return a


# ------------------------------------------------------------------ C20 FM Station
FM_STROKES = [   # brush-stroke control points (x, y) + widths, measured on the x4 upscale of Brad's crop
    ([(220, 140), (370, 113), (520, 85)], [58, 48, 28]),     # F top bar
    ([(355, 135), (318, 262), (258, 405)], [54, 44, 24]),    # F stem
    ([(272, 272), (410, 244)], [48, 28]),                    # F middle bar
    ([(405, 412), (455, 270), (503, 138)], [28, 50, 62]),    # M left leg
    ([(503, 138), (546, 296)], [62, 40]),                    # M down to the valley
    ([(546, 296), (615, 205), (684, 120)], [38, 76, 60]),    # M up to the right peak
    ([(694, 118), (680, 262), (650, 405)], [62, 50, 26]),    # M right leg
]


@build
def fm_station():
    """FM Station, North Hollywood (opened 1976; the Valley's hard-rock club: Poison, Warrant, Metallica,
    Great White played it). Source: VRM's Sept 2026 post of the rooftop box sign (src/C20 = Brad's pull s2140-13).
    The brushed FM is traced from a x4 Real-ESRGAN upscale of the pull (R21; ~55 px cap): flecks filled, the wire
    across the M's right leg and the peeled patch removed. Pass 3 (Brad 10-28): the marquee board under it is drawn
    as in the photo, measured on the pull: board, top beam, frame, the three posts and the V brace, and the FM box
    sitting right of the board's centre as it does on the roof. The marquee's own lines are band names (live marks)
    and the photo is AI-smeared there (unreadable: R21 reason a), so it reads NORTH HOLLYWOOD only, in squared
    changeable-marquee letters (Big Shoulders Display ExtraBold, the open face closest to Wagner-style letters),
    hung one by one on the tracks with small tilts and uneven gaps, as such signs are. Units: x4-crop px of the
    fm2 crop (native = 291 + U/4, 272 + U/4), x2.15."""
    import random
    a = Art('sfv_fm_station')
    f = 2.15
    def S(g):
        return affinity.scale(g, f, f, origin=(0, 0))
    def B(x0, y0, x1, y1):
        return S(box(x0, y0, x1, y1))
    fm = S(mask_geom(WORK + '/r21/fm_letters.png', smooth=SMOOTH['fm']))
    bx = S(Polygon([(100, 45), (860, 45), (860, 68), (935, 68), (935, 470), (860, 470), (860, 490), (100, 490),
                    (100, 470), (25, 470), (25, 80), (100, 80)]))
    a.add(bx)
    a.cut(fm)
    a.declare('exempt', fm.buffer(20), 'hand-brushed FM: traced from the sign (R21)')
    # posts (native x 345-352, 467-475, 498-515; y 394-427) and the V brace between the first two
    for x0, x1 in ((216, 244), (704, 736), (828, 896)):
        a.add(B(x0, 486, x1, 626))
    a.add(S(stroke_line([(240, 564), (464, 618), (708, 548)], 12)))   # shallow V brace, measured (native 352,413 / 407,426 / 468,409)
    # marquee board (native x 121-558, y 427-588): outer edge, top beam, frame
    X0, X1, Y0, Y1 = -680.0, 1068.0, 620.0, 1264.0
    board = B(X0, Y0, X1, Y1)
    a.add(board)
    a.cut(S(ring(box(X0, Y0, X1, Y1).buffer(-18, join_style=2), 14, inner_offset=0)))
    a.cut(B(X0 + 32, 672, X1 - 32, 686))                                 # under the top beam
    a.declare('redrawn', board.union(B(200, 480, 900, 630)), 'marquee board, beam, frame, posts and brace: constructed at the photo measurements')
    # tracks + hung letters: the beam line is the top rail; one rail between the rows, one under
    face_l, face_r = X0 + 40, X1 - 40
    cx = (face_l + face_r) / 2
    cap = 190.0
    tops = (728.0, 988.0)
    for yr in (tops[0] + cap + 32, tops[1] + cap + 30):
        a.cut(B(face_l, yr, face_r, yr + 8))
    rnd = random.Random(1976)
    for word, top in zip(('NORTH', 'HOLLYWOOD'), tops):
        glyphs = []
        for ch in word:
            g, _ = T(ch, 'BigShouldersDisplay[wght].ttf', cap=cap, var=[800])
            glyphs.append(hscale(g, 1.32 if ch == 'W' else 1.08))      # marquee W tiles run wide
        gaps = [cap * 0.15 * (1 + rnd.uniform(-0.45, 0.45)) for _ in glyphs[1:]]
        total = sum(width(g) for g in glyphs) + sum(gaps)
        x = cx - total / 2
        placed = []
        for n, g in enumerate(glyphs):
            w0 = width(g)
            g = move(g, x=x, bottom=top + cap + rnd.uniform(-4, 4))
            placed.append(affinity.rotate(g, rnd.uniform(-1.2, 1.2), origin='centroid'))
            x += w0 + (gaps[n] if n < len(gaps) else 0)
        row = S(unary_union(placed))
        a.cut(row)
        a.declare('typeset', row.envelope, 'Big Shoulders Display ExtraBold, marquee letters hung one by one; R21 reason a: the marquee letters are AI-smeared in the only photo')
        a.declare('exempt', row.envelope.buffer(12), 'LEVEL only: marquee letters hung by hand on the tracks; the small per-letter tilts and uneven gaps are the sign (Brad 10-28)')
    return a


# ------------------------------------------------------------------ C30 Weber's Place
@build
def webers():
    """Weber's Place, 19312 Vanowen St, Reseda (dive bar with live music and punk shows). Source: Brad's pull
    s2150-22 (VRM's May 2026 photo of the sign, now at VRM; src/C30), x4 Real-ESRGAN.
    Pass 3 (Brad 10-28, L46): the photo is squared up first: a homography on the PLACE box (a true rectangle on
    the sign's plane; 4 % keystone) puts every element in one frame (sfv2/work/r21/webers_rect.png). The orange
    swash W is traced from its face there, with the glossy glare on its middle stroke counted as face and the
    orange wedge at the top of the middle (cut off from the rest by that glare) kept: pass 2 lost both. 'eber's'
    is now traced too: its faces separate cleanly from their side walls, and Bookman Bold Italic set at its own
    spacing is 19 % wider than the sign's word at the sign's height, so it is not an exact face (R21 rule 3b).
    PLACE is traced from the box.
    Oval panel and PLACE box constructed at the measured outline. Built in rectified px."""
    a = Art('sfv_webers_place')
    cx, cy, rx, ry = 2046.0, 894.0, 1609.0, 612.0           # ellipse fit to 18 panel-edge points read on the squared photo
    ov = affinity.translate(affinity.scale(Point(0, 0).buffer(1, resolution=160), rx, ry), cx, cy)
    rules = unary_union([ring(ov, 34, inner_offset=-34), ring(ov, 16, inner_offset=-96)])
    W = mask_geom(WORK + '/r21/web_W_rect.png', smooth=SMOOTH['web_W'])
    a.declare('exempt', W.envelope, "the orange swash W: traced from the sign's face in the squared-up frame (R21, L46)")
    e = mask_geom(WORK + '/r21/web_eber_faces_co.png', smooth=SMOOTH['web_eber'])
    a.declare('exempt', e.envelope, "eber's: the sign's letter faces traced in the squared-up frame (R21; Bookman set at its own spacing is 19 % wider than the sign's word, so it is not an exact match)")
    e = e.difference(W.buffer(14))
    pb = box(1566, 1150, 2450, 1360)
    rules = rules.difference(unary_union([W.buffer(60), e.buffer(60), pb.buffer(60, join_style=2)]))
    rules = rules.buffer(-7, join_style=2).buffer(7, join_style=2)
    rules = unary_union([p_ for p_ in getattr(rules, 'geoms', [rules]) if p_.area > 4000])
    a.add(rules)
    a.add(W)
    a.add(e)
    a.add(pb)
    pl = mask_geom(WORK + '/r21/web_place_rect.png', smooth=SMOOTH['web_place'])
    a.cut(pl)
    a.declare('exempt', pl.envelope, 'PLACE: traced from the sign box in the squared-up frame (R21)')
    a.declare('redrawn', ov, 'oval panel rim + PLACE box: constructed at the measured outline')
    cap, _ = T('19312 VANOWEN ST.  ·  RESEDA', 'Jost[wght].ttf', cap=92, var=[600], track=0.16)
    cap = move(cap, cx=cx, y=cy + ry + 120)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    return a


# ------------------------------------------------------------------ C27 Moby Disc


def mask_geom(path, smooth=3, alphamax=1.0, min_area=60):
    import numpy as np
    from PIL import Image
    m = np.array(Image.open(path).convert('L')) > 127
    return trace_geom(m, alphamax=alphamax, smooth_sigma=smooth)


@build
def moby_disc():
    """Moby Disc Records (14410 Ventura Blvd, Sherman Oaks; 6553 Topanga Canyon Blvd, Canoga Park; early
    1970s-2001). Source: the store's inner record sleeve, Flickr 5379507456 original 2520 px (src/C27), x4
    Real-ESRGAN. R21 pass 2: everything on the sleeve is traced, lettering included: the MOBY DISC RECORDS arc
    (~160 px cap in the source) and "A Whale of a Store!" with its hand-drawn underlines; whale, record, waves,
    splash as before. Cleanup inside the source shapes only (specks, ink dropouts). Locator line = house type."""
    a = Art('sfv_moby_disc')
    illu = mask_geom(WORK + '/moby_illu.png', smooth=None)     # smoothing lost the record-label ring (part B)
    a.add(illu)
    a.declare('exempt', illu.buffer(10).envelope, 'illustration: whale, record, waves, splash traced from the sleeve (cleaned)')
    arch = mask_geom(WORK + '/moby_arch.png', smooth=3)
    a.add(arch)
    a.declare('exempt', arch.envelope, 'hand lettering traced from the sleeve: MOBY DISC RECORDS on its arc (R21)')
    tag = mask_geom(WORK + '/moby_tag_trace.png', smooth=3)
    a.add(tag)
    a.declare('exempt', tag.envelope, 'hand lettering traced from the sleeve: A Whale of a Store! with its underlines (R21)')
    cx = 415 * 4
    cap, _ = T('SHERMAN OAKS  ·  CANOGA PARK', 'Jost[wght].ttf', cap=90, var=[600], track=0.16)
    cap = move(cap, cx=cx, y=4630)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'navy'
    a.clean = True
    return a


# ------------------------------------------------------------------ C46 The Jolly Roger
SRC = '/home/claude/sfv2/src'


@build
def jolly_roger():
    """The Jolly Roger restaurant (Sherman Oaks Fashion Square on Riverside Dr; also Canoga Park and Northridge;
    1960s-80s). Source: the 1970s menu cover, VRM archive item 566 (Gorsky Menu Collection), 3000 px scan
    (src/C46). One-colour version of the linocut: the menu's black block, traced at full resolution and
    print-cleaned at its final size (S9 floors). The hand-cut 'The Jolly Roger' lettering stays hand lettering
    (traced, exempt); the menu's (R) and its corner code letter are removed. Ink: charcoal on Vintage White,
    the paper standing in for the menu's cream."""
    import numpy as np
    from PIL import Image
    from scipy import ndimage as nd
    im = np.array(Image.open(SRC + '/C46/jolly_roger_menu_1970s_VRM_archive_566.jpg').convert('RGB')).astype(int)
    crop = im[440:2760, 640:2410]
    m = crop.max(axis=2) < 80
    m[2230:, :120] = False                         # menu code letter 'L', bottom-left corner
    # the (R) after 'Roger': small ring right of the word, top of the cover
    lab, n = nd.label(m)
    for i, sl in enumerate(nd.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if 430 < sl[0].start < 560 and sl[1].start > 1240 and h < 40 and w < 40:
            m[lab == i] = False
    target_w = 2850
    f = target_w / m.shape[1]
    big = np.array(Image.fromarray((m * 255).astype(np.uint8)).resize((target_w, int(m.shape[0] * f)), Image.LANCZOS)) > 127
    big = print_clean(big, 300)
    a = Art('sfv_jolly_roger')
    g = trace_geom(big, alphamax=1.0)
    a.add(g)
    a.declare('exempt', g.envelope, "illustration + hand-cut lettering: the menu's linocut, traced from the 3000 px scan and print-cleaned")
    cap, _ = T('SHERMAN OAKS  ·  CANOGA PARK', 'Jost[wght].ttf', cap=100, var=[600], track=0.16)
    cap = move(cap, cx=target_w / 2, y=g.bounds[3] + 110)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'charcoal'
    a.clean = dict(hair_in=0.027)
    return a


# ------------------------------------------------------------------ C07 Devonshire Downs
@build
def devonshire_downs():
    """Devonshire Downs, 18000 Devonshire St, Northridge (harness track 1946; SFV Fair grounds; San Fernando
    Valley State College from the 1960s; Newport '69; razed 2001). Source: the 1960-65 rental flyer, CSUN
    Special Collections scan 1553 x 2083 (src/C07; same image as VRM's post). Our own drawing of the
    pediment sign (tapered panel, cornice, finial, display case, posts). R21 pass 2: 'Devonshire Downs' (~55 px cap)
    is traced from a x4 upscale of the scan (was Libre Caslon); the white script line is re-set in Sacramento (R21
    reason c, see below; was Damion)."""
    a = Art('sfv_devonshire_downs')
    k = 3.0
    def P(pts):
        return Polygon([(x * k, y * k) for x, y in pts])
    lw = 14 * 1.0
    panel = P([(285, 126), (744, 126), (690, 509), (340, 509)])   # corners re-measured on the flyer (R21 pass)
    a.add(ring(panel, lw * 1.4, inner_offset=-lw * 1.4))           # thin edge, as painted (v1's 0.15 in frame crowded the lettering)
    # pediment: cornice band rising to the finial
    ped_out = P([(258, 118), (521, 42), (782, 118), (770, 130), (521, 57), (271, 130)])   # cornice band, measured
    a.add(ped_out)
    a.add(Point(521 * k, 30 * k).buffer(19 * k, resolution=64))
    a.cut(Point(516 * k, 25 * k).buffer(6 * k, resolution=32))            # highlight on the ball
    # display case
    case = box(380 * k, 272 * k, 635 * k, 486 * k)
    a.add(ring(case, 8 * k, inner_offset=0))
    a.add(ring(case.buffer(-14 * k, join_style=2), 4 * k, inner_offset=0))
    a.add(Point(392 * k, 302 * k).buffer(5 * k))                          # latch
    # glass glints
    for x0, y0, x1, y1 in ((430, 320, 470, 280 + 20), (455, 380, 545, 300), (500, 440, 600, 340)):
        a.add(stroke_line([(x0 * k, y0 * k), (x1 * k, y1 * k)], 4.5 * k).intersection(case.buffer(-20 * k)))
    # base moulding + posts
    a.add(box(330 * k, 505 * k, 695 * k, 524 * k))
    for px in (410, 614):
        a.add(box((px - 12) * k, 524 * k, (px + 12) * k, 610 * k))
    a.declare('redrawn', box(250 * k, 20 * k, 780 * k, 612 * k), 'sign: our own drawing after the flyer illustration')
    # R21: the flyer's own lettering, traced. Frame: this drawing's units = flyer px - (242, 43) (checked on the panel
    # corners); the x4 upscales map back with /4 + their crop origin.
    def from_x4(path, ox, oy, sm):
        g = mask_geom(path, smooth=sm)
        g = affinity.scale(g, 0.25, 0.25, origin=(0, 0))
        g = affinity.translate(g, ox - 242, oy - 43)
        return affinity.scale(g, k, k, origin=(0, 0))
    t = from_x4(WORK + '/r21/devon_letters_co.png', 0.05 * 1553, 0.02 * 2083, SMOOTH['devon'])
    a.add(t)
    a.declare('exempt', t.envelope, "'Devonshire Downs': the flyer's hand-painted lettering, traced (R21)")
    # The flyer's white script line is a hairline monoline script (~4 % stroke) over the shrubs and stair stripes:
    # traced, the second line breaks up on the stripes and the strokes sit under the print floor (R21 reason c, tried
    # 10-28: sfv2/work/r21/devon_script_raw*.png). Re-set in Sacramento, the closest OFL match (upright monoline
    # with the same looped capitals), weighted up to the 0.03 in line floor; same words, two lines as on the flyer.
    l1, _ = T("The San Fernando Valley's only complete", 'Sacramento-Regular.ttf', cap=44 * k)
    l2, _ = T('fair grounds and exhibit facility!', 'Sacramento-Regular.ttf', cap=44 * k)
    l1 = l1.buffer(1.2, join_style=1); l2 = l2.buffer(1.2, join_style=1)
    # the script's pinhole loops at crossing joins sit under the counter floor at this size: filled (floor fix, L44)
    def _fill_pin(g, amin=(0.035 * 300) ** 2):
        return unary_union([Polygon(p_.exterior, [h for h in p_.interiors if Polygon(h).area >= amin]) for p_ in getattr(g, 'geoms', [g])])
    l1, l2 = _fill_pin(l1), _fill_pin(l2)
    l1 = move(l1, cx=470 * k, y=636 * k)
    l2 = move(l2, x=l1.bounds[0] + (l1.bounds[2] - l1.bounds[0]) * 0.36, y=l1.bounds[3] + 14 * k)
    a.add(l1, 'typeset', 'Sacramento, weighted to the line floor; R21 reason c: hairline script broken by the stair stripes')
    a.add(l2, 'typeset', 'Sacramento, weighted to the line floor; R21 reason c: hairline script broken by the stair stripes')
    a.declare('exempt', unary_union([l1, l2]).envelope, 'LEVEL only: a looped monoline script whose letters ride the baseline unevenly by design (set level from the font)')
    s2 = l2
    cap, _ = T('18000 DEVONSHIRE ST.  ·  NORTHRIDGE', 'Jost[wght].ttf', cap=24 * k, var=[600], track=0.16)
    cap = move(cap, cx=512 * k, y=s2.bounds[3] + 50 * k)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'red'
    a.clean = True                       # S9 floors on the traced painted lettering and the script loops
    return a


# ------------------------------------------------------------------ C40 Fantasy Faire 1967
@build
def fantasy_faire():
    """Fantasy Faire and Magic Music Festival, July 15-16 1967, at Devonshire Downs ('Devonshire Meadows' on
    the poster), Northridge. Source: the 1967 poster (The Gates of Eden; Circle Printing, LA), PAE lot 13574,
    1999 x 2804 (src/C40). The credit line reads 'Poster design -- The Gates of Eden, Penny Havard - 1967' with no
    copyright symbol or word, so the poster was published without notice (1909 Act): public domain, art included.
    Pass 3 (Brad 10-28, L49): the gap between the title and the festival lines is filled with the poster's own centre
    figure, the Mucha-style woman with the rose and her burst of stars, traced from the red plate (x4 Real-ESRGAN,
    then cut out by a drawn boundary). Every element sits at its printed position on the poster (the lettering
    masks are 1:1 crops; offsets measured by template match). Left out: the two winged figures (bare-chested, which
    Meta's ad rules reject), the laurel fronds they hold, the band list (live marks), times and credits.
    The figure's hairlines are lifted to the DTG line floor along their own centrelines (print-clean)."""
    a = Art('sfv_fantasy_faire_1967')
    sc = 1.9
    for name, (px, py) in (('A', (224, 192)), ('B', (208, 1704)), ('C', (212, 2120))):
        g = mask_geom(WORK + f'/ff_{name}.png', smooth=None)
        g = affinity.scale(affinity.translate(g, px, py), sc, sc, origin=(0, 0))
        a.add(g)
        a.declare('exempt', g.envelope, 'hand lettering from the 1967 poster: traced from the red plate, lightly cleaned')
    fig = mask_geom(WORK + '/r21/ff_figure_floor.png', smooth=None)   # hairlines lifted to 0.021 in on their own centrelines (floor, L27; Hub City's 1.5 pt)
    fig = affinity.scale(fig, 0.25, 0.25, origin=(0, 0))                  # x4 crop -> poster px
    fig = affinity.scale(affinity.translate(fig, 600, 540), sc, sc, origin=(0, 0))
    a.add(fig)
    a.declare('exempt', fig.envelope, "illustration: the poster's centre figure with the rose and stars, traced from the red plate (pass 3)")
    a.ink = 'red'
    a.clean = dict(hair_in=0.021)
    return a


# ------------------------------------------------------------------ C42 Rusty's Hacienda
@build
def rustys():
    """Rusty's Hacienda, 6439 Lankershim Blvd near Victory, North Hollywood (Mexican family restaurant; also
    Glendale, El Monte, Los Angeles; c.1965-1970s). R21 pass 2: rebuilt from the ad Brad pulled (Valley News,
    June 30 1972, VRM post s2159-50), x4 Real-ESRGAN of the whole ad and traced as printed, the Hattiesburg-ad way
    (SR + threshold, no smoothing; print-clean floors only): the RUSTY'S HACIENDA headline with its zigzag inline,
    Family Restaurants, the MEXICAN FOOD sombrero, Cocktail Lounge / Banquets / Food to Go / Entertainment, and the
    ad's own address block (No. Hollywood Hacienda / 6439 Lankershim Blvd. / (near Victory)), which is the place
    line, so no house line is added. Left out: the phone number (standing rule) and the other-locations block;
    (near Victory) is re-centred where the phone was cut (L21). The sombrero's mustache is kept (Brad 10-28: it is
    the ad's own art; pass 2 had cut it on a caricature caution that was HQ's, not his, L48). v1's menu-based
    Knewave re-set is retired."""
    a = Art('sfv_rustys_hacienda')
    g = mask_geom(WORK + '/r21/rusty_keep_final.png', smooth=None)
    a.add(g)
    a.declare('exempt', g.envelope, "the 1972 ad traced as printed (hand-lettered headline, sombrero, the ad's own type) - R21")
    a.ink = 'red'
    a.clean = True
    return a


# ------------------------------------------------------------------ C25 Don's (Burbank)
@build
def dons():
    """Don's Restaurant & Coffee Shop, 509 S. Glenoaks Blvd, Burbank (Don Draper's drive-in from 1947;
    closed 2002; one panel of the neon sign is at VRM, the other at the Gordon R. Howard Museum). Source:
    the menu cover in VRM's Aug 2026 post (src/C25 + Brad's screenshot): the brush 'Don's' with the chef in
    the D, traced from a x4 Real-ESRGAN upscale and cleaned (hand lettering + illustration: exempt);
    R21 pass 2: RESTAURANT AND COFFEE SHOP traced from the same pull (was Oswald); the address in Jost (house
    locator line); no phone number."""
    a = Art('sfv_dons')
    logo = mask_geom(WORK + '/dons_clean.png', smooth=None)     # smoothing erased the eyes/smile (part B): raw potrace curves
    logo = affinity.scale(logo, 1.9, 1.9, origin=(0, 0))
    lb = logo.bounds
    a.add(logo)
    a.declare('exempt', logo.envelope, "hand lettering + chef illustration from the menu cover (traced, cleaned)")
    # R21: RESTAURANT / AND / COFFEE SHOP are the menu's own hand-drawn condensed letters (~21 px cap in Brad's
    # pull, a clean print photo): traced from the x4 upscale of the same pull, kept in the menu's own layout.
    # Registration: that upscale and dons_clean share scale (logo width 1394 px in both); offset (-120, +136).
    lines = mask_geom(WORK + '/r21/dons_lines.png', smooth=SMOOTH['dons_lines'])
    lines = affinity.scale(affinity.translate(lines, -120, 136), 1.9, 1.9, origin=(0, 0))
    a.add(lines)
    a.declare('exempt', lines.envelope, "hand lettering from the menu cover: RESTAURANT AND COFFEE SHOP (traced, R21)")
    cx = (lines.bounds[0] + lines.bounds[2]) / 2
    # the menu's own address line, in its own words (no phone): ~8 px cap in the pull, so re-set (R21 reason a)
    ad, _ = T('509 SO. GLENOAKS BLVD.  ·  BURBANK, CALIFORNIA', 'Jost[wght].ttf', cap=96, var=[600], track=0.08)
    ad = scale_to(ad, w=2560) if width(ad) > 2560 else ad      # big enough that the periods clear the print-clean speck floor
    ad = move(ad, cx=cx, y=lines.bounds[3] + 150)
    a.add(ad, 'typeset', 'Jost SemiBold (the menu address line, its own words, re-set); R21 reason a: ~8 px cap in the pull')
    a.ink = 'charcoal'
    a.clean = True
    return a


# ------------------------------------------------------------------ C18 Sasch
@build
def sasch():
    """Sasch, 11345 Ventura Blvd, Studio City ('L.A.'s most sophisticated nightclub', 1980s). Source: the
    matchbook in VRM's posts (Sept 2026 + Feb 2022; Brad pulled it twice = emphasis; src/C18). The brush
    'Sasch' is traced from a x4 Real-ESRGAN upscale (hand lettering, exempt; its deliberate rising angle is
    kept); the matchbook's keyline is rebuilt as a true offset; the tagline (rotated on the script's angle)
    and the address are re-set in TeX Gyre Heros (Helvetica, as printed). No phone number."""
    a = Art('sfv_sasch')
    sc = 3.5
    g = mask_geom(WORK + '/sasch_letters.png', smooth=None)
    g = affinity.scale(g, sc, sc, origin=(0, 0))
    a.add(g)
    a.declare('exempt', g.envelope, 'hand lettering from the matchbook (traced); the word rises ~15 deg by design')
    kl = ring(g.buffer(18, join_style=1), 13, inner_offset=0)
    kl = kl.buffer(-5, join_style=1).buffer(5, join_style=1)
    a.add(kl)
    a.declare('redrawn', kl.envelope, 'keyline: true offset of the traced letters (rebuilt, not traced)')
    gb = g.bounds
    ang = -15.0
    tg, _ = T("LA'S MOST SOPHISTICATED NIGHTCLUB", 'texgyreheros-regular.otf', cap=68, track=0.02)
    cxy = (gb[0] + (gb[2] - gb[0]) * 0.55, gb[3] - (gb[3] - gb[1]) * 0.18)
    tg = move(tg, cx=cxy[0], cy=cxy[1] + 95)
    tg = affinity.rotate(tg, ang, origin=cxy)
    a.cut(tg.buffer(22))
    a.add(tg, 'typeset', 'TeX Gyre Heros (rotated on the script angle); R21 reasons a+b: ~5 px cap, Helvetica as printed')
    a.declare('exempt', tg.envelope, "LEVEL only: the tagline runs on the matchbook's 15-deg script angle")
    ad1, _ = T('11345 Ventura Boulevard', 'texgyreheros-regular.otf', cap=120, track=0.01)
    ad2, _ = T('Studio City', 'texgyreheros-regular.otf', cap=120, track=0.01)
    cx = (gb[0] + gb[2]) / 2
    ad1 = move(ad1, cx=cx, y=max(gb[3], tg.bounds[3]) + 200)
    ad2 = move(ad2, cx=cx, y=ad1.bounds[3] + 70)
    a.add(ad1, 'typeset', 'TeX Gyre Heros; R21 reasons a+b: ~11 px cap, Helvetica as printed')
    a.add(ad2, 'typeset', 'TeX Gyre Heros; R21 reasons a+b: ~11 px cap, Helvetica as printed')
    a.ink = 'gold'
    a.clean = True
    return a


# ------------------------------------------------------------------ C37 Encino Bowl
def hhex(cx, cy, w, h, tip):
    """Horizontal elongated hexagon (pointed left/right)."""
    x0, x1 = cx - w / 2, cx + w / 2
    return Polygon([(x0, cy), (x0 + tip, cy - h / 2), (x1 - tip, cy - h / 2), (x1, cy), (x1 - tip, cy + h / 2), (x0 + tip, cy + h / 2)])


@build
def encino_bowl():
    """Encino Bowl & Coffee Shop, 15945 Ventura Blvd, Encino (1962 - May 1986; co-owners Irv Miro and Harry
    Grant; birthday parties, arcade, a nursery inside). Source: Brad's pull s2157-59 (VRM Apr 2026 post), x4
    Real-ESRGAN of the whole sign, the BOWL plane rectified on the B and L stems, then a 1-D projective spacing
    correction so the four boxes come out equal (sfv2/work/r21/enc_bowl_rect_w.png). R21 pass 2, traced: the BOWL
    wedge-serif letters (~78 px cap in the pull; glare on B and O recovered by hue), ENCINO (~22 px; the C's broken
    lower jaw rebuilt as the mirror of its intact upper jaw), and Coffee Shop (each word levelled and de-sheared on
    its own half of the two-faced oval, Shop scaled to Coffee's cap height). Constructed at measured positions: the
    four pointy-top hexagon boxes (v1 drew them pointing sideways: wrong), the ENCINO box, posts, poles, the oval.
    The EB drum monogram is too small and curved to trace (R21 reason a): E and B re-set in Michroma (the squared
    extended sans of the ENCINO letters). Built in corrected-rectified px x K."""
    a = Art('sfv_encino_bowl')
    K = 1.4
    def S(g):
        return affinity.scale(g, K, K, origin=(0, 0))
    def B(x0, y0, x1, y1):
        return box(x0 * K, y0 * K, x1 * K, y1 * K)
    # four pointy-top hexagon boxes, seams between them
    xs = [270 + 540 * k for k in range(5)]
    hexes = [Polygon([(xs[k] * K, 375 * K), ((xs[k] + 270) * K, 322 * K), (xs[k + 1] * K, 375 * K),
                      (xs[k + 1] * K, 718 * K), ((xs[k] + 270) * K, 776 * K), (xs[k] * K, 718 * K)]) for k in range(4)]
    row = unary_union(hexes)
    a.add(row)
    for x in xs[1:4]:
        a.cut(B(x - 4, 380, x + 4, 713))
    a.declare('redrawn', row, 'BOWL boxes: four pointy-top hexagons at the measured outline (regularised to equal width)')
    bowl = S(mask_geom(WORK + '/r21/enc_bowl_letters_w.png', smooth=SMOOTH['enc_bowl']))
    # L47: the traced row still rose 1.05 deg left to right after the BOWL-plane rectification (tops and feet both
    # climb ~40 px B->L against the level boxes): graduated capture drift (L39), levelled as one unit.
    bowl = affinity.rotate(bowl, 1.05, origin=bowl.centroid)
    a.cut(bowl)
    a.declare('exempt', bowl.envelope, 'BOWL: the sign letters traced (R21)')
    # ENCINO box + its dark lower body, letters knocked out
    a.add(B(801, 58, 1867, 236))          # the white face only: the box's dark lower body is garment (one ink)
    enc = S(mask_geom(WORK + '/r21/enc_encino_letters_fix_w.png', smooth=SMOOTH['enc_encino']))
    a.cut(enc)
    a.declare('exempt', enc.envelope, 'ENCINO: the sign letters traced (R21); broken C jaw mirrored from its upper jaw')
    a.declare('redrawn', B(801, 58, 1867, 236), 'ENCINO box face: constructed at the measured outline')
    # posts + drum with the EB monogram
    cx = (801 + 1867) / 2
    for px in (cx - 245, cx + 245):
        a.add(B(px - 22, -150, px + 22, 62))
    dc = (cx * K, -240 * K)
    drum = affinity.translate(affinity.scale(Point(0, 0).buffer(1, resolution=96), 230 * K, 120 * K), *dc)
    a.add(drum)
    a.cut(ring(drum, 9 * K, inner_offset=-22 * K))
    e1, _ = T('E', 'Michroma-Regular.ttf', cap=118 * K)
    b1, _ = T('B', 'Michroma-Regular.ttf', cap=118 * K)
    e1 = move(e1, right=dc[0] + 4, cy=dc[1]); b1 = move(b1, x=dc[0] - 4, cy=dc[1])
    a.cut(unary_union([e1, b1]), 'typeset', 'Michroma (EB drum monogram, R21 reason a)')
    a.declare('redrawn', drum, 'EB drum: constructed')
    # Coffee Shop sign (pass 3, Brad 10-28, L47): the two-faced lozenge rectified face by face: the vertical
    # vanishing point from the BOWL stems (the seam and the f stems run to it: the script is upright) and each
    # face's horizontal vanishing point fitted so its top and bottom edges mirror (sfv2/work/r21/enc_sym.py;
    # rectified faces enc_rect_L3.0.png, length = 3 x seam height). Letters traced there at mid-tone thresholds
    # (pass 2's dark-core threshold thinned the brush strokes). The outline is the right face's measured profile,
    # mirrored (the sign is symmetric; the left tip is lost in rim glare). Placed as in the photo: 56 % of the
    # BOWL row wide, centred under its right half, hung on a short post; the main pole is the thick one to its left.
    import json as _json
    lz = _json.load(open(WORK + '/r21/enc_lozenge.json'))
    kk = 1210.0 / (2 * lz['x'][-1])                         # rectified px -> build units
    OX, OY = 1931.0, 1172.0                                  # oval centre (build units)
    xs_, hs_ = lz['x'], lz['h']
    upper = [(OX + x * kk, OY - h * kk) for x, h in zip(xs_, hs_)]
    lower = [(OX + x * kk, OY + h * kk) for x, h in zip(xs_, hs_)][::-1]
    right = upper + lower
    left = [(2 * OX - x, y) for x, y in right][::-1]
    face = S(Polygon(right).union(Polygon(left)).buffer(0))
    a.add(B(1052, 718, 1179, 1430))                          # main pole (photo x 870-1000), runs on past the sign
    a.add(B(1612, 712, 1732, OY - hs_[0] * kk + 20))         # short post the sign hangs from (photo x 1440-1580)
    rim = face.buffer(16 * K, join_style=1)
    a.add(rim)
    a.cut(ring(rim, 8 * K, inner_offset=-8 * K))            # dark trim line at the face edge (0.037 in), outer band 0.036 in
    a.cut(B(OX - 4, OY - hs_[0] * kk + 8, OX + 4, OY + hs_[0] * kk - 8))      # the seam where the two faces meet
    a.declare('redrawn', face.buffer(12 * K), 'Coffee Shop lozenge: measured right-face profile, mirrored; trim and seam constructed')
    def place(path, sm):
        g = mask_geom(path, smooth=sm)
        g = affinity.translate(g, -lz['cx'], -lz['cy'])
        g = affinity.scale(g, kk, kk, origin=(0, 0))
        return S(affinity.translate(g, OX, OY))
    cs = unary_union([place(WORK + '/r21/enc_coffee_rect.png', SMOOTH['enc_cs']),
                      place(WORK + '/r21/enc_shop_rect.png', SMOOTH['enc_cs'])])
    a.cut(cs)
    a.declare('exempt', cs.envelope, 'Coffee Shop: the sign lettering traced from the per-face rectified photo (R21, L47)')
    cap, _ = T('15945 VENTURA BLVD.  ·  ENCINO', 'Jost[wght].ttf', cap=95, var=[600], track=0.16)
    cap = move(cap, cx=1350 * K, y=1430 * K + 90)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    return a


# ------------------------------------------------------------------ C35 Mike's Pizza
@build
def mikes_pizza():
    """Mike's Pizza, 8160 Van Nuys Blvd, Panorama City (closed 1993; 'Serving since 1954'). Source: the menu
    cover in VRM's Sept 2026 post (1.3K/304/76; src/C35 + Brad's screenshot). The chef and the 'Mike's' script
    are traced from a x4 Real-ESRGAN upscale (illustration + hand lettering, exempt), one colour: the menu's
    black and red plates together, the yellow and white left as garment. A napkin occludes the right edge of
    the cover; it was cut along its own edge and nothing of the chef was redrawn (checked at print zoom).
    R21 pass 2: PIZZA is now traced from the same upscale (~55 px cap in the menu photo), in its place beside the
    script; SERVING SINCE 1954 stays re-set in Jost Bold (about 7 px in the source: R21 reason a). VRM sells a
    different redraw of this chef (their own layout): ours is the menu cover's layout."""
    a = Art('sfv_mikes_pizza')
    sc = 1.55
    chef = affinity.scale(mask_geom(WORK + '/mike_chef.png', smooth=None), sc, sc, origin=(0, 0))
    scr = affinity.scale(mask_geom(WORK + '/mike_script.png', smooth=None), sc, sc, origin=(0, 0))
    a.add(chef)
    a.declare('exempt', chef.envelope, 'illustration: the menu chef (traced, one-colour)')
    a.add(scr)
    a.declare('exempt', scr.envelope, "hand lettering: the menu's 'Mike's' script (traced)")
    pz = affinity.scale(mask_geom(WORK + '/r21/mikes_pizza.png', smooth=SMOOTH['pizza']), sc, sc, origin=(0, 0))
    a.add(pz)
    a.declare('exempt', pz.envelope, "hand lettering: the menu's PIZZA (traced in place, R21)")
    sb = scr.bounds
    a.declare('redrawn', box(sb[2] + 20, sb[1] - 40, pz.bounds[2] + 250, sb[3] + 60),
              'PIZZA: the R21 trace replaces the v1 re-set (League Spartan Black); the old letters are retired on purpose')
    cb = chef.bounds
    # R21 reason a: SERVING SINCE 1954 is ~7 px cap in the source, below the trace floor -> re-set
    sv, _ = T('SERVING SINCE 1954', 'Jost[wght].ttf', cap=70, var=[700], track=0.06)
    sv = move(sv, cx=(cb[0] + cb[2]) / 2 - 20, y=cb[3] - 150)
    a.add(sv, 'typeset', 'Jost Bold; R21 reason a: ~7 px cap in the menu photo')
    ad, _ = T('8160 VAN NUYS BLVD.  ·  PANORAMA CITY', 'Jost[wght].ttf', cap=96, var=[600], track=0.14)
    ad = move(ad, cx=(cb[0] + cb[2]) / 2, y=cb[3] + 140)
    a.add(ad, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'red'
    a.clean = True
    return a


# ------------------------------------------------------------------ C13 The Pass Club
def suit(kind, cx, cy, h):
    """Card suits, constructed (circles, triangles, rhombus), height h, centred."""
    r = h * 0.27
    if kind == 'diamond':
        return Polygon([(cx, cy - h / 2), (cx + h * 0.36, cy), (cx, cy + h / 2), (cx - h * 0.36, cy)])
    if kind in ('heart', 'spade'):
        top = cy - h / 2
        c1 = Point(cx - r * 0.95, top + r).buffer(r, resolution=48)
        c2 = Point(cx + r * 0.95, top + r).buffer(r, resolution=48)
        tri = Polygon([(cx - r * 1.93, top + r * 1.25), (cx + r * 1.93, top + r * 1.25), (cx, top + h * (0.92 if kind == 'heart' else 0.78))])
        g = unary_union([c1, c2, tri]).buffer(2).buffer(-2)
        if kind == 'spade':
            g = affinity.scale(g, 1, -1, origin=(cx, cy - h * 0.06))
            stem = Polygon([(cx - h * 0.04, cy + h * 0.12), (cx + h * 0.04, cy + h * 0.12), (cx + h * 0.16, cy + h / 2), (cx - h * 0.16, cy + h / 2)])
            g = unary_union([g, stem])
        return g
    if kind == 'club':
        rr = h * 0.2
        c = [Point(cx, cy - h * 0.25).buffer(rr, resolution=48), Point(cx - h * 0.22, cy + h * 0.05).buffer(rr, resolution=48),
             Point(cx + h * 0.22, cy + h * 0.05).buffer(rr, resolution=48)]
        stem = Polygon([(cx - h * 0.04, cy), (cx + h * 0.04, cy), (cx + h * 0.16, cy + h / 2), (cx - h * 0.16, cy + h / 2)])
        return unary_union(c + [stem, Point(cx, cy - h * 0.02).buffer(h * 0.1)])


@build
def pass_club():
    """The Pass Club, Santa Susana Pass (card club on the Ventura County side of the pass, 'an ace from the
    LA County line'; Valley Times photo, Oct 14 1963). Source: VRM's post of the LAPL Valley Times photo
    (src/C13; Brad pulled it twice). Our own drawing of the club house with its four card-suit panels, the
    hilltop and the ridge behind; THE PASS CLUB set in Rye, the place line in Jost."""
    a = Art('sfv_pass_club')
    k = 3.0
    # ridge line behind (two soft peaks)
    ridge = [(0, 330), (120, 262), (260, 214), (360, 222), (470, 175), (600, 200), (760, 255), (900, 300), (1000, 325)]
    a.add(brush([(x * k, y * k) for x, y in ridge], [9 * k] * len(ridge)))
    # house
    hx0, hx1, hy = 180 * k, 820 * k, 420 * k
    roof = Polygon([(160 * k, 350 * k), (500 * k, 300 * k), (840 * k, 350 * k), (840 * k, 372 * k), (500 * k, 322 * k), (160 * k, 372 * k)])
    a.add(roof)
    wall = box(hx0, 368 * k, hx1, 560 * k)
    a.add(ring(wall, 8 * k, inner_offset=-8 * k))
    gable = Polygon([(hx0, 368 * k), (500 * k, 322 * k), (hx1, 368 * k)])
    a.add(ring(gable, 6 * k, inner_offset=-6 * k).difference(box(0, 362 * k, 99999, 99999)))
    # board-and-batten lines
    for x in (215, 445, 555, 785):
        a.add(box(x * k - 4, 380 * k, x * k + 4, 548 * k))
    # door + two panels with the suits
    door = box(460 * k, 430 * k, 540 * k, 552 * k)
    a.add(door)
    a.cut(box(498 * k, 440 * k, 502 * k, 552 * k))
    for (x0, kinds) in ((240, ('heart', 'spade')), (580, ('diamond', 'club'))):
        pnl = box(x0 * k, 392 * k, (x0 + 180) * k, 540 * k)
        a.add(ring(pnl, 6 * k, inner_offset=-6 * k))
        a.add(suit(kinds[0], (x0 + 52) * k, 442 * k, 74 * k))
        a.add(suit(kinds[1], (x0 + 128) * k, 492 * k, 74 * k))
    # chimneys
    for cxp in (330, 650):
        a.add(box((cxp - 16) * k, 300 * k, (cxp + 16) * k, 345 * k))
    # hilltop
    hill = [(60, 640), (200, 572), (420, 560), (700, 565), (880, 590), (960, 640)]
    a.add(stroke_line([(x * k, y * k) for x, y in hill], 9 * k))
    a.add(box(160 * k, 556 * k, 840 * k, 568 * k))
    # fence to the right
    for x in range(860, 975, 28):
        a.add(box(x * k - 6, 545 * k, x * k + 6, 590 * k))
    a.add(stroke_line([(850 * k, 552 * k), (985 * k, 560 * k)], 6 * k))
    a.declare('redrawn', box(0, 140 * k, 1000 * k, 650 * k), 'club house + hill: our own drawing after the 1963 photo')
    t1, _ = T('THE PASS CLUB', 'Rye-Regular.ttf', cap=72 * k, track=0.04)
    t1 = move(t1, cx=500 * k, y=60 * k)
    a.add(t1, 'typeset', 'Rye; R21 reason a: no lettering in any source (the 1963 photo shows no sign text)')
    cap, _ = T('SANTA SUSANA PASS  ·  1963', 'Jost[wght].ttf', cap=30 * k, var=[600], track=0.18)
    cap = move(cap, cx=500 * k, y=680 * k)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'cream'
    return a


# ------------------------------------------------------------------ C48 Phil's Diner
def italic(g, deg=10):
    b = g.bounds
    return affinity.skew(g, xs=-deg, origin=(b[0], b[3]))


@build
def phils_diner():
    """Phil's Diner, 11138 Chandler Blvd, North Hollywood (a 1926 dining car beside the Lankershim depot;
    opened 1928; LA Historic-Cultural Monument; moved to Lankershim & Weddington; VRM shows its replica neon).
    Source: VRM's Mar 2026 post of the 1950s photo at Chandler Blvd (src/C48 + Brad's screenshot) and the
    roadarch 2012 photos. Our own side elevation of the car (barrel roof, monitor, scalloped awning, windows,
    lettered panels, end steps) and the pole sign; lettering set in Oswald Bold (car panels, as painted)
    and Oswald Bold sheared 10 deg (pole sign)."""
    a = Art('sfv_phils_diner')
    k = 3.0
    x0, x1 = 120.0, 900.0
    yb, yw0, yr = 620.0, 470.0, 372.0          # bottom of body, top of lower panels, eave line
    body = box(x0 * k, yw0 * k, x1 * k, yb * k)
    a.add(ring(body, 7 * k, inner_offset=-7 * k))
    win = box(x0 * k, yr * k, x1 * k, yw0 * k)
    a.add(ring(win, 6 * k, inner_offset=-6 * k))
    n = 14
    for i in range(1, n):
        x = x0 + (x1 - x0) * i / n
        a.add(box(x * k - 3 * k, yr * k, x * k + 3 * k, yw0 * k))
    # barrel roof: low arch, rounded at both ends
    rise = 46.0
    pts = [((x0 - 14) * k, yr * k)]
    for t in [i / 120 for i in range(121)]:
        x = x0 - 14 + (x1 - x0 + 28) * t
        e = min(t, 1 - t) / 0.07
        y = yr - rise * (math.sqrt(max(0, 1 - (1 - min(e, 1)) ** 2)))
        pts.append((x * k, y * k))
    pts.append(((x1 + 14) * k, yr * k))
    roof = Polygon(pts).buffer(0)
    a.add(ring(roof, 7 * k, inner_offset=-7 * k))
    mon = box((x0 + 110) * k, (yr - rise - 22) * k, (x1 - 110) * k, (yr - rise + 2) * k)
    a.add(ring(mon, 5 * k, inner_offset=-5 * k))
    for i in range(1, 12):
        x = x0 + 110 + (x1 - x0 - 220) * i / 12
        a.add(box(x * k - 2 * k, (yr - rise - 20) * k, x * k + 2 * k, (yr - rise) * k))
    # scalloped awning over the windows
    aw_y = yr + 2
    aw = box(x0 * k, aw_y * k, x1 * k, (aw_y + 14) * k)
    sc = []
    m = 26
    for i in range(m):
        cx = x0 + (x1 - x0) * (i + 0.5) / m
        sc.append(Point(cx * k, (aw_y + 14) * k).buffer((x1 - x0) / m / 2 * k, resolution=24).intersection(box(0, (aw_y + 14) * k, 1e5, 1e5)))
    a.add(unary_union([aw] + sc))
    # lettered panels PHIL'S | DINER, with the door between
    door = box(500 * k, (yw0 + 8) * k, 560 * k, (yb - 6) * k)
    a.add(ring(door, 5 * k, inner_offset=-5 * k))
    words = [("PHIL'S", x0 + 30, 480), ('DINER', 580, x1 - 30)]
    gs = [T(w_, 'Oswald[wght].ttf', cap=100 * k, var=[700], track=0.05)[0] for w_, _, _ in words]
    f = min(1.0, min((lx1 - lx0) * k / width(g) for g, (_, lx0, lx1) in zip(gs, words)))
    base = (yw0 + yb) / 2 * k + 50 * k * f
    for g, (_, lx0, lx1) in zip(gs, words):
        g = affinity.scale(g, f, f, origin=(0, 0))        # same size for both words, one shared baseline
        g = affinity.translate(g, (lx0 + lx1) / 2 * k - (g.bounds[0] + g.bounds[2]) / 2, base)
        a.add(g, 'typeset', 'Oswald Bold; R21 reason a: sign letters ~15-18 px cap in the photo')
    # skirt + wheels-free base and end steps
    a.add(box((x0 - 10) * k, (yb - 2) * k, (x1 + 10) * k, (yb + 14) * k))
    for i in range(3):                     # end steps (solid stair profile)
        a.add(box((x0 - 24 - i * 20) * k, (yb - 34 + i * 16) * k, x0 * k, (yb + 14) * k))
    # pole sign
    px = 520.0
    a.add(box((px - 7) * k, 170 * k, (px + 7) * k, (yr - rise - 22) * k))
    sg = rrect((px - 150) * k, 30 * k, (px + 150) * k, 175 * k, 14 * k)
    a.add(ring(sg, 7 * k, inner_offset=-7 * k))
    s1, _ = T("PHIL'S", 'Oswald[wght].ttf', cap=46 * k, var=[700], track=0.06)
    s2, _ = T('DINER', 'Oswald[wght].ttf', cap=46 * k, var=[700], track=0.12)
    s1 = italic(move(s1, cx=px * k, y=48 * k)); s2 = italic(move(s2, cx=(px + 10) * k, y=110 * k))
    a.add(s1, 'typeset', 'Oswald Bold, sheared 10 deg; R21 reason a: sign letters ~15-18 px cap in the photo')
    a.add(s2, 'typeset', 'Oswald Bold, sheared 10 deg; R21 reason a: sign letters ~15-18 px cap in the photo')
    a.declare('exempt', unary_union([s1, s2]).envelope, 'LEVEL only: italic (sheared) sign lettering; baselines are level')
    a.declare('redrawn', box((x0 - 70) * k, 20 * k, (x1 + 30) * k, (yb + 20) * k), 'dining car + sign: our own drawing after the 1950s photo')
    cap, _ = T('11138 CHANDLER BLVD.  ·  NORTH HOLLYWOOD', 'Jost[wght].ttf', cap=26 * k, var=[600], track=0.14)
    cap = move(cap, cx=(x0 + x1) / 2 * k, y=(yb + 60) * k)
    a.add(cap, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'red'
    return a


# ------------------------------------------------------------------ C23 The Sugar Shack
@build
def sugar_shack():
    """The Sugar Shack, 12458 Magnolia Blvd at Whitsett, North Hollywood (1970s teenage night club, '20 and
    under welcome'; now Joe Peep's Pizza). Sources: VRM's Aug 18 2017 post (211/88/19) and Rick Watts' 1970s
    coupon in the Southern California Memories group (114/40/10), captured 1:1 from the browser (src/C23).
    The wood-plank SUGAR SHACK logo is traced from a x4 Real-ESRGAN upscale (hand lettering, exempt); the
    coupon's other lines are re-set: TeX Gyre Schola Bold (Century, as printed) and Righteous for the
    disco line. No phone number, no hours."""
    a = Art('sfv_sugar_shack')
    sc = 2.35
    logo = affinity.scale(mask_geom(WORK + '/ss_logo_mask.png', smooth=None), sc, sc, origin=(0, 0))
    lb = logo.bounds
    cx = (lb[0] + lb[2]) / 2
    t1, _ = T("L.A.'s Most Popular", 'texgyreschola-bold.otf', cap=120, track=0.025)   # tracked to the gap floor (type is no longer print-cleaned, L44)
    t2, _ = T('Teenage Night Club', 'texgyreschola-bold.otf', cap=120, track=0.025)
    t1 = move(t1, cx=cx, bottom=lb[1] - 260)
    t2 = move(t2, cx=cx, y=t1.bounds[3] + 40)
    a.add(t1, 'typeset', 'TeX Gyre Schola Bold; R21 reason a: ~13 px cap on the coupon photo')
    a.add(t2, 'typeset', 'TeX Gyre Schola Bold; R21 reason a: ~13 px cap on the coupon photo')
    th, _ = T('THE', 'texgyreschola-bold.otf', cap=95, track=0.04)
    th = move(th, x=lb[0] - 60, y=lb[1] + 50)
    a.declare('redrawn', th.envelope.buffer(70), 'THE moved 40 units left, 10 up to clear the logo by the gap floor (type is no longer print-cleaned, L44)')
    a.add(th, 'typeset', 'TeX Gyre Schola Bold; R21 reason a: ~10 px cap on the coupon photo')
    a.add(logo)
    a.declare('exempt', logo.envelope, 'hand lettering: the wood-plank logo from the 1970s coupon (traced)')
    d1, _ = T('DANCING · GAMES · SNACKS', 'Righteous-Regular.ttf', cap=118, track=0.04)
    d1 = move(d1, cx=cx, y=lb[3] + 120)
    a.add(d1, 'typeset', 'Righteous; R21 reason a: ~13 px cap on the coupon photo')
    d2, _ = T('20 and Under Welcome!', 'texgyreschola-bold.otf', cap=110, track=0.0)
    d2 = move(d2, cx=cx, y=d1.bounds[3] + 90)
    a.add(d2, 'typeset', 'TeX Gyre Schola Bold; R21 reason a: ~12 px cap on the coupon photo')
    ad, _ = T('12458 MAGNOLIA BLVD.  ·  NORTH HOLLYWOOD', 'Jost[wght].ttf', cap=88, var=[600], track=0.14)
    ad = move(ad, cx=cx, y=d2.bounds[3] + 120)
    a.add(ad, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    a.ink = 'charcoal'
    a.clean = True
    return a


# ------------------------------------------------------------------ C38 June Ellen's
@build
def june_ellens():
    """June Ellen's donuts, Van Nuys Blvd (one of the cruising turnarounds; 'the June Ellen's side' of the
    boulevard, Daily Sundial 1973-11-06). Source: the rooftop script sign in VRM's post (photo by Rick
    McCloskey, 1972: the photograph itself is not used, only the business's sign script, re-set). 'June
    Ellen's' set in Pacifico (the script on the Cruise Night tee, so the two pair); the rest in Oswald and Jost. Companion to
    the Cruise Night tee."""
    a = Art('sfv_june_ellens')
    s1, adv1 = T_shaped("June Ellen", 'Pacifico-Regular.ttf', size=560)     # whole-string shaping keeps the script joins
    s2, _ = T("’s", 'Pacifico-Regular.ttf', size=560, track=0.04)
    sc = unary_union([s1, affinity.translate(s2, adv1 - 30, 0)])     # apostrophe tucked to the n, clear of it
    sc = move(sc, x=0, y=0)
    a.add(sc, 'typeset', 'Pacifico (the Cruise Night script); R21 reason a: neon script ~18 px cap in a night photo')
    a.declare('exempt', sc.envelope, "LEVEL only: font-set script on a level baseline; the raised apostrophe-s reads as a tilt to the gate")
    W = width(sc)
    cx = sc.bounds[0] + W / 2
    # R21: the sign script is ~18 px in a night photo (neon glare), below the trace floor -> re-set (reason a).
    # Rule 4: one house locator line only (was DONUTS + THE TURNAROUND line).
    y = sc.bounds[3] + 120
    a.add(box(cx - W * 0.36, y, cx + W * 0.36, y + 14))
    t2, _ = T('DONUTS  ·  VAN NUYS BLVD.', 'Jost[wght].ttf', cap=100, var=[600], track=0.18)
    t2 = move(t2, cx=cx, y=y + 80)
    a.add(t2, 'typeset', 'Jost SemiBold (house locator line, R21 rule 4)')
    return a


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in BUILDS.items():
        if ONLY and name not in ONLY:
            continue
        art = fn()
        ink = getattr(art, 'ink', 'cream')
        art.save(OUT, ink=ink, clean=getattr(art, 'clean', False))


if __name__ == '__main__':
    main()
