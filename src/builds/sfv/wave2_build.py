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
    a.declare('redrawn', v, 'VALLEY: monoline channel letters constructed from the sign photo (not traced)')
    a.declare('redrawn', p, 'PLAZA: monoline channel letters constructed from the sign photo (not traced)')
    # pole stub
    pole = box(mid - 70, body_bot - 2, mid + 70, body_bot + 150)
    a.add(pole)
    # caption
    cap, _ = T('NORTH HOLLYWOOD  ·  1951', 'Jost[wght].ttf', cap=95, var=[600], track=0.16)
    cap = move(cap, cx=mid, y=body_bot + 230)
    a.add(cap, 'typeset', 'Jost SemiBold')
    return a


# ------------------------------------------------------------------ C50 Zodys
def vhex(cx, y0, w, h, tip):
    x0, x1 = cx - w / 2, cx + w / 2
    return Polygon([(cx, y0), (x1, y0 + tip), (x1, y0 + h - tip), (cx, y0 + h), (x0, y0 + h - tip), (x0, y0 + tip)])


@build
def zodys():
    """Zodys, 8201 Topanga Canyon Blvd, Canoga Park (opened Sept 27 1962; chain closed 1986). Source: LAPL
    Valley Times photo 00057938 'Radio wave opens doors of Zodys' (src/C50), the five hexagon letter boxes
    on the folded-plate canopy. Boxes are constructed geometry; letters set in Kameron Bold (bracketless
    slab, the nearest OFL match to the box letters), narrowed to the box like the originals."""
    a = Art('sfv_zodys')
    TW, TH, tip, gap = 500.0, 1080.0, 215.0, 74.0
    xs = [TW / 2 + i * (TW + gap) for i in range(5)]
    for cx, ch in zip(xs, 'ZODYS'):
        hx = vhex(cx, 0, TW, TH, tip)
        a.add(hx)
        a.cut(ring(hx, 15, inner_offset=-44))
        g, _ = T(ch, 'Kameron[wght].ttf', cap=500, var=[700])
        g = scale_to(g, w=min(width(g) * 0.78, TW - 2 * 44 - 2 * 15 - 90), xs=None) if False else hscale(g, min(0.78, (TW - 210) / width(g)))
        g = move(g, cx=cx, cy=TH / 2 + 4)
        a.cut(g, 'typeset', 'Kameron Bold (narrowed to the box, max x0.78)')
    a.declare('redrawn', box(0, 0, xs[-1] + TW / 2, TH), 'hexagon boxes: constructed geometry after the LAPL photo')
    mid = (xs[0] + xs[-1]) / 2
    cap, _ = T('CANOGA PARK  ·  1962', 'Jost[wght].ttf', cap=100, var=[600], track=0.18)
    cap = move(cap, cx=mid, y=TH + 120)
    a.add(cap, 'typeset', 'Jost SemiBold')
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
        a.declare('typeset', gl, 'Rokkitt ExtraBold, rotated to the arch (per-glyph)')
        # post from the box down to the shell
        a.add(affinity.rotate(box(px - 9, py + THb / 2 - 4, px + 9, py + lift + 10), rot, origin=(px, py)))
    # script + address
    sc, _ = T('Canoga Park', 'Yellowtail-Regular.ttf', size=430)
    sc = move(sc, cx=cx, y=cy + 170)
    a.add(sc, 'typeset', 'Yellowtail')
    ad, _ = T('21300 ROSCOE BLVD.  ·  OPENED 1963', 'Jost[wght].ttf', cap=88, var=[600], track=0.16)
    ad = move(ad, cx=cx, y=sc.bounds[3] + 110)
    a.add(ad, 'typeset', 'Jost SemiBold')
    a.ink = 'red'
    return a


# ------------------------------------------------------------------ C28 GEMCO
@build
def gemco():
    """GEMCO membership card (Gemco, the members-only department store chain, 1959-1986; Valley stores
    incl. Granada Hills). Source: the membership card on the Roy Hooper Gemco tribute site (src/C28, crop
    only: oval logo, 'DEPARTMENT STORES AND SUPERMARKETS', the diagonal MEMBERSHIP band) + the 1986 VRM
    storefront photo. Card, oval and band are constructed; GEMCO set in Libre Caslon Text Bold (the bold
    old-style roman of the oval and the store letters); the card's sans lines in Jost Bold / Medium. No member name/number. Tees only: a pending IC025
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
    g, _ = T('GEMCO', 'LibreCaslonText[wght].ttf', cap=230, var=[700], track=0.05)
    g = move(g, cx=960, cy=600)
    assert g.buffer(40).within(ov), 'GEMCO crowds the oval'
    a.cut(g, 'typeset', 'Libre Caslon Text Bold')
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
    a.cut(m, 'typeset', 'Jost Bold (rotated with the band)')
    st, _ = T('DEPARTMENT STORES AND SUPERMARKETS', 'Jost[wght].ttf', cap=68, var=[500], track=0.14)
    st = move(st, cx=vc.x - 260, cy=vc.y - 160 - 80)
    st = affinity.rotate(st, ang, origin=(vc.x, vc.y))
    assert st.buffer(30).within(interior), 'small line leaves the card'
    a.add(st, 'typeset', 'Jost Medium (rotated with the band)')
    a.declare('exempt', unary_union([band, st]).envelope, "LEVEL only: band lettering runs on the card's printed diagonal (deliberate angle)")
    pl, _ = T('SAN FERNANDO VALLEY', 'Jost[wght].ttf', cap=95, var=[600], track=0.2)
    pl = move(pl, cx=CW / 2, y=CH + 130)
    a.add(pl, 'typeset', 'Jost SemiBold')
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
    Grown; closed July 2003; now a CVS). Source: Brad's two VRM crops of the pole sign (dup = emphasis) and
    the Roadside Peek / Biondo photos (src/C51). Pole, letter pillows, STEAK/HOUSE boxes and the COFFEE SHOP
    blob are our own drawing of the sign; letters set in Lilita One (pillows), Oswald SemiBold (boxes) and
    Knewave (the brush caps on the blob). The pillows keep the sign's small playful tilts."""
    a = Art('sfv_leons')
    px0, px1 = 610.0, 700.0
    a.add(box(px0, 40, px1, 3160))
    a.add(box(px0 - 18, 10, px1 + 18, 60))
    for y in range(190, 3120, 150):
        a.cut(Point((px0 + px1) / 2, y).buffer(19, resolution=24))
    tilts = [-3.0, 2.0, 0.0, -2.0, 3.0]
    for i, (ch, tl) in enumerate(zip('LEONS', tilts)):
        cy = 320 + i * 396
        cx = 300
        pil = superellipse(cx, cy, 200, 182, n=2.7)
        frame = ring(pil, 26, inner_offset=-26)
        g, _ = T(ch, 'LilitaOne-Regular.ttf', cap=262)
        g = move(g, cx=cx, cy=cy + 4)
        a.add(affinity.rotate(frame, tl, origin=(cx, cy)))
        gl = affinity.rotate(g, tl, origin=(cx, cy))
        a.add(gl)
        a.declare('typeset', gl, 'Lilita One')
        a.declare('exempt', pil.buffer(30), 'LEVEL only: the sign pillows hang at small deliberate tilts (source)')
        a.add(box(cx + 190, cy - 16, px0 + 2, cy + 16))       # bracket to the pole
    for word, y0 in (('STEAK', 520.0), ('HOUSE', 1040.0)):
        bx = box(px1 + 50, y0, px1 + 1020, y0 + 450)
        a.add(bx)
        a.add(box(px1 - 2, y0 + 40, px1 + 52, y0 + 70))
        a.add(box(px1 - 2, y0 + 380, px1 + 52, y0 + 410))
        g, _ = T(word, 'Oswald[wght].ttf', cap=330, var=[600], track=0.04)
        g = scale_to(g, w=820) if width(g) > 820 else g
        g = move(g, cx=(px1 + 50 + px1 + 1020) / 2, cy=y0 + 225)
        a.cut(g, 'typeset', 'Oswald SemiBold')
    # COFFEE SHOP blob: wide shield/kidney shape
    bw, bh, bx0, by0 = 1180.0, 700.0, 70.0, 2290.0
    pts = []
    for i in range(121):
        t = i / 120
        pts.append((bx0 + bw * t, by0 + 40 - 60 * math.sin(math.pi * t)))           # top, arched up
    for i in range(121):
        t = i / 120
        ang = math.pi * t
        pts.append((bx0 + bw / 2 + (bw / 2) * math.cos(ang), by0 + 40 + (bh - 40) * (0.55 + 0.45 * math.sin(ang))))
    blob = Polygon(pts).buffer(0).buffer(-120, join_style=1).buffer(120, join_style=1)
    a.add(blob)
    a.declare('redrawn', blob, 'COFFEE SHOP panel: our own drawing of the sign shape')
    c1, _ = T('COFFEE', 'Knewave-Regular.ttf', cap=190, track=0.03)
    c2, _ = T('SHOP', 'Knewave-Regular.ttf', cap=190, track=0.03)
    bcx = bx0 + bw / 2
    c1 = move(c1, cx=bcx, y=by0 + 150)
    c2 = move(c2, cx=bcx + 20, y=c1.bounds[3] + 55)
    a.cut(c1, 'typeset', 'Knewave')
    a.cut(c2, 'typeset', 'Knewave')
    cap, _ = T('NORTH HOLLYWOOD  ·  1945', 'Jost[wght].ttf', cap=88, var=[600], track=0.16)
    cap = move(cap, cx=(70 + px1 + 1020) / 2, y=3240)
    a.add(cap, 'typeset', 'Jost SemiBold')
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
        a.add(g, 'typeset', f'Kameron Bold (x{f:.2f})')
    a.declare('exempt', unary_union([h2, h3]), 'LEVEL only: the small AND sits raised before ART as on the sign (the gate reads a line through their counters)')
    sl = []
    for txt, cx, y in (('New-Old', 520, 560), ('& Rare', 520, 760), ('Bought', 2480, 560), ('& Sold', 2480, 760)):
        g, _ = T(txt, 'Fredoka[wdth,wght].ttf', cap=118, var=[600, 100], track=0.03)
        g = move(g, cx=cx, y=y)
        a.add(g, 'typeset', 'Fredoka SemiBold')
    books, cuts = books_on_shelf(PW / 2 - 560, 900, 1120)
    a.add(books)
    a.cut(cuts)
    a.declare('redrawn', books.buffer(10), 'books + bookends: our own drawing of the sign motif')
    cap, _ = T('NORTH HOLLYWOOD  ·  1961', 'Jost[wght].ttf', cap=92, var=[600], track=0.16)
    cap = move(cap, cx=PW / 2, y=PH + 140)
    a.add(cap, 'typeset', 'Jost SemiBold')
    a.ink = 'red'
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
    Great White played it). Source: VRM's Sept 2026 post of the rooftop box sign (src/C20; 1.8K/449/192).
    The brush 'FM' is hand lettering at ~85 px in the source, so it is redrawn as brush strokes along the
    measured centrelines (exempt from EDGES/LEVEL as hand lettering); the box and the marquee board are
    constructed; marquee lines set in Oswald SemiBold (no band names: those are live marks)."""
    a = Art('sfv_fm_station')
    f = 2.15
    fm = unary_union([brush([(x + 6, y + 7) for x, y in pts], ws) for pts, ws in FM_STROKES])
    # notched-corner box, as on the sign
    bx = Polygon([(100, 45), (860, 45), (860, 68), (935, 68), (935, 470), (860, 470), (860, 490), (100, 490),
                  (100, 470), (25, 470), (25, 80), (100, 80)])
    bx = affinity.scale(bx, f, f, origin=(0, 0))
    fm = affinity.scale(fm, f, f, origin=(0, 0))
    a.add(bx)
    a.cut(fm)
    a.declare('exempt', fm.buffer(20), 'hand-brushed FM: redrawn as brush strokes along the sign letters')
    a.declare('redrawn', bx, 'box sign: constructed')
    bxb = bx.bounds
    cx = (bxb[0] + bxb[2]) / 2
    # posts
    for px in (cx - 520, cx + 520):
        a.add(box(px - 40, bxb[3] - 5, px + 40, bxb[3] + 190))
    # marquee board
    BW, BH = 3000.0, 1180.0
    y0 = bxb[3] + 185
    board = box(cx - BW / 2, y0, cx + BW / 2, y0 + BH)
    a.add(ring(board, 30, inner_offset=0))
    face = board.buffer(-58, join_style=2)
    a.add(face)
    rows = [('FM STATION', 300), ('NORTH HOLLYWOOD', 230), ('LIVE MUSIC  ·  1976', 170)]
    fb = face.bounds
    ys = [fb[1] + 90, None, None]
    y = fb[1] + 95
    for i, (txt, capx) in enumerate(rows):
        g, _ = T(txt, 'Oswald[wght].ttf', cap=capx, var=[600], track=0.06)
        if width(g) > BW - 300:
            g = scale_to(g, w=BW - 300)
        g = move(g, cx=cx, y=y)
        a.cut(g, 'typeset', 'Oswald SemiBold')
        y = g.bounds[3] + 75
        if i < len(rows) - 1:
            a.cut(box(fb[0] + 40, y - 34, fb[2] - 40, y - 20))     # letter rail
            y += 10
    a.declare('redrawn', board, 'marquee board: constructed')
    return a


# ------------------------------------------------------------------ C30 Weber's Place
@build
def webers():
    """Weber's Place, 19312 Vanowen St, Reseda (dive bar with live music and punk shows). Source: VRM's May
    2026 photo of the sign itself (VRM holds it; src/C30). Oval panel and the PLACE box are constructed;
    'Weber's' set in TeX Gyre Bonum Bold Italic (Bookman Bold Italic, the sign's face; GUST font licence,
    free for commercial use, already used on the Hammond Casa ad), PLACE in TeX Gyre Bonum Bold."""
    a = Art('sfv_webers_place')
    OW, OH = 3000.0, 1220.0
    cx, cy = OW / 2, OH / 2
    ov = affinity.scale(Point(0, 0).buffer(1, resolution=160), OW / 2, OH / 2)
    ov = affinity.translate(ov, cx, cy)
    rules = unary_union([ring(ov, 34, inner_offset=-34), ring(ov, 16, inner_offset=-96)])
    w, _ = T("Weber's", 'texgyrebonum-bolditalic.otf', cap=520, track=0.0)
    w = move(w, cx=cx - 30, y=150)
    pl, _ = T('PLACE', 'texgyrebonum-bold.otf', cap=170, track=0.05)
    pb = box(0, 0, width(pl) + 150, height(pl) + 110)
    pb = move(pb, cx=cx + 40, y=w.bounds[3] + 70)
    # the oval's rules break around the big letters and the PLACE box; slivers opened out (< 0.05 in)
    rules = rules.difference(unary_union([w.buffer(60), pb.buffer(60, join_style=2)]))
    rules = rules.buffer(-7, join_style=2).buffer(7, join_style=2)
    rules = unary_union([p_ for p_ in getattr(rules, 'geoms', [rules]) if p_.area > 4000])
    a.add(rules)
    a.add(w, 'typeset', 'TeX Gyre Bonum Bold Italic')
    a.add(pb)
    pl = move(pl, cx=(pb.bounds[0] + pb.bounds[2]) / 2, cy=(pb.bounds[1] + pb.bounds[3]) / 2)
    a.cut(pl, 'typeset', 'TeX Gyre Bonum Bold')
    a.declare('redrawn', ov, 'oval panel + PLACE box: constructed')
    cap, _ = T('19312 VANOWEN ST.  ·  RESEDA', 'Jost[wght].ttf', cap=92, var=[600], track=0.16)
    cap = move(cap, cx=cx, y=OH + 120)
    a.add(cap, 'typeset', 'Jost SemiBold')
    return a


# ------------------------------------------------------------------ C27 Moby Disc
WORK = '/home/claude/sfv2/work'


def mask_geom(path, smooth=3, alphamax=1.0, min_area=60):
    import numpy as np
    from PIL import Image
    m = np.array(Image.open(path).convert('L')) > 127
    return trace_geom(m, alphamax=alphamax, smooth_sigma=smooth)


@build
def moby_disc():
    """Moby Disc Records (14410 Ventura Blvd, Sherman Oaks; 6553 Topanga Canyon Blvd, Canoga Park; early
    1970s-2001). Source: the store's inner record sleeve, Flickr 5379507456 original 2520 px (src/C27). The
    whale, spout, record, waves and splash are traced from a x4 Real-ESRGAN upscale of the sleeve print and
    cleaned (illustration: exempt); MOBY DISC RECORDS is re-set on the arc in Fraunces Black Italic (soft,
    the Cooper-style face of the sleeve), narrowed x0.78; the tagline re-set in the same face. VRM sells a
    whale tee: ours is redrawn, adds the two Valley stores, and uses its own layout."""
    a = Art('sfv_moby_disc')
    FR = 'Fraunces-Italic[SOFT,WONK,opsz,wght].ttf'
    V = [72, 900, 100, 0]
    illu = mask_geom(WORK + '/moby_illu.png', smooth=None)     # smoothing lost the record-label ring (part B)
    a.add(illu)
    a.declare('exempt', illu.buffer(10).envelope, 'illustration: whale, record, waves, splash traced from the sleeve (cleaned)')
    cx, cy = 415 * 4, 470 * 4
    size = 400 / cap_ratio(FR, V)
    txt = 'MOBY DISC   RECORDS'
    arc = arc_text(txt, FR, size, cx, cy, 1330, centre_deg=-89, var=V, track=0.02, xs=0.78, anchor=txt.index('   ') + 1)
    a.add(arc)
    a.declare('exempt', arc.envelope, "LEVEL only: lettering set on the sleeve's arc (typeset glyph by glyph in Fraunces Black Italic Soft)")
    t1, _ = T('A Whale', FR, cap=150, var=V, track=0.02)
    t2, _ = T('of a Store!', FR, cap=150, var=V, track=0.02)
    t1 = move(t1, x=90, y=3010)
    t2 = move(t2, x=150, y=t1.bounds[3] + 70)
    a.cut(unary_union([t1, t2]).buffer(45))
    a.add(t1, 'typeset', 'Fraunces Black Italic Soft')
    a.add(t2, 'typeset', 'Fraunces Black Italic Soft')
    cap, _ = T('SHERMAN OAKS  ·  CANOGA PARK', 'Jost[wght].ttf', cap=115, var=[600], track=0.16)
    cap = move(cap, cx=cx, y=4630)
    a.add(cap, 'typeset', 'Jost SemiBold')
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
    a.add(cap, 'typeset', 'Jost SemiBold')
    a.ink = 'charcoal'
    a.clean = dict(hair_in=0.027)
    return a


# ------------------------------------------------------------------ C07 Devonshire Downs
@build
def devonshire_downs():
    """Devonshire Downs, 18000 Devonshire St, Northridge (harness track 1946; SFV Fair grounds; San Fernando
    Valley State College from the 1960s; Newport '69; razed 2001). Source: the 1960-65 rental flyer, CSUN
    Special Collections scan 1553 x 2083 (src/C07; same image as VRM's post). Our own drawing of the
    pediment sign (tapered panel, cornice, finial, display case, posts); 'Devonshire Downs' re-set in Libre
    Caslon Text Bold; the flyer's script line re-set in Damion."""
    a = Art('sfv_devonshire_downs')
    k = 3.0
    def P(pts):
        return Polygon([(x * k, y * k) for x, y in pts])
    lw = 14 * 1.0
    panel = P([(285, 130), (740, 130), (688, 512), (337, 512)])
    a.add(ring(panel, lw * 2.0, inner_offset=-lw * 2.0))
    # pediment: cornice band rising to the finial
    ped_out = P([(258, 135), (515, 62), (770, 135), (770, 150), (515, 80), (258, 150)])
    a.add(ped_out)
    a.add(Point(515 * k, 50 * k).buffer(25 * k, resolution=64))
    a.cut(Point(509 * k, 44 * k).buffer(8 * k, resolution=32))            # highlight on the ball
    # display case
    case = box(380 * k, 272 * k, 635 * k, 486 * k)
    a.add(ring(case, 5 * k, inner_offset=0))
    a.add(ring(case.buffer(-12 * k, join_style=2), 3.4 * k, inner_offset=0))
    a.add(Point(392 * k, 302 * k).buffer(5 * k))                          # latch
    # glass glints
    for x0, y0, x1, y1 in ((430, 320, 470, 280 + 20), (455, 380, 545, 300), (500, 440, 600, 340)):
        a.add(stroke_line([(x0 * k, y0 * k), (x1 * k, y1 * k)], 3.2 * k).intersection(case.buffer(-16 * k)))
    # base moulding + posts
    a.add(box(330 * k, 505 * k, 695 * k, 524 * k))
    for px in (410, 614):
        a.add(box((px - 9) * k, 524 * k, (px + 9) * k, 610 * k))
    a.declare('redrawn', box(250 * k, 20 * k, 780 * k, 612 * k), 'sign: our own drawing after the flyer illustration')
    t1, _ = T('Devonshire', 'LibreCaslonText[wght].ttf', cap=46 * k, var=[700], track=0.035)
    t2, _ = T('Downs', 'LibreCaslonText[wght].ttf', cap=46 * k, var=[700], track=0.035)
    t1 = move(t1, cx=512 * k, bottom=200 * k)
    t2 = move(t2, cx=512 * k, bottom=252 * k)
    a.add(t1, 'typeset', 'Libre Caslon Text Bold')
    a.add(t2, 'typeset', 'Libre Caslon Text Bold')
    sT, advT = T('T', 'Damion-Regular.ttf', cap=36 * k)
    sR, _ = T("he San Fernando Valley's only complete", 'Damion-Regular.ttf', cap=36 * k, track=0.025)
    s1 = unary_union([sT, affinity.translate(sR, advT + 40, 0)])     # the T bar clears the h
    s2, _ = T('fair grounds and exhibit facility!', 'Damion-Regular.ttf', cap=36 * k, track=0.025)
    s1 = move(s1, cx=512 * k, y=640 * k)
    s2 = move(s2, cx=540 * k, y=s1.bounds[3] + 20 * k)
    a.add(s1, 'typeset', 'Damion')
    a.add(s2, 'typeset', 'Damion')
    a.declare('exempt', unary_union([s1, s2]).envelope, 'LEVEL only: Damion is a casual brush script whose letters ride the baseline unevenly by design (set from the font on a level baseline)')
    cap, _ = T('18000 DEVONSHIRE ST.  ·  NORTHRIDGE', 'Jost[wght].ttf', cap=24 * k, var=[600], track=0.16)
    cap = move(cap, cx=512 * k, y=s2.bounds[3] + 50 * k)
    a.add(cap, 'typeset', 'Jost SemiBold')
    a.ink = 'red'
    return a


# ------------------------------------------------------------------ C40 Fantasy Faire 1967
@build
def fantasy_faire():
    """Fantasy Faire and Magic Music Festival, July 15-16 1967, at Devonshire Downs ('Devonshire Meadows' on
    the poster), Northridge. Source: the 1967 poster (Penny Havard / The Gates of Eden; Circle Printing, LA),
    PAE lot 13574, 1999 x 2804 (src/C40). No copyright notice appears on the poster (1909 Act: published
    without notice). Only the hand lettering is used, traced from the red plate and lightly cleaned (hand
    lettering: exempt); no band names (live marks), no figures, no times. Caption set in Jost."""
    a = Art('sfv_fantasy_faire_1967')
    sc = 1.9
    ys = 0.0
    blocks = []
    for name, gap in (('A', -10), ('B', 60), ('C', 0)):
        g = mask_geom(WORK + f'/ff_{name}.png', smooth=None)
        g = affinity.scale(g, sc, sc, origin=(0, 0))
        blocks.append((g, gap))
    W = max(width(g) for g, _ in blocks)
    y = 0
    for g, gap in blocks:
        g = move(g, cx=W / 2, y=y)
        a.add(g)
        a.declare('exempt', g.envelope, 'hand lettering from the 1967 poster: traced from the red plate, lightly cleaned')
        y = g.bounds[3] + gap + 60
    cap, _ = T('NORTHRIDGE, CALIF.  ·  1967', 'Jost[wght].ttf', cap=100, var=[600], track=0.18)
    cap = move(cap, cx=W / 2, y=y + 60)
    a.add(cap, 'typeset', 'Jost SemiBold')
    a.ink = 'red'
    a.clean = True
    return a


# ------------------------------------------------------------------ C42 Rusty's Hacienda
@build
def rustys():
    """Rusty's Hacienda, 6439 Lankershim Blvd near Victory, North Hollywood (Mexican family restaurant; also
    Glendale and El Monte; c.1965-1970s). Source: the c.1965 take-out menu header, LAPL Menu Collection
    MENU-002225 (src/C42), and the 1972 Valley News ad in Brad's VRM post. The menu's brush lettering is
    re-set in Knewave (a heavy brush italic, the closest OFL match); the menu's mascot is left out (period
    caricature). No phone numbers."""
    a = Art('sfv_rustys_hacienda')
    t0, _ = T('Bienvenidos Amigos', 'Knewave-Regular.ttf', cap=170, track=0.03)
    t1, _ = T("Rusty's Hacienda", 'Knewave-Regular.ttf', cap=335, track=0.015)
    t2, _ = T('Enjoy a Delicious Margarita Cocktail', 'Knewave-Regular.ttf', cap=150, track=0.03)
    t3, _ = T("While You're Waiting", 'Knewave-Regular.ttf', cap=150, track=0.03)
    W = width(t1)
    t0 = move(t0, x=40, y=0)
    t1 = move(t1, cx=W / 2, y=t0.bounds[3] + 90)
    t2 = move(t2, cx=W / 2, y=t1.bounds[3] + 170)
    t3 = move(t3, cx=W / 2, y=t2.bounds[3] + 60)
    for g in (t0, t1, t2, t3):
        a.add(g, 'typeset', 'Knewave')
    a.declare('exempt', unary_union([t0, t1, t2, t3]).envelope, 'LEVEL only: Knewave is a brush italic whose letters ride the baseline unevenly by design (set from the font on a level baseline)')
    y = t3.bounds[3] + 120
    a.add(box(W * 0.12, y, W * 0.88, y + 16))
    cap, _ = T('NO. HOLLYWOOD  ·  6439 LANKERSHIM BLVD.', 'Jost[wght].ttf', cap=82, var=[600], track=0.14)
    cap = move(cap, cx=W / 2, y=y + 80)
    a.add(cap, 'typeset', 'Jost SemiBold')
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
    RESTAURANT AND COFFEE SHOP re-set in Oswald SemiBold, the address in Jost; no phone number."""
    a = Art('sfv_dons')
    logo = mask_geom(WORK + '/dons_clean.png', smooth=None)     # smoothing erased the eyes/smile (part B): raw potrace curves
    logo = affinity.scale(logo, 1.9, 1.9, origin=(0, 0))
    lb = logo.bounds
    a.add(logo)
    a.declare('exempt', logo.envelope, "hand lettering + chef illustration from the menu cover (traced, cleaned)")
    cx = (lb[0] + lb[2]) / 2 + 40
    l1, _ = T('RESTAURANT', 'Oswald[wght].ttf', cap=190, var=[600], track=0.08)
    l2, _ = T('AND', 'Oswald[wght].ttf', cap=120, var=[600], track=0.1)
    l3, _ = T('COFFEE SHOP', 'Oswald[wght].ttf', cap=190, var=[600], track=0.08)
    l1 = move(l1, cx=cx, y=lb[3] + 150)
    l2 = move(l2, cx=cx, y=l1.bounds[3] + 60)
    l3 = move(l3, cx=cx, y=l2.bounds[3] + 60)
    for g in (l1, l2, l3):
        a.add(g, 'typeset', 'Oswald SemiBold')
    ad, _ = T('509 SOUTH GLENOAKS BLVD.  ·  BURBANK, CALIF.', 'Jost[wght].ttf', cap=80, var=[600], track=0.12)
    ad = move(ad, cx=cx, y=l3.bounds[3] + 110)
    a.add(ad, 'typeset', 'Jost SemiBold')
    a.ink = 'charcoal'
    a.clean = True
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
