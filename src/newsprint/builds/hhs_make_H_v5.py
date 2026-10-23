"""HHS H v5 (Brad 10-22 19:02 markup on v4e): the two yellow areas omitted - the shoulder flag (and the shoulder corner
under it) and the stem bottom below the line of the foot sweep (the stem now ends on the sweep, the h foot flag goes with it) -
the ear mirrored vertically so its hairline leaves the stem top, arcs over and drops into the ball (as on the 1983 jersey),
and every new junction rounded. Built on v4e:
HHS H v4e (Brad 10-22 13:34 markups): minimal additive/subtractive edits to v4, all in Manufacturing Consent's own vocabulary.
  1 top-centre  : spur stroke = MC capital H's left element UNCUT at the top - its stem rises into MC's own diagonal hairline,
                  which now lands on the h ascender (exactly where MC lands it on its hairline). Replaces v4's flat chop.
  2 top-right   : boxy i-dot + neck removed. Ear = MC capital J's own ball terminal (hairline curling into a ball), mirrored,
                  attached to the ascender's right side the way MC attaches the r's ear.
  3 bottom-left : spur stroke's foot UNCUT - MC's full sweep with its own pointed tip runs under the h stem (as it runs under MC's
                  hairline); the h foot's left spur, which collided with it, removed.
  4 bottom-right: leg ends in a ball (same MC J ball) instead of a flat pen cut - the jersey's rounded leg end.
Shapes are the font's; only scale, rotation, position chosen.
v5.2 (Brad 21:00): the leg end is one clean capsule (fitted straight edges + tangent half-circle)."""
import re, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
D = f"{HB}/hhs"
sys.path.insert(0, f"{HB}/lib")
from newsprint import vectorize, render_svg
P = dict(L_h=1000, h_h=930, h_x=330, h_y=70, cond=0.8, lean=-0.12,
         ear_s=0.75, ear_rot=-46.0, ear_dx=0, ear_dy=50,       # ear: scale, rotation (deg, +=ccw), anchor offset below ascender top-right
         leg_trim=985, ball_k=1.08, ball_dx=6, ball_dy=0,  # leg: trim row (h px @1600), ball diameter / leg width, ball offset
         spur_cut=95, fillet=6, slot_x=405, ear_cut=240, foot_r=18, foot_dx=25, fillet_ball=30, foot_dy=0, out="v5",
         ear_flip=1, ear_vdy=20, ear_fillet=22, cut_on=1, cut_slope=-0.9, cut_dy=0, sh_on=1, smooth_r=7)
for kv in sys.argv[1:]:
    k, v = kv.split("="); P[k] = v if k == "out" else float(v)

def crop(a): ys, xs = np.where(a); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def disk(r): r = max(1, int(r)); return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
def scale(a, s, sx=1.0):
    return cv2.resize(a.astype(np.uint8) * 255, (max(1, round(a.shape[1] * s * sx)), max(1, round(a.shape[0] * s))), interpolation=cv2.INTER_AREA) > 127

# ---- parts ------------------------------------------------------------------------------------------------
L0 = np.load(f"{D}/mcH_Lfull.npy")                            # MC H left element: top swash, stem + rising hairline, spur, full foot
def close_channel(L0, x_end):
    """1: the stem's rising hairline flows into the top swash - close the right end of the channel between them,
    leaving a round-ended slot (white) to the left of x_end."""
    yy, xx = np.mgrid[:L0.shape[0], :L0.shape[1]]
    zone = (xx > 380) & (xx < 456) & (yy > 30) & (yy < 160)
    n, lab, st, _ = cv2.connectedComponentsWithStats((~L0 & zone).astype(np.uint8), 4)
    ch = lab == lab[70, 450]                                                     # the channel itself (not the background right of the stem)
    assert lab[70, 450] > 0
    ys, xs = np.where(ch); u = np.array([np.cos(np.radians(-31)), np.sin(np.radians(-31))])   # channel axis (rises right ~31 deg)
    t = (xs - x_end) * u[0] + (ys - 0) * u[1]
    # centre-line point at x_end: midway between swash underside and tail top in that column
    col = np.where(ch[:, x_end])[0]; cy = (col.min() + col.max()) / 2; r = (col.max() - col.min()) / 2 * np.cos(np.radians(31))
    proj = (xs - x_end) * u[0] + (ys - cy) * u[1]
    keep_white = (proj < 0) | ((xs - x_end) ** 2 + (ys - cy) ** 2 <= r * r)
    out = L0.copy(); out[ys[~keep_white], xs[~keep_white]] = True
    return out
L1 = close_channel(L0, int(P["slot_x"])) if P["slot_x"] > 0 else L0
n_, lab_L, st_L, _ = cv2.connectedComponentsWithStats(L1.astype(np.uint8), 8)
foot_id = 1 + int(np.argmax(st_L[1:, 1]))                    # MC draws the foot as its own stroke (lowest component)
FOOT = lab_L == foot_id; L = L1 & ~FOOT                      # kept in the same box so the default placement is MC's
h = np.load(f"{D}/mch.npy").copy(); hy, hx = np.mgrid[:h.shape[0], :h.shape[1]]
h[(hx < P["spur_cut"]) & (hy > 840)] = False                 # 3: h foot's left spur (collides with the spur stroke's foot)
leg_zone = hx > 300
h[leg_zone & (hy > P["leg_trim"])] = False                   # 4: leg cut above the baseline; the ball finishes it
h[(hy > 1030)] = False
Jfull = np.load(f"{D}/mcJ_ball_piece.npy"); xc = int(P["ear_cut"])
Jp = Jfull[:, :xc][:, ::-1]                                  # MC J ball terminal (ball + curl + a short run of its hairline), mirrored
col = np.where(Jfull[:, xc - 1])[0]; J_anchor = (0.0, float(col.mean()))   # the hairline's cut end (buried in the ascender)
ys_, xs_ = np.where(np.load(f"{D}/mcJ_ball_piece.npy")[:, :230][:260])
ball_d0 = 218.0                                              # MC J ball diameter @1600

def transform(piece, anchor, s, rot):
    p = scale(piece, s).astype(np.uint8) * 255; ax, ay = anchor[0] * s, anchor[1] * s
    hh, ww = p.shape; c = (ww / 2, hh / 2)
    M = cv2.getRotationMatrix2D(c, rot, 1.0); cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(hh * sin + ww * cos) + 4, int(hh * cos + ww * sin) + 4
    M[0, 2] += nw / 2 - c[0]; M[1, 2] += nh / 2 - c[1]
    q = cv2.warpAffine(p, M, (nw, nh)) > 127
    a = M @ np.array([ax, ay, 1.0]); return q, (a[0], a[1])

def build(P):
    k = P["h_h"] / h.shape[0] * (1030 / h.shape[0]) ** 0   # h scale (height of the untrimmed glyph box maps to h_h)
    k = P["h_h"] / 1030.0
    sL = P["L_h"] / L1.shape[0]
    Ls = scale(L, sL, P["cond"]); Fs = scale(FOOT, sL, P["cond"]); hs = scale(h, k, P["cond"])
    Wc = Hc = 1500; c = np.zeros((Hc, Wc), bool); ox = oy = 120
    def put(m, x, y):
        x, y = int(round(x)) + ox, int(round(y)) + oy; c[y:y + m.shape[0], x:x + m.shape[1]] |= m
    put(Ls, 0, 0); put(Fs, P["foot_dx"], P["foot_dy"])
    hc = np.zeros_like(c); x_, y_ = int(round(P["h_x"])) + ox, int(round(P["h_y"])) + oy; hc[y_:y_ + hs.shape[0], x_:x_ + hs.shape[1]] = hs
    yy0, xx0 = np.mgrid[:Hc, :Wc]
    Fc = np.zeros_like(c); x0f_, y0f_ = ox + int(round(P["foot_dx"])), oy + int(round(P["foot_dy"])); Fc[y0f_:y0f_ + Fs.shape[0], x0f_:x0f_ + Fs.shape[1]] = Fs
    if P["cut_on"]:
        # lower yellow: the stem below the foot sweep's line goes (h foot flag included). Line: through the sweep's top-right tip
        # (where it meets the stem's left edge), rising right at cut_slope - the box Brad drew.
        st_l = np.where(hc[y_ + int(700 * k)])[0].min()                       # stem left edge, lower stem
        fy = np.where(Fc[:, st_l - 2:st_l + 6].any(1))[0]; jy = fy.min() + (fy.max() - fy.min()) * 0.62 + P["cut_dy"]
        below = yy0 > jy + P["cut_slope"] * (xx0 - st_l)
        hc &= ~(below & (xx0 >= st_l - 4) & (xx0 < x_ + int(398 * k * P["cond"])) & (yy0 > y_ + int(600 * k)))   # up to the flag tip, short of the leg
    if P["sh_on"]:
        # upper yellow: the shoulder flag and the corner under it - everything right of the line from the arch's descending edge
        # (MC h px 493,373 -> 666,579: the box Brad drew) goes; the leg's own right edge then carries on up to the arch.
        def hp(px, py): return x_ + px * k * P["cond"], y_ + py * k
        (ax_, ay_), (bx_, by_) = hp(493, 373), hp(666, 579)
        right = (xx0 - ax_) * (by_ - ay_) - (yy0 - ay_) * (bx_ - ax_) > 0
        hc &= ~(right & (yy0 < by_ + 5) & (yy0 > y_ + 300 * k))       # (the flag tip rises above the line start)
    c |= hc
    if P["smooth_r"] > 0:
        # 'smoothed out naturally': round only the new corners - sweep/stem junction, stem's cut end, shoulder
        sr = int(P["smooth_r"]); zone = np.zeros_like(c)
        if P["cut_on"]:
            zone |= (cv2.dilate(Fc.astype(np.uint8), disk(40)) > 0) & (xx0 > st_l - 60) & (xx0 < x_ + int(300 * k * P["cond"]) + 30) & (yy0 > y_ + int(600 * k))
        if P["sh_on"]:
            zone |= (xx0 > ax_ - 40) & (yy0 > ay_ - 50) & (yy0 < by_ + 40)
        sm = cv2.GaussianBlur(c.astype(np.float32), (0, 0), sr) > 0.5
        c = np.where(zone, sm, c)
    # 2: ear - hairline anchored inside the ascender, just under its top-right corner
    ear, a = transform(Jp, J_anchor, P["ear_s"], P["ear_rot"])
    tx = P["h_x"] + 262 * k * P["cond"] + P["ear_dx"] - 6; ty = P["h_y"] + P["ear_dy"]
    if P["ear_flip"]:                                         # v5: mirrored top-to-bottom - hairline rises from the stem top into the ball
        ear = ear[::-1]; a = (a[0], ear.shape[0] - 1 - a[1]); ty = P["h_y"] + P["ear_vdy"]
    put(ear, tx - a[0], ty - a[1])
    # 4: leg ball - centred on the leg's end, diameter = ball_k x the leg's width there
    row = int(round(P["h_y"] + P["leg_trim"] * k)) + oy - 2
    cols = np.where(c[row, :])[0]; cols = cols[cols > ox + P["h_x"] + 300 * k * P["cond"]]
    lw = cols.max() - cols.min(); cx = (cols.max() + cols.min()) / 2
    r = lw * P["ball_k"] / 2
    yy, xx = np.mgrid[:Hc, :Wc]
    ball = (xx - (cx + P["ball_dx"])) ** 2 + (yy - (row - r * 0.15 + P["ball_dy"])) ** 2 <= r * r
    before = c.copy(); c |= ball
    # joins: MC's own joins are crisp, so only a small radius where pieces meet; the ball flares into the leg like MC's J ball
    def fillet(c, seed, r, reach, only=None):
        if not seed.any(): return c
        src = c if only is None else (c & only)              # close only the given piece (never bridge to a neighbour)
        closed = cv2.morphologyEx(src.astype(np.uint8), cv2.MORPH_CLOSE, disk(r)) > 0
        return c | (closed & (cv2.dilate(seed.astype(np.uint8), disk(reach)) > 0))
    hm = hc
    c = fillet(c, ball & before, int(P["fillet_ball"]), int(2.5 * P["fillet_ball"]),
               only=(xx > ox + P["h_x"] + 390 * k * P["cond"]) & (yy > oy + P["h_y"] + 700 * k))   # the leg only (h foot flag sits at x<375)
    if P.get("leg_hull", 1):
        # v5.1 (Brad 20:34): the leg runs into the ball with no notch or kink - the leg's last stretch and the ball are
        # wrapped in their convex hull, so both edges meet the ball on a tangent
        bcy = row - r * 0.15 + P["ball_dy"]
        zone = (xx > ox + P["h_x"] + 390 * k * P["cond"]) & (yy > bcy - P.get("hull_reach", 2.4) * r)
        pts = np.column_stack(np.where(c & zone))[:, ::-1].astype(np.int32)
        hull = np.zeros_like(c, dtype=np.uint8); cv2.fillPoly(hull, [cv2.convexHull(pts)], 1)
        c = c | ((hull > 0) & zone)
        # round the one remaining corner (left side, where the leaning leg edge meets the ball)
        ro = int(round(P.get("leg_round", 0.7) * r))
        zbig = (xx > ox + P["h_x"] + 390 * k * P["cond"]) & (yy > bcy - P.get("hull_reach", 2.4) * r - 3 * ro)
        opened = cv2.morphologyEx((c & zbig).astype(np.uint8), cv2.MORPH_OPEN, disk(ro)) > 0
        c = np.where(zone, opened, c)
    if P.get("leg_capsule_prelean", 0):
        # v5.2 (Brad 21:00): the leg's last stretch rebuilt as one clean capsule - both edges fitted as straight lines over
        # the leg's lower third, ending in a half-circle tangent to both (no wobble, notch or step where leg meets ball)
        bcy = row - r * 0.15 + P["ball_dy"]
        lx0 = ox + P["h_x"] + 390 * k * P["cond"]
        ytop = int(bcy - P.get("cap_reach", 3.2) * r); yfit1 = int(bcy - 0.25 * r)
        rows_, L_, R_ = [], [], []
        for y in range(ytop, yfit1):
            xs = np.where(c[y, int(lx0):])[0]
            if len(xs): rows_.append(y); L_.append(lx0 + xs.min()); R_.append(lx0 + xs.max())
        rows_ = np.array(rows_); pl = np.polyfit(rows_, L_, 1); pr = np.polyfit(rows_, R_, 1)
        xl_c, xr_c = np.polyval(pl, bcy), np.polyval(pr, bcy)
        ccx, rr = (xl_c + xr_c) / 2, (xr_c - xl_c) / 2
        band = (yy >= ytop) & (xx >= lx0 - 2)
        cap = np.zeros_like(c, dtype=np.uint8)
        poly = np.array([[np.polyval(pl, ytop), ytop], [np.polyval(pr, ytop), ytop], [xr_c, bcy], [xl_c, bcy]], np.float32)
        cv2.fillPoly(cap, [np.round(poly * 8).astype(np.int32)], 1, lineType=cv2.LINE_8, shift=3)
        cap = (cap > 0) | ((xx - ccx) ** 2 + (yy - bcy) ** 2 <= rr * rr)
        c = np.where(band, cap, c)
    ear_mask = np.zeros_like(c); x0, y0 = int(round(tx - a[0])) + ox, int(round(ty - a[1])) + oy
    ear_mask[y0:y0 + ear.shape[0], x0:x0 + ear.shape[1]] = ear
    c = fillet(c, ear_mask & (cv2.dilate(hm.astype(np.uint8), disk(2)) > 0), int(P["ear_fillet"]), int(3 * P["ear_fillet"]))   # v5: the stem top flows into the hairline
    # 3: the spur stroke's foot runs into the h stem
    Fm = np.zeros_like(c); x0f, y0f = ox + int(round(P["foot_dx"])), oy + int(round(P["foot_dy"])); Fm[y0f:y0f + Fs.shape[0], x0f:x0f + Fs.shape[1]] = Fs
    c = fillet(c, Fm & (cv2.dilate(hm.astype(np.uint8), disk(3)) > 0), int(P["foot_r"]), int(4 * P["foot_r"]))
    poke = Fm & ~(cv2.dilate(hm.astype(np.uint8), disk(1)) > 0) & (xx > np.where(hm.any(0))[0].min() + 60)
    if poke.sum() > 50: print("WARN foot tip pokes past the h stem:", int(poke.sum()), "px")
    c = crop(c); Hh, Ww = c.shape; M = np.float32([[1, P["lean"], max(0, -P["lean"] * Hh)], [0, 1, 0]])
    out = crop(cv2.warpAffine(c.astype(np.uint8), M, (int(Ww + abs(P["lean"]) * Hh) + 2, Hh)) > 0)
    return leg_capsule(out) if P.get("leg_capsule", 1) else out

def leg_capsule(M, y0f=0.62):
    """v5.2 (Brad 21:00): rebuild the leg's lower stretch, after the lean, as one clean capsule: its two edges fitted as
    straight lines, ending in a half-circle tangent to both (cut perpendicular to the leg's axis at the tangent points),
    so nothing wobbles, notches or steps where the leg meets its round end."""
    H, W = M.shape; y0 = int(H * y0f)
    runs = {}
    for y in range(y0, H):
        xs = np.where(M[y])[0]
        if not len(xs): continue
        # the rightmost run of ink in the row is the leg
        br = np.where(np.diff(xs) > 1)[0]; start = xs[br[-1] + 1] if len(br) else xs[0]
        runs[y] = (start, xs[-1])
    ys = np.array(sorted(runs)); yb = ys.max()
    L = np.array([runs[y][0] for y in ys], float); R = np.array([runs[y][1] for y in ys], float)
    w0 = np.median((R - L)[: len(ys) // 2]); r_est = w0 / 2
    fit = ys < yb - 2.6 * r_est
    pl = np.polyfit(ys[fit], L[fit], 1); pr = np.polyfit(ys[fit], R[fit], 1)
    s_ = (pl[0] + pr[0]) / 2                                   # dx/dy of the leg axis
    th = np.arctan(-s_)                                        # lean angle from vertical (leg tops lean right: s_ < 0)
    hw = (np.polyval(pr, yb) - np.polyval(pl, yb)) / 2         # half width, horizontal
    r = hw * np.cos(th)                                        # perpendicular half width = circle radius
    # centre on the axis, so the circle's lowest point sits on the leg's original bottom
    cy = yb - r; cx = (np.polyval(pl, cy) + np.polyval(pr, cy)) / 2
    n = np.array([np.cos(th), np.sin(th)])                     # unit normal to the edges (pointing right)
    tl = np.array([cx, cy]) - r * n; tr = np.array([cx, cy]) + r * n
    yy, xx = np.mgrid[:H, :W]
    zone = np.zeros_like(M)
    for y, (a, b) in runs.items(): zone[y, a:b + 1] = True
    zone = (cv2.dilate(zone.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0) & (yy >= y0)
    out = M & ~zone
    cap = np.zeros((H, W), np.uint8)
    poly = np.array([[np.polyval(pl, y0 - 3), y0 - 3], [np.polyval(pr, y0 - 3), y0 - 3], tr, tl], np.float32)
    cv2.fillPoly(cap, [np.round(poly * 16).astype(np.int32)], 1, shift=4)
    cv2.circle(cap, (int(round(cx * 16)), int(round(cy * 16))), int(round(r * 16)), 1, -1, shift=4)
    return out | (cap > 0)

def hs_mask(c, hs, P, ox, oy, k):
    m = np.zeros_like(c); x, y = int(round(P["h_x"])) + ox, int(round(P["h_y"])) + oy
    m[y:y + hs.shape[0], x:x + hs.shape[1]] = hs; return m

if __name__ == "__main__":
    M = build(P)
    m = np.pad(M, 40); svg_out = vectorize(m, turdsize=60, alphamax=1.0, opttolerance=0.2)
    tag = P["out"]
    open(f"{D}/hhs_H_{tag}.svg", "w").write(svg_out)
    tiles = [np.array(Image.open(f"{HB}/ref/hhs/h_fused_bw.png").convert("L")) < 128]
    s = open(f"{HB}/ref/hhs/hhs_oldenglish_H_connected.svg").read(); a, b = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', s)[0]]
    tiles.append(crop(render_svg(s, int(a * 600 / b), 600)))
    s4 = open(f"{HB}/ref/hhs/hhs_H_v4.svg").read(); a, b = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', s4)[0]]
    tiles.append(crop(render_svg(s4, int(a * 600 / b), 600)))
    tiles.append(crop(render_svg(svg_out, m.shape[1], m.shape[0])))
    cell = 560; B = Image.new("L", (cell * 4, cell + 40), 255); d = ImageDraw.Draw(B)
    for i, (t, lab_) in enumerate(zip(tiles, ["1983 jersey (7-view fusion)", "v2 photo trace", "v4 (your markup)", f"{tag}: markup edits"])):
        t = t.astype(np.uint8) * 255; sc = 520 / t.shape[0]; t = cv2.resize(t, (int(t.shape[1] * sc), 520), interpolation=cv2.INTER_AREA)
        B.paste(Image.fromarray(255 - t), (i * cell + (cell - t.shape[1]) // 2, 10)); d.text((i * cell + 20, cell + 12), lab_, fill=0)
    B.save(f"{D}/hhs_H_{tag}_compare.png"); print("ok", M.shape)
