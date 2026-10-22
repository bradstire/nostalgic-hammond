"""Embroidery hats v3 (Brad 10-22: "check all designs against the embroidery specs").
Printful dad hat (Yupoong 6245CM): front 5.5 x 2.0 in, side/back 2.0 x 1.0 in (<= 5 characters per inch),
letters >= 0.25 in, details >= 0.05 in, threads from Printful's 15-colour palette only.
Pipeline per file: lettering as vector -> 300 dpi mask -> letters re-spaced so every gap >= 0.06 in ->
strokes thinner than 0.05 in rebuilt to 0.05 in on their own centreline -> checker (stroke, merge, counters) -> PNG."""
import sys, re, numpy as np, cv2
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/lib")
from PIL import Image, ImageDraw, ImageFont
from vtype import run, text_geom, svg_doc, affinity, unary_union
from embcheck import check, enforce_min_stroke, gap_events
from newsprint import render_svg, vectorize
import cairosvg, io
D = f"{HB}/hats"; DPI = 300
THREAD = {"white": "#FFFFFF", "black": "#000000", "red": "#CC3333", "purple": "#6B5294", "gold": "#FFCC00",
          "navy": "#333366", "maroon": "#660000", "old_gold": "#A67843", "royal": "#005397"}
GAP = int(0.06 * DPI)

def geom_mask(g, height_px=None, width_px=None):
    b = g.bounds; s = min(height_px / (b[3] - b[1]) if height_px else 1e9, width_px / (b[2] - b[0]) if width_px else 1e9)
    g = affinity.scale(g, s, s, origin=(0, 0)); b = g.bounds; g = affinity.translate(g, -b[0] + 4, -b[1] + 4)
    W, H = int(b[2] - b[0] + 8), int(b[3] - b[1] + 8)
    png = cairosvg.svg2png(bytestring=svg_doc([(g, "#000000")], W, H).encode(), output_width=W, output_height=H)
    a = np.array(Image.open(io.BytesIO(png)).convert("RGBA"))[..., 3] >= 128
    ys, xs = np.where(a); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def clusters(m):
    """Glyph clusters left->right: connected components merged when they overlap horizontally (i-dots, accents)."""
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    comps = sorted([(st[i, 0], st[i, 0] + st[i, 2], i) for i in range(1, n) if st[i, 4] > 20])
    groups = []
    for x0, x1, i in comps:
        if groups and x0 < groups[-1][1] - 0.35 * (x1 - x0): groups[-1][1] = max(groups[-1][1], x1); groups[-1][2].append(i)
        else: groups.append([x0, x1, [i]])
    return [(np.isin(lab, g[2])) for g in groups]

def _dist_ok(dil, ys, xs, dy, dx):
    yy, xx = ys + dy, xs + dx
    ok = (yy >= 0) & (yy < dil.shape[0]) & (xx >= 0) & (xx < dil.shape[1])
    return not dil[yy[ok], xx[ok]].any()

def separate_pieces(c, gap):
    """Inside one glyph cluster (i-dot, swash), move the smaller pieces away from the main piece until >= gap."""
    n, lab, st, cen = cv2.connectedComponentsWithStats(c.astype(np.uint8), 8)
    if n <= 2: return c
    main = 1 + int(np.argmax(st[1:, 4])); out = (lab == main)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * gap + 1, 2 * gap + 1))
    pad = gap * 4; out = np.pad(out, pad); dil = cv2.dilate(out.astype(np.uint8), k) > 0
    for i in range(1, n):
        if i == main or st[i, 4] < 20: continue
        ys, xs = np.where(np.pad(lab == i, pad)); v = cen[i] - cen[main]; v = v / (np.linalg.norm(v) + 1e-6)
        t = 0
        while not _dist_ok(dil, ys, xs, int(round(v[1] * t)), int(round(v[0] * t))) and t < pad: t += 1
        out[ys + int(round(v[1] * t)), xs + int(round(v[0] * t))] = True
    ys, xs = np.where(out); return out[ys.min():ys.max() + 1, xs.min():xs.max() + 1] if False else out[pad:-pad, pad:-pad] if t < pad else out

def respace(m, gap=GAP):
    """Re-lay glyph clusters left->right so each is >= gap (true distance) from everything placed before it."""
    cl = clusters(m); H = m.shape[0]; pad = gap * 4
    out = np.zeros((H + 2 * pad, m.shape[1] + gap * (len(cl) + 4) + 2 * pad), bool)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * gap + 1, 2 * gap + 1)); shift = 0
    for c in cl:
        c = separate_pieces(c, gap)
        ys, xs = np.where(c); ys = ys + pad; xs = xs + pad
        if c.shape[0] != m.shape[0]: ys = ys - (c.shape[0] - m.shape[0]) // 2
        dil = cv2.dilate(out.astype(np.uint8), k) > 0
        while not _dist_ok(dil, ys, xs, 0, shift): shift += 1
        out[ys, xs + shift] = True
    ys, xs = np.where(out); return out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def open_counters(m, r=2):
    """Widen enclosed counters/cut-outs by r px so they stay open when stitched (strokes re-checked after)."""
    inv = np.pad(~m, 1, constant_values=True).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 4)
    holes = (lab != lab[0, 0]) & (lab > 0); holes = holes[1:-1, 1:-1]
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return m & ~(cv2.dilate(holes.astype(np.uint8), k) > 0)

def enforce_gaps(m, gap=GAP):
    """Where two separate shapes come closer than `gap`, trim the smaller one back to `gap`."""
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    out = m.copy()
    for i in range(1, n):
        dt = cv2.distanceTransform((lab != i).astype(np.uint8), cv2.DIST_L2, 5)   # distance to component i
        for j in range(1, n):
            if j == i or st[j, 4] >= st[i, 4]: continue
            out[(lab == j) & (dt < gap)] = False
    return out

def bridge_gaps(m, gap=GAP):
    """Where two separate shapes come closer than `gap`, JOIN them (fill the narrow white between) —
    right for cartoon art where a sliver cut is accidental (a hand nearly severed from its arm)."""
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    out = m.copy(); r = gap / 2 + 1
    dts = {i: cv2.distanceTransform((lab != i).astype(np.uint8), cv2.DIST_L2, 5) for i in range(1, n) if st[i, 4] > 1500}
    keys = list(dts)
    for a_ in range(len(keys)):
        for b_ in range(a_ + 1, len(keys)):
            i, j = keys[a_], keys[b_]
            if dts[i][lab == j].min() < gap:
                out |= (dts[i] < r) & (dts[j] < r)
    return out

def prep(m):
    """final-size mask -> stitch-safe: strokes >= 0.05in, counters opened, pieces and letters >= 0.06in apart."""
    m = enforce_min_stroke(m, 0.05); m = open_counters(m, 2); m = enforce_min_stroke(m, 0.05)
    return m

def fit(m, w_in=None, h_in=None):
    s = min(w_in * DPI / m.shape[1] if w_in else 1e9, h_in * DPI / m.shape[0] if h_in else 1e9)
    return cv2.resize(m.astype(np.float32), (int(m.shape[1] * s), int(m.shape[0] * s)), interpolation=cv2.INTER_AREA) > 0.5

def vstack(parts, gap_in):
    W = max(p.shape[1] for p in parts); g = int(gap_in * DPI); H = sum(p.shape[0] for p in parts) + g * (len(parts) - 1)
    out = np.zeros((H, W), bool); y = 0
    for p in parts:
        x = (W - p.shape[1]) // 2; out[y:y + p.shape[0], x:x + p.shape[1]] |= p; y += p.shape[0] + g
    return out

def smooth(m):
    m = np.pad(m, 12); m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2) > 0.5
    svg = vectorize(m, turdsize=10, alphamax=1.0, opttolerance=0.3)
    return render_svg(svg, m.shape[1], m.shape[0])

def finish(m, thread, name, placement="front", text=None):
    m = smooth(m)
    r = check(m, placement, text)
    rgba = np.zeros((*m.shape, 4), np.uint8); c = THREAD[thread]
    rgba[m, :3] = [int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)]; rgba[m, 3] = 255
    Image.fromarray(rgba, "RGBA").save(f"{D}/{name}.png", dpi=(DPI, DPI))
    flag = "PASS" if r["pass"] else "CHECK"
    print(f"{flag:5s} {name:34s} {r['size_in'][0]:.2f}x{r['size_in'][1]:.2f}in  min line {r['min_line_in']}in  "
          f"merges {r['gaps_merging']}  counters closing {r['holes_closing']}  {thread} {c}" + (f"  text {r['text']}" if text else ""))
    return m, r

def textline(text, font, var=None, tr=0.0, h_in=None, w_in=None, cap_px=900):
    g = run([(text, font, cap_px, var, tr, 0)])
    if h_in: m = geom_mask(g, height_px=int(h_in * DPI))
    else:
        m0 = geom_mask(g, height_px=600); m = fit(m0, w_in=w_in)
    return respace(prep(m), GAP)

results = {}
if __name__ == "__main__":
    # 1) HUB CITY — authentic headline letters (Real-ESRGAN of the 1966 ad), re-spaced, thin parts rebuilt
    hc = cv2.imread(f"{HB}/hubcity/sr_gray_3150.png", 0)
    hb_ = hc[65:241, 89:2615] < 140; hb_[150 - 65:, 2572 - 89:] = False
    ys, xs = np.where(hb_); head = hb_[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cols = head.any(axis=0); gaps = []; run_ = 0
    for x in range(len(cols)):
        if not cols[x]: run_ += 1
        else:
            if run_ > 25: gaps.append((x - run_, x))
            run_ = 0
    cut = sorted(gaps, key=lambda g: abs((g[0] + g[1]) / 2 - head.shape[1] * 0.42))[0]
    l1, l2 = head[:, :cut[0]], head[:, cut[1]:]
    crop = lambda a: a[np.where(a.any(1))[0].min():np.where(a.any(1))[0].max() + 1, np.where(a.any(0))[0].min():np.where(a.any(0))[0].max() + 1]
    l1, l2 = crop(l1), crop(l2)
    sc_ = 0.40 * DPI / l2.shape[0]                                    # 0.40in cap height
    l1 = respace(prep(fit(l1, h_in=0.42)), GAP); l2 = respace(prep(fit(l2, h_in=0.42)), GAP)
    results["hubcity"] = finish(vstack([l1, l2], 0.12), "black", "hat_hubcity_black", text=[("HUB CITY", 0.42, l1.shape[1] / DPI), ("DRAG RACEWAY", 0.42, l2.shape[1] / DPI)])

    # 2) CAMELOT — v3 letters (Old English swash C + Grenze Gotisch Black), solid fill (inline can't stitch at this size)
    G, GV, MC = "GrenzeGotisch[wght].ttf", [900], "ManufacturingConsent-Regular.ttf"
    cam = fit(geom_mask(run([("C", MC, 1180, None, 0, 0.02), ("amelot", G, 1000, GV, 0.05, 0)]), height_px=600), w_in=3.8)
    mus = fit(geom_mask(run([("Music", G, 1000, GV, 0.05, 0)]), height_px=600), h_in=cam.shape[0] / DPI * 0.97)
    cam = respace(prep(cam), GAP); mus = respace(prep(mus), GAP)
    camm = vstack([cam, mus], 0.07)
    if camm.shape[0] > 1.95 * DPI: camm = fit(camm, h_in=1.95)
    results["camelot_r"] = finish(camm, "red", "hat_camelot_red")
    results["camelot_w"] = finish(camm, "white", "hat_camelot_white")

    # 3) MISSISSIPPI BRITCHES — logotype (Inter, Helvetica Medium match), white thread (no cream in the palette)
    INTER, IV = "Inter[opsz,wght].ttf", [32, 700]
    l1 = textline("mississippi", INTER, IV, 0.0, h_in=None, w_in=3.6)
    l2 = textline("britches", INTER, IV, 0.0, h_in=l1.shape[0] / DPI * 0.92)
    results["britches"] = finish(vstack([l1, l2], 0.09), "white", "hat_britches_white", text=[("mississippi", 0.26, 3.6), ("britches", 0.26, l2.shape[1] / DPI)])

    # 4) ALBERT SPEED'S — sign lettering, 3 lines
    AR, AV = "Archivo[wdth,wght].ttf", [800, 82]   # axes order = (Weight, Width)
    a1 = textline("ALBERT", AR, AV, 0.06, h_in=0.36); a2 = textline("SPEED'S", AR, AV, 0.04, h_in=0.56)
    a3 = textline("RESTAURANT", AR, AV, 0.06, h_in=0.34)
    if a3.shape[1] > 3.9 * DPI: a3 = fit(a3, w_in=3.9)
    sp = vstack([a1, a2, a3], 0.08)
    results["speeds"] = finish(sp, "red", "hat_speeds_red", text=[("ALBERT", 0.36, a1.shape[1] / DPI), ("SPEED'S", 0.56, a2.shape[1] / DPI), ("RESTAURANT", a3.shape[0] / DPI, a3.shape[1] / DPI)])

    # 5) HHS — v3 Old English H (Manufacturing Consent, leaned to the 1983 jersey)
    svg = open(f"{HB}/ref/hhs/hhs_H_v3.svg").read(); w0, h0 = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', svg)[0]]
    hh = int(1.9 * DPI); Hm = render_svg(svg, int(w0 * hh / h0), hh); ys, xs = np.where(Hm); Hm = Hm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Hm = prep(Hm); Hm = separate_pieces(np.pad(Hm, 40), GAP); ys, xs = np.where(Hm); Hm = Hm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    results["hhs_p"] = finish(Hm, "purple", "hat_hhs_oldenglishH_purple")
    results["hhs_g"] = finish(Hm, "gold", "hat_hhs_oldenglishH_gold")

    # 6) CULPEPPER duck (front) — v3 duck with opened face/shirt/arm, built at embroidery weight in culpepper/build.py
    dk = np.array(Image.open(f"{HB}/culpepper/culpepper_duck_hat_embroidery.png"))[..., 3] > 127
    ys, xs = np.where(dk); dk = dk[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    dk = bridge_gaps(enforce_min_stroke(dk, 0.05))   # stroke rebuild + join sliver gaps (counter-opening/trimming damaged the face)
    results["duck"] = finish(dk, "black", "hat_culpepper_duck_black")

    # 7) CULPEPPER back — single arched word on the 2.0 x 1.0 in back panel, <= 5 characters per inch.
    #    Condensed gothic like the 1968 ad headline (Oswald 650). ALTERNATE ONLY: at 0.28in the P/R bowls are ~0.04in and will fill when stitched; the front lockup (#8) is the primary text solution. Laid out at 4x along the arc, each letter >= 0.06in
    #    (true distance) from the previous one, spacing widened to ~1.9in, then downsampled and stitch-proofed.
    JOST = "Jost[wght].ttf"
    X = 4; f = ImageFont.truetype(f"{HB}/../fonts/Oswald[wght].ttf", 400 * X); f.set_variation_by_axes([650])
    cap = int(0.28 * DPI) * X; R = int(4.2 * DPI) * X
    glyphs = []
    for ch in "CULPEPPER":
        im = Image.new("L", (700 * X, 700 * X), 0); ImageDraw.Draw(im).text((100 * X, 600 * X), ch, font=f, fill=255, anchor="ls")
        a = np.array(im) > 127; ys, xs = np.where(a); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        a = cv2.resize(a.astype(np.float32), (max(1, int(a.shape[1] * cap / a.shape[0])), cap), interpolation=cv2.INTER_AREA) > 0.5
        glyphs.append(np.pad(a, 20 * X))
    S = int(2 * (R + cap * 2)); cx = cy = S // 2
    def put(g, th):
        rc = R + cap / 2; gx, gy = cx + rc * np.sin(th), cy - rc * np.cos(th)
        rot = np.array(Image.fromarray((g * 255).astype(np.uint8)).rotate(-np.degrees(th), expand=True, resample=Image.BICUBIC)) > 127
        x0, y0 = int(round(gx - rot.shape[1] / 2)), int(round(gy - rot.shape[0] / 2))
        ys, xs = np.where(rot); return ys + y0, xs + x0
    def layout(gap):
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * gap * X + 1, 2 * gap * X + 1))
        canvas = np.zeros((S, S), bool); th = 0.0; thetas = []
        for g in glyphs:
            dil = cv2.dilate(canvas.astype(np.uint8), k) > 0
            while True:
                ys, xs = put(g, th)
                if not dil[ys, xs].any(): break
                th += 0.001
            canvas[ys, xs] = True; thetas.append(th); th += (g.shape[1] - 40 * X) / R * 0.5
        off = -(thetas[0] + thetas[-1]) / 2; canvas = np.zeros((S, S), bool)
        for g, t in zip(glyphs, thetas):
            ys, xs = put(g, t + off); canvas[ys, xs] = True
        ys, xs = np.where(canvas); c = canvas[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        return cv2.resize(c.astype(np.float32), (c.shape[1] // X, c.shape[0] // X), interpolation=cv2.INTER_AREA) > 0.5
    gap = GAP + 3; back = layout(gap)
    while back.shape[1] < 1.86 * DPI: gap += 3; back = layout(gap)      # ~1.9in wide: <= 5 cpi and inside 2.0in
    back = enforce_min_stroke(back, 0.05); back = open_counters(back, 2); back = enforce_min_stroke(back, 0.05)
    results["back"] = finish(back, "black", "hat_culpepper_back_black", "back", text=[("CULPEPPER", 0.28, back.shape[1] / DPI)])

    # 8) CULPEPPER front lockup (alternate): duck + CULPEPPER / BODY & PAINT beside it, all on the 5.5 x 2.0 front
    t1 = textline("CULPEPPER", JOST, [700], 0.08, h_in=0.40)
    t2 = textline("BODY & PAINT", JOST, [560], 0.12, h_in=0.34)
    t2 = fit(t2, w_in=min(t2.shape[1] / DPI, t1.shape[1] / DPI)) if t2.shape[1] > t1.shape[1] else t2
    txt = vstack([t1, t2], 0.10)
    dks = dk
    H = max(dks.shape[0], txt.shape[0]); lock = np.zeros((H, dks.shape[1] + int(0.22 * DPI) + txt.shape[1]), bool)
    lock[H - dks.shape[0]:, :dks.shape[1]] = dks
    ty = (H - txt.shape[0]) // 2; lock[ty:ty + txt.shape[0], dks.shape[1] + int(0.22 * DPI):] = txt
    results["lockup"] = finish(lock, "black", "hat_culpepper_front_lockup_black", text=[("CULPEPPER", t1.shape[0] / DPI, t1.shape[1] / DPI), ("BODY & PAINT", t2.shape[0] / DPI, t2.shape[1] / DPI)])
