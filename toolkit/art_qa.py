#!/usr/bin/env python3
"""NT art gate (S9): automated print-master QA for Nostalgic Towns art.

Usage:  python3 art_qa.py MASTER.png --width-in 10 [--out DIR] [--name NAME]

Checks, all measured at final print size (ppi = master width px / print width in):
  1. COUNTERS   enclosed negative space narrower than 0.025 in (0.64 mm), or clogged (< 0.35 x the
                surrounding stroke width)                                               -> FAIL
  2. GAPS       two separate shapes closer than 6 % of the smaller one's height, clamped to
                0.012-0.03 in (letters crowding/touching; scales with type size)        -> FAIL
  3. LEVEL      text lines whose baseline tilts > 0.35 deg with a visible end-to-end rise
                (> 0.015 in or 5 % of letter height), or baseline jitter > 3 %          -> FAIL
  4. EDGES      traced wobble, two measures per text line (calibrated 10-25: Didi-Wa v2 =
                success comp): curvature inflections per inch > 3.4 + 0.25/cap_in, or
                curvature peaks per cap-height of outline > 7.5 (lumps on curved strokes) -> FAIL
                Edge tests are style-sensitive (script vs slab): every traced case in the
                calibration set trips EDGES or LEVEL, but part B visual sign-off still rules.
  5. STROKES    linework thinner than 0.015 in (HQ's break-up floor; FAIL if > 1 % of linework). Target is the
                published POD guidance - Gooten: lines/text no narrower than 10 px @ 300 dpi (0.033 in) and
                fonts >= 10 pt; under 0.03 in is a WARN to look at (contrast matters: L20's thin mint outline)
Knockout lettering (letters cut out of an ink panel) is read as text too.
Halftone photo screens (fields of tiny dots) are detected and excluded from 1-5.
--exempt x0,y0,x1,y1:reason  (repeatable) excludes a hand-drawn illustration, display lockup or a
deliberate design tilt from LEVEL/EDGES only; a reason starting 'LEVEL only:' waives LEVEL but keeps EDGES.
Every exemption is printed in the report and overlay.
--typeset x0,y0,x1,y1:Font   (repeatable) declares a line rendered directly from a font (never screened,
traced or textured); EDGES is skipped there (a font outline is clean by construction; bracketed serifs
otherwise read as wobble). Everything else still applies. The build script that renders it is the record.
A sidecar MASTER.prov.json {"exempt": [[box, reason]], "typeset": [[box, font]], "redrawn": [[box, how]]} is read
automatically. "redrawn" marks shapes deliberately moved or rebuilt (a levelled line, rebuilt sign geometry, redrawn
rules): SURVIVAL skips them and every one is printed as a WARN for the eye check. Declarations are the record of
what changed; each typeset/redrawn box must cover the OLD shapes it replaces as well as the new ones.
--compare PREVIOUS.png        (rebuilds; REQUIRED for any changed master) SURVIVAL check: fails if a shape of the
previous master was lost, split into pieces or shrank > 20 % without a re-set/redraw declared over it (a cleanup
that passes every metric but eats letter parts - 10-25 socks - is caught here). Same canvas size required;
otherwise skipped with a WARN. Declared TYPESET boxes are verified either way: inside the canvas, holding ink,
and (with --compare) at least half the previous master's ink in that box (10-25 Galaxy natural lost its
re-set COURTESY PASS line behind its own declaration).
Writes NAME_qa.json + NAME_qa.png (overlay: red counters, magenta gaps, blue thin strokes,
green/red baselines with angle, orange boxes = wobbly lines).
SOURCE (R21): when the sidecar carries rules ["R21"], every typeset line must give its R21 reason or FAIL.
TRACED-TILT (L47): traced lettering inside an exemption still fails a whole-line tilt > 1 deg (visible rise) unless the
reason declares a deliberate angle. Part B for traces: toolkit/trace_overlay.py (master outline on the source).
Exit code 0 = PASS, 1 = FAIL. WARNs never fail the gate but must be looked at.
Visual sign-off (S9 part B) is still required: the overlay + print-zoom tiles vs the source.
"""
import argparse, json, math, os, sys
import numpy as np
import cv2
from scipy import ndimage
from scipy.ndimage import gaussian_filter1d
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import find_peaks

LIMITS = dict(counter_in=0.025, counter_rel=0.35, gap_in=0.03, gap_min_in=0.012, gap_rel=0.06, tilt_deg=0.35, jitter=0.03,
              wobble_a=3.4, wobble_b=0.25, peaks_cap_max=7.5, stroke_fail_in=0.015, stroke_warn_in=0.03)
# calibrated 2026-10-25 against Didi-Wa v2 (success comp), Fiesta v3, Magnolia v3 (pass) vs the
# traced Magnolia/Fiesta/Didi-Wa originals (fail); see NT_PRODUCT_STANDARDS S9.
def wobble_limit(cap_in):
    # clean type has a fixed number of structural curve changes per letter, so the per-inch count
    # rises as type gets smaller; trace wobble is ~constant per print inch. limit = a + b / cap.
    return LIMITS['wobble_a'] + LIMITS['wobble_b'] / max(cap_in, 0.05)


def ink_layers(a):
    op = a[..., 3] > 128
    cols, counts = np.unique(a[op][:, :3].reshape(-1, 3), axis=0, return_counts=True)
    keep = cols[counts > max(200, 0.004 * op.sum())]
    layers = []
    for c in keep:
        m = op & (np.abs(a[..., :3].astype(int) - c.astype(int)).sum(2) < 40)
        if m.sum() > 0:
            layers.append((tuple(int(v) for v in c), m))
    if not layers:
        layers = [((0, 0, 0), op)]
    return op, layers


def halftone_zone(mask, ppi):
    """Photo screens: large areas with very high edge density (dot fields or connected screen mesh).
    Text lines are thin strips and never reach the size test, so small type stays checked."""
    er = ndimage.binary_erosion(mask)
    edge = (mask & ~er).astype(float)
    win = int(0.12 * ppi) | 1
    dens = ndimage.uniform_filter(edge, size=win)
    ink = ndimage.uniform_filter(mask.astype(float), size=win)
    hot = (dens > 0.14) & (ink > 0.08)
    hot = ndimage.binary_closing(hot, iterations=int(0.05 * ppi) + 1)
    zl, zn = ndimage.label(hot)
    zone = np.zeros_like(mask)
    for k, sl in enumerate(ndimage.find_objects(zl), 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if min(h, w) >= 0.45 * ppi and (zl[sl] == k).sum() >= (0.7 * ppi) ** 2:
            zone[sl] |= zl[sl] == k
    zone = ndimage.binary_fill_holes(ndimage.binary_dilation(zone, iterations=int(0.03 * ppi) + 1))
    # a photo sits in a rectangle: extend each zone that fills most of its box to the whole box
    # (pale areas of a screened photo - sky, wires - are sparse but still photo)
    zl, zn = ndimage.label(zone)
    for k, sl in enumerate(ndimage.find_objects(zl), 1):
        if (zl[sl] == k).mean() > 0.5:
            zone[sl] = True
    # ...and to a drawn frame (thin rectangular outline) that encloses it: the frame is the photo's edge
    if zone.any():
        fl, fn = ndimage.label(mask)
        for k, sl in enumerate(ndimage.find_objects(fl), 1):
            h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
            if h < ppi or w < ppi:
                continue
            reg = fl[sl] == k
            if reg.mean() < 0.12 and zone[sl].mean() > 0.4:
                zone[sl[0].start + 1:sl[0].stop - 1, sl[1].start + 1:sl[1].stop - 1] = True
    return zone


def check_counters(m, ppi, excl):
    holes = ndimage.binary_fill_holes(m) & ~m
    lab, n = ndimage.label(holes)
    dt = ndimage.distance_transform_edt(holes)
    out = []
    if n == 0:
        return out, holes & False
    mx = ndimage.maximum(dt, lab, range(1, n + 1))
    bad = np.zeros_like(m)
    floor_px = LIMITS['counter_in'] * ppi
    ink_dt = ndimage.distance_transform_edt(m)
    objs = ndimage.find_objects(lab)
    for i, w in enumerate(mx, 1):
        width = 2 * w
        sl = objs[i - 1]
        if sl is None:
            continue
        reg = lab[sl] == i
        if reg.sum() < 4 or excl[sl][reg].mean() > 0.5:
            continue
        # local stroke width = 2 x the deepest ink within one counter-width ring around the hole
        pad = int(max(width, 0.04 * ppi)) + 2
        y0, y1 = max(0, sl[0].start - pad), min(m.shape[0], sl[0].stop + pad)
        x0, x1 = max(0, sl[1].start - pad), min(m.shape[1], sl[1].stop + pad)
        hole = np.zeros((y1 - y0, x1 - x0), bool)
        hole[sl[0].start - y0:sl[0].stop - y0, sl[1].start - x0:sl[1].stop - x0] = reg
        ring = ndimage.binary_dilation(hole, iterations=pad) & m[y0:y1, x0:x1]
        stroke = 2 * float(np.percentile(ink_dt[y0:y1, x0:x1][ring], 90)) if ring.any() else 0
        why = None
        if width < floor_px:
            why = 'tiny'
        elif stroke > 0 and width < LIMITS['counter_rel'] * stroke and reg.sum() < (0.25 * ppi) ** 2:
            why = 'clogged'
        if why:
            bad[sl] |= reg
            out.append(dict(x=int(sl[1].start), y=int(sl[0].start), width_in=round(width / ppi, 3),
                            stroke_in=round(stroke / ppi, 3), why=why))
    return out, bad


def check_gaps(m, ppi, excl, min_area):
    lab, n = ndimage.label(m)
    if n < 2:
        return [], np.zeros_like(m)
    objs = ndimage.find_objects(lab)
    areas = ndimage.sum(m, lab, range(1, n + 1))
    big = np.isin(lab, np.nonzero(areas >= min_area)[0] + 1)
    lab = np.where(big, lab, 0)
    r = LIMITS['gap_in'] * ppi / 2
    dt, (iy, ix) = ndimage.distance_transform_edt(lab == 0, return_indices=True)
    near = lab[iy, ix]
    band = (dt <= r) & (lab == 0) & ~excl
    pairs = {}
    for a_, b_, d_, bb in ((near[:, 1:], near[:, :-1], np.minimum(dt[:, 1:], dt[:, :-1]), band[:, 1:] & band[:, :-1]),
                           (near[1:, :], near[:-1, :], np.minimum(dt[1:, :], dt[:-1, :]), band[1:, :] & band[:-1, :])):
        sel = bb & (a_ != b_) & (a_ > 0) & (b_ > 0)
        ys, xs = np.nonzero(sel)
        for y, x, p_, q_, d in zip(ys, xs, a_[sel], b_[sel], d_[sel]):
            k = (min(p_, q_), max(p_, q_))
            if k not in pairs or d < pairs[k][0]:
                pairs[k] = (float(d), int(x), int(y))
    out = []; bad = np.zeros_like(m)
    for (p_, q_), (d, x, y) in pairs.items():
        hp = objs[p_ - 1][0].stop - objs[p_ - 1][0].start; hq = objs[q_ - 1][0].stop - objs[q_ - 1][0].start
        floor_in = min(LIMITS['gap_in'], max(LIMITS['gap_min_in'], LIMITS['gap_rel'] * min(hp, hq) / ppi))
        gap_in = 2 * d / ppi
        if gap_in < floor_in:
            out.append(dict(x=x, y=y, gap_in=round(gap_in, 3), floor_in=round(floor_in, 3)))
            bad[max(0, y - 2):y + 3, max(0, x - 2):x + 3] = True
    return out, bad


def text_lines(m, ppi, excl, exempt=()):
    lab, n = ndimage.label(m)
    comps = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (0.06 * ppi <= h <= 2.5 * ppi):
            continue
        if w > 6 * h or w < 0.08 * h:
            continue
        if any(sl[1].start >= b[0] and sl[0].start >= b[1] and sl[1].stop <= b[2] and sl[0].stop <= b[3]
               for b, _ in exempt):
            continue                     # inside a declared exemption box
        reg = lab[sl] == i
        if excl[sl][reg].mean() > 0.3:
            continue
        fill = reg.mean()
        if fill < 0.12:                  # frames, rules, open outlines
            continue
        holes = ndimage.binary_fill_holes(reg) & ~reg
        if holes.any():
            hl, hn = ndimage.label(holes)
            if hn >= 3 and (ndimage.sum(holes, hl, range(1, hn + 1)) > (0.03 * ppi) ** 2).sum() >= 3:
                continue                 # a panel with cut-out letters, read separately as knockout text
        comps.append(dict(id=i, x0=sl[1].start, x1=sl[1].stop, y0=sl[0].start, y1=sl[0].stop, h=h,
                          cx=(sl[1].start + sl[1].stop) / 2, cy=(sl[0].start + sl[0].stop) / 2))
    comps.sort(key=lambda c: c['cx'])
    used = set(); lines = []
    for c in sorted(comps, key=lambda c: -c['h']):
        if c['id'] in used:
            continue
        line = [c]; used.add(c['id'])
        grow = True
        while grow:
            grow = False
            med_h = np.median([k['h'] for k in line])
            xs = [k['cx'] for k in line]
            for k in comps:
                if k['id'] in used:
                    continue
                if not (0.55 * med_h <= k['h'] <= 1.6 * med_h):
                    continue
                # vertical overlap with the nearest member, and horizontal adjacency
                nearest = min(line, key=lambda q: abs(q['cx'] - k['cx']))
                ov = min(nearest['y1'], k['y1']) - max(nearest['y0'], k['y0'])
                if ov < 0.5 * min(nearest['h'], k['h']):
                    continue
                if abs(nearest['cx'] - k['cx']) > 2.2 * med_h:
                    continue
                line.append(k); used.add(k['id']); grow = True
        if len(line) >= 3:
            lines.append(sorted(line, key=lambda q: q['cx']))
    return lab, lines


def fit_baseline(line):
    """Robust baseline: punctuation/quotes (short shapes) are left out, a Theil-Sen fit takes the slope (immune to a
    dipping $, J or Q), then shapes off the line by > 8 % of letter height drop out and the fit is refined."""
    h90 = np.percentile([c['h'] for c in line], 90)
    pts = [c for c in line if c['h'] >= 0.6 * h90] or line
    x = np.array([c['cx'] for c in pts], float)
    yb = np.array([c['y1'] for c in pts], float)
    h = np.median([c['h'] for c in pts])
    if len(x) >= 3:
        sl = [(yb[j] - yb[i]) / (x[j] - x[i]) for i in range(len(x)) for j in range(i + 1, len(x)) if x[j] != x[i]]
        m = float(np.median(sl)) if sl else 0.0
        b = float(np.median(yb - m * x))
        keep = np.abs(yb - (m * x + b)) < 0.08 * h
        if keep.sum() >= 2:
            p = np.polyfit(x[keep], yb[keep], 1)
        else:
            p = np.array([m, b])
    else:
        p = np.polyfit(x, yb, 1); keep = np.ones(len(x), bool)
    res = (yb - np.polyval(p, x))[keep] if keep.any() else np.array([0.0])
    ang = math.degrees(math.atan(p[0]))
    jitter = float(1.4826 * np.median(np.abs(res - np.median(res))) / h)
    return ang, jitter, p, h, int(keep.sum())


def subpixel_contours(region_mask, ppi):
    """Outlines at sub-pixel precision (0.5 level of a lightly blurred mask): no pixel-staircase artefacts."""
    from skimage.measure import find_contours
    from scipy.ndimage import gaussian_filter
    ys, xs = np.nonzero(region_mask)
    if len(ys) == 0:
        return []
    y0, y1 = max(0, ys.min() - 4), ys.max() + 5; x0, x1 = max(0, xs.min() - 4), xs.max() + 5
    f = gaussian_filter(region_mask[y0:y1, x0:x1].astype(float), 1.0)
    out = []
    for c in find_contours(f, 0.5):
        if len(c) < 30:
            continue
        p = c[:, ::-1]  # (x, y)
        area = 0.5 * abs(np.dot(p[:, 0], np.roll(p[:, 1], 1)) - np.dot(p[:, 1], np.roll(p[:, 0], 1)))
        if area < (0.02 * ppi) ** 2:
            continue
        out.append(p)
    return out


def _curvature(p, ppi):
    seg = np.hypot(*np.diff(np.vstack([p, p[:1]]), axis=0).T)
    L = seg.sum()
    s = np.concatenate([[0], np.cumsum(seg)]); t = np.arange(0, L, 1.0)
    q = np.stack([np.interp(t, s, np.append(p[:, 0], p[0, 0])), np.interp(t, s, np.append(p[:, 1], p[0, 1]))], 1)
    s1 = max(1.0, 0.006 * ppi)
    q = np.stack([gaussian_filter1d(q[:, 0], s1, mode='wrap'), gaussian_filter1d(q[:, 1], s1, mode='wrap')], 1)
    d = np.gradient(q, axis=0); dd = np.gradient(d, axis=0)
    k = (d[:, 0] * dd[:, 1] - d[:, 1] * dd[:, 0]) / np.maximum((d ** 2).sum(1) ** 1.5, 1e-9)
    return k, L


def inflections_per_in(region_mask, ppi):
    total_len = 0.0; infl = 0
    s2 = max(2.0, 0.012 * ppi); kmin = 1.0 / (0.30 * ppi)
    for p in subpixel_contours(region_mask, ppi):
        k, L = _curvature(p, ppi); total_len += L
        k = gaussian_filter1d(k, s2, mode='wrap')
        sgn = np.where(k > kmin, 1, np.where(k < -kmin, -1, 0))
        nz = sgn[sgn != 0]
        if len(nz) > 1:
            infl += int((nz != np.roll(nz, 1)).sum())
    return infl / max(total_len / ppi, 1e-6), total_len / ppi


def curvature_peaks_per_in(region_mask, ppi):
    L_tot = 0.0; pk = 0
    s2 = max(2.0, 0.010 * ppi); prom = 1.0 / (0.12 * ppi)
    for p in subpixel_contours(region_mask, ppi):
        k, L = _curvature(p, ppi); L_tot += L
        k = gaussian_filter1d(k, s2, mode='wrap')
        kk = np.concatenate([k, k[:50]])
        a, _ = find_peaks(kk, prominence=prom, distance=int(s2 * 2))
        b, _ = find_peaks(-kk, prominence=prom, distance=int(s2 * 2))
        pk += int((a < len(k)).sum() + (b < len(k)).sum())
    return pk / max(L_tot / ppi, 1e-6)


def thin_strokes(m, ppi, excl):
    from skimage.morphology import skeletonize
    sk = skeletonize(m)
    dt = ndimage.distance_transform_edt(m)
    w = 2 * dt
    # ignore skeleton tips (strokes taper to their ends)
    nb = ndimage.convolve(sk.astype(int), np.ones((3, 3), int), mode='constant') - 1
    tips = sk & (nb <= 1)
    tipzone = ndimage.binary_dilation(tips, iterations=int(0.04 * ppi) + 1)
    valid = sk & ~tipzone & ~excl
    tot = int(valid.sum())
    fail = valid & (w < LIMITS['stroke_fail_in'] * ppi)
    warn = valid & (w < LIMITS['stroke_warn_in'] * ppi) & ~fail
    return int(fail.sum()), int(warn.sum()), tot, fail, warn


def survival(prev_path, cur_rgba, ppi, declared):
    """Per ink colour: every shape of the previous master must still be there (>= 80 % area, not split).
    A shape counts as declared (re-set / redrawn) when >= 80 % of its pixels fall inside a declared box.
    Pieces smaller than 0.01 in square (single-pixel corner tips) don't count as a split."""
    pa = np.asarray(Image.open(prev_path).convert('RGBA'))
    if pa.shape[:2] != cur_rgba.shape[:2]:
        return None
    H, W = pa.shape[:2]
    dmask = np.zeros((H, W), bool)
    for b in declared:
        x0, y0, x1, y1 = [int(v) for v in b]
        dmask[max(0, y0 - 5):max(0, y1 + 5), max(0, x0 - 5):max(0, x1 + 5)] = True
    speck = (0.01 * ppi) ** 2
    _, players = ink_layers(pa)
    bad = []
    for col, pm in players:
        cm = (cur_rgba[..., 3] > 128) & (np.abs(cur_rgba[..., :3].astype(int) - np.array(col)).sum(2) < 40)
        lab, n = ndimage.label(pm)
        for i, sl in enumerate(ndimage.find_objects(lab), 1):
            reg = lab[sl] == i
            a0 = reg.sum()
            if a0 < (0.03 * ppi) ** 2 or a0 > 0.25 * pm.size:     # skip specks and full-bleed grounds
                continue
            if (dmask[sl] & reg).sum() >= 0.8 * a0:
                continue                  # inside a declared re-set / redraw
            y0, x0 = sl[0].start, sl[1].start
            now = cm[sl] & reg
            a1 = now.sum()
            pl, pn = ndimage.label(now)
            pieces = int(sum(1 for j in range(1, pn + 1) if (pl == j).sum() >= speck))
            if a1 < 0.8 * a0 or pieces > 1:
                bad.append(dict(layer=str(col), x=int(x0), y=int(y0), area_kept=round(float(a1) / a0, 2), pieces=pieces))
    return bad


def run(path, width_in, out_dir, name=None, exempt=(), typeset=(), compare=None, redrawn=()):
    side = os.path.splitext(path)[0] + '.prov.json'
    if os.path.exists(side):
        pv = json.load(open(side))
        exempt = list(exempt) + [(tuple(b), r) for b, r in pv.get('exempt', [])]
        typeset = list(typeset) + [(tuple(b), f) for b, f in pv.get('typeset', [])]
        redrawn = list(redrawn) + [(tuple(b), h) for b, h in pv.get('redrawn', [])]
        r21 = 'R21' in pv.get('rules', [])
    else:
        r21 = False
    name = name or os.path.splitext(os.path.basename(path))[0]
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im)
    H, W = a.shape[:2]
    ppi = W / width_in
    op, layers = ink_layers(a)
    excl = halftone_zone(op, ppi)
    rep = dict(file=os.path.basename(path), print_width_in=width_in, ppi=round(ppi, 1),
               layers=[c for c, _ in layers], halftone_area_pct=round(100 * excl.mean() / max(op.mean(), 1e-9), 1),
               counters=[], gaps=[], lines=[], strokes={}, verdict='PASS', fails=[], warns=[],
               exemptions=[dict(box=list(b), reason=r) for b, r in exempt],
               typeset=[dict(box=list(b), font=f) for b, f in typeset],
               redrawn=[dict(box=list(b), how=h) for b, h in redrawn])
    over_red = np.zeros((H, W), bool); over_mag = np.zeros((H, W), bool)
    over_blue = np.zeros((H, W), bool); over_lb = np.zeros((H, W), bool)
    min_area = (0.025 * ppi) ** 2
    # substrate layers (a card/panel colour the other inks sit on) have the ink as their 'negative space':
    # their counters/gaps are the ink strokes, already judged by STROKES, so they are skipped here
    substrate = set()
    if len(layers) > 1:
        for col, m in layers:
            others = op & ~m
            if others.any() and (ndimage.binary_fill_holes(m) & others).sum() > 0.85 * others.sum():
                substrate.add(col)
    rep['substrate_layers'] = [str(c) for c in substrate]
    # counters + gaps per ink layer (negative space inside a colour), and for all ink vs ground
    for col, m in [(c, m) for c, m in layers if c not in substrate] + ([('all', op)] if len(layers) > 1 else []):
        cs, bad = check_counters(m, ppi, excl)
        for c in cs:
            c['layer'] = str(col)
        rep['counters'] += cs; over_red |= bad
        gs, gb = check_gaps(m, ppi, excl, min_area)
        for g in gs:
            g['layer'] = str(col)
        rep['gaps'] += gs; over_mag |= gb
    # dedupe by position
    def dedupe(items):
        seen = set(); out = []
        for it in items:
            k = (it['x'] // 8, it['y'] // 8)
            if k not in seen:
                seen.add(k); out.append(it)
        return out
    rep['counters'] = dedupe(rep['counters']); rep['gaps'] = dedupe(rep['gaps'])
    # text lines: level + edges
    line_draw = []
    sources = []
    for col, m in layers:
        sources.append((str(col), m))
        ko = ndimage.binary_fill_holes(m) & ~m      # knockout shapes cut out of this ink
        if ko.sum() > (0.1 * ppi) ** 2:
            sources.append((f'knockout in {col}', ko))
    for col, m in sources:
        lab, lines = text_lines(m, ppi, excl, exempt)
        for ln in lines:
            ang, jit, p, h, nk = fit_baseline(ln)
            reg = np.isin(lab, [c['id'] for c in ln])
            ipi, plen = inflections_per_in(reg, ppi)
            ppc = curvature_peaks_per_in(reg, ppi) * h / ppi
            x0 = min(c['x0'] for c in ln); x1 = max(c['x1'] for c in ln)
            y0 = min(c['y0'] for c in ln); y1 = max(c['y1'] for c in ln)
            entry = dict(layer=str(col), box=[int(x0), int(y0), int(x1), int(y1)], letters=len(ln),
                         cap_in=round(h / ppi, 3), tilt_deg=round(ang, 2), jitter=round(jit, 3),
                         inflect_per_in=round(ipi, 1), peaks_per_cap=round(ppc, 2))
            flags = []
            ex = [r for b, r in exempt if x0 >= b[0] - 5 and y0 >= b[1] - 5 and x1 <= b[2] + 5 and y1 <= b[3] + 5]
            if ex:
                entry['exempt'] = ex[0]
            rise = abs(math.tan(math.radians(ang))) * (x1 - x0)
            entry['rise_in'] = round(rise / ppi, 3)
            # a tilt only counts when the end-to-end rise is visible (short words with round overshoot are not tilted)
            if abs(ang) > LIMITS['tilt_deg'] and rise > max(0.015 * ppi, 0.05 * h):
                flags.append('tilt')
            if jit > LIMITS['jitter']:
                flags.append('jitter')
            entry['wobble_limit'] = round(wobble_limit(h / ppi), 1)
            ts = [f for b, f in typeset if x0 >= b[0] - 5 and y0 >= b[1] - 5 and x1 <= b[2] + 5 and y1 <= b[3] + 5]
            if ts:
                entry['typeset'] = ts[0]
            elif ipi > entry['wobble_limit'] or ppc > LIMITS['peaks_cap_max']:
                flags.append('wobble')
            if ex:
                # 'LEVEL only: ...' exemptions waive the level test but keep EDGES
                if ex[0].upper().startswith('LEVEL ONLY'):
                    flags = [f'exempt:{f}' if f in ('tilt', 'jitter') else f for f in flags]
                else:
                    flags = [f'exempt:{f}' for f in flags]
            entry['flags'] = flags
            rep['lines'].append(entry)
            line_draw.append((entry, p))
    # TRACED-TILT (L47, 10-28): exemptions waive LEVEL for hand lettering, but a whole traced line set off level
    # by capture (Encino 'Shop' at -3.5 deg in pass 2) is not hand quality. Each traced-lettering exemption is
    # re-read on its own and fails when a line tilts > 1.0 deg with a visible rise > 0.03 in, unless its reason
    # declares a deliberate angle (arc, slant, rise, diagonal, angle, hung, tilt, LEVEL only).
    DELIB = ('arc', 'slant', 'rise', 'rising', 'diagonal', 'angle', 'hung', 'tilt', 'level only', 'illustration')
    for b, r in exempt:
        rl = r.lower()
        if not any(k in rl for k in ('letter', 'lettering', 'traced')) or any(k in rl for k in DELIB):
            continue
        x0, y0, x1, y1 = [max(0, int(v)) for v in b]
        for col, m in sources:
            sub = np.zeros_like(m); sub[y0:y1, x0:x1] = m[y0:y1, x0:x1]
            lab2, lines2 = text_lines(sub, ppi, excl, ())
            for ln in lines2:
                if len(ln) < 3:
                    continue
                ang, jit, p2, h2, _ = fit_baseline(ln)
                # the topline must agree: a capture tilt moves tops and feet together; a tall S/h beside a small o
                # moves them apart (letter size, not tilt)
                flip = [dict(c, y1=-c['y0'], y0=-c['y1']) for c in ln]
                angt = -fit_baseline(flip)[0]
                lx0 = min(c['x0'] for c in ln); lx1 = max(c['x1'] for c in ln)
                rise = abs(math.tan(math.radians(ang))) * (lx1 - lx0)
                if (lx1 - lx0) >= 1.0 * ppi and abs(ang) > 1.0 and abs(angt) > 0.6 and ang * angt > 0 and rise > 0.03 * ppi:
                    rep.setdefault('traced_tilt', []).append(dict(box=[int(lx0), int(min(c['y0'] for c in ln)), int(lx1), int(max(c['y1'] for c in ln))],
                                                                 tilt_deg=round(ang, 2), top_tilt_deg=round(angt, 2), rise_in=round(rise / ppi, 3), exempt=r))
    if rep.get('traced_tilt'):
        rep['fails'].append(f"TRACED-TILT: {len(rep['traced_tilt'])} traced line(s) set off level by capture (> 1 deg, visible rise); fix the rectification or declare the deliberate angle")
    # strokes (all ink)
    f_tot = w_tot = sk_all = 0
    for col, m in layers:
        nf, nw, nt, fmask, wmask = thin_strokes(m, ppi, excl)
        f_tot += nf; w_tot += nw; sk_all += nt
        over_blue |= ndimage.binary_dilation(fmask, iterations=2)
        over_lb |= ndimage.binary_dilation(wmask, iterations=1)
    rep['strokes'] = dict(fail_pct=round(100 * f_tot / max(sk_all, 1), 2), warn_pct=round(100 * w_tot / max(sk_all, 1), 2))
    # verdict
    if rep['counters']:
        rep['fails'].append(f"COUNTERS: {len(rep['counters'])} enclosed spaces < {LIMITS['counter_in']} in")
    if rep['gaps']:
        rep['fails'].append(f"GAPS: {len(rep['gaps'])} places where shapes sit < {LIMITS['gap_in']} in apart")
    for b, r in exempt:
        rep['warns'].append(f'EXEMPT {list(b)}: {r}')
    tl = [l for l in rep['lines'] if 'tilt' in l['flags'] or 'jitter' in l['flags']]
    if tl:
        rep['fails'].append(f"LEVEL: {len(tl)} text line(s) not level/steady")
    wl = [l for l in rep['lines'] if 'wobble' in l['flags']]
    if wl:
        rep['fails'].append(f"EDGES: {len(wl)} text line(s) with traced wobble")
    if rep['strokes']['fail_pct'] > 1.0:
        rep['fails'].append(f"STROKES: {rep['strokes']['fail_pct']}% of linework < {LIMITS['stroke_fail_in']} in")
    elif rep['strokes']['warn_pct'] > 2:
        rep['warns'].append(f"STROKES: {rep['strokes']['warn_pct']}% of linework < {LIMITS['stroke_warn_in']} in")
    if not rep['lines']:
        rep['warns'].append('No text lines detected: LEVEL/EDGES did not run - sign-off must check lettering by eye')
    # TYPESET declarations must be real: inside the canvas and holding ink (10-25: a re-set line pasted at a
    # negative offset was never painted, and its declaration hid the loss from SURVIVAL)
    prev_op = None
    if compare:
        pa_ = np.asarray(Image.open(compare).convert('RGBA'))
        if pa_.shape[:2] == (H, W):
            prev_op = pa_[..., 3] > 128
    for b, f in typeset:
        x0, y0, x1, y1 = [int(v) for v in b]
        if x0 < -5 or y0 < -5 or x1 > W + 5 or y1 > H + 5:
            rep['fails'].append(f'TYPESET: declared line {f} {list(b)} runs off the canvas - text clipped or never painted')
        cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
        ink_now = int(op[cy0:cy1, cx0:cx1].sum()) if cx1 > cx0 and cy1 > cy0 else 0
        if ink_now < (0.03 * ppi) ** 2:
            rep['fails'].append(f'TYPESET: declared line {f} {list(b)} holds no ink')
        elif prev_op is not None:
            ink_prev = int(prev_op[cy0:cy1, cx0:cx1].sum())
            if ink_prev > (0.05 * ppi) ** 2 and ink_now < 0.5 * ink_prev:
                rep['fails'].append(f'TYPESET: declared line {f} {list(b)} has {ink_now / ink_prev:.0%} of the previous master\'s ink there - a re-set must replace the line, not drop it')
    # SOURCE (R21, 10-28): under trace-first, a re-set line must say why it was not traced: below the trace floor
    # (reason a), the exact face as printed (b), a trace that fails the gate (c), or the one house locator line (rule 4)
    if r21:
        ok = ('R21 reason a', 'R21 reason b', 'R21 reason c', 'R21 reasons', 'R21 rule 4')
        for b, f in typeset:
            if not any(k in f for k in ok):
                rep['fails'].append(f'SOURCE: re-set line {f} {list(b)} gives no R21 reason (trace-first: trace it, or log why not)')
    if compare:
        sv = survival(compare, a, ppi, [b for b, _ in typeset] + [b for b, _ in redrawn])
        for b, h in redrawn:
            rep['warns'].append(f'REDRAWN {list(b)}: {h} - survival not checked there; compare to the previous master by eye')
        if sv is None:
            rep['warns'].append('SURVIVAL skipped: previous master has a different canvas size - compare by eye')
        else:
            rep['survival'] = sv
            if sv:
                rep['fails'].append(f'SURVIVAL: {len(sv)} shape(s) of the previous master lost, split or shrunk > 20 %')
    rep['verdict'] = 'FAIL' if rep['fails'] else 'PASS'
    # overlay
    bg = Image.new('RGBA', (W, H), (236, 233, 226, 255)); bg.alpha_composite(im)
    o = np.asarray(bg.convert('RGB')).copy()
    o[over_lb] = (110, 170, 255); o[over_blue] = (0, 70, 255)
    o[ndimage.binary_dilation(over_red, iterations=3)] = (255, 0, 0)
    o[ndimage.binary_dilation(over_mag, iterations=4)] = (255, 0, 200)
    ov = Image.fromarray(o); d = ImageDraw.Draw(ov)
    lw = max(2, int(0.01 * ppi))
    try:
        F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', max(14, int(0.09 * ppi)))
    except Exception:
        F = ImageFont.load_default()
    for e, p in line_draw:
        x0, y0, x1, y1 = e['box']
        bad = any(not f.startswith('exempt') for f in e['flags'])
        col = (220, 0, 0) if ('tilt' in e['flags'] or 'jitter' in e['flags']) else ((140, 140, 140) if 'exempt' in e else (0, 160, 60))
        d.line([(x0, np.polyval(p, x0)), (x1, np.polyval(p, x1))], fill=col, width=lw)
        if 'wobble' in e['flags']:
            d.rectangle([x0 - 6, y0 - 6, x1 + 6, y1 + 6], outline=(255, 140, 0), width=lw)
        d.text((x0, y1 + 4), f"{e['tilt_deg']:+.2f}°  j{e['jitter']:.3f}  w{e['inflect_per_in']}/{e['wobble_limit']}  p{e['peaks_per_cap']}", font=F,
               fill=col if bad else (0, 120, 50))
    for b, r in exempt:
        d.rectangle(b, outline=(120, 120, 120), width=lw)
        d.text((b[0] + 6, b[1] + 6), 'EXEMPT: ' + r, font=F, fill=(90, 90, 90))
    os.makedirs(out_dir, exist_ok=True)
    ov.save(os.path.join(out_dir, f'{name}_qa.png'))
    with open(os.path.join(out_dir, f'{name}_qa.json'), 'w') as f:
        json.dump(rep, f, indent=1)
    return rep


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('png'); ap.add_argument('--width-in', type=float, required=True)
    ap.add_argument('--out', default='qa_out'); ap.add_argument('--name')
    ap.add_argument('--exempt', action='append', default=[], help='x0,y0,x1,y1:reason')
    ap.add_argument('--typeset', action='append', default=[], help='x0,y0,x1,y1:Font')
    ap.add_argument('--compare', help='previous master (rebuild survival check)')
    a = ap.parse_args()
    def parse(items):
        out = []
        for e in items:
            box, _, txt = e.partition(':')
            out.append((tuple(int(v) for v in box.split(',')), txt or 'unspecified'))
        return out
    r = run(a.png, a.width_in, a.out, a.name, parse(a.exempt), parse(a.typeset), a.compare)
    print(f"{r['verdict']}  {r['file']} @ {a.width_in} in ({r['ppi']} ppi)")
    for x in r['fails']:
        print('  FAIL', x)
    for x in r['warns']:
        print('  WARN', x)
    sys.exit(0 if r['verdict'] == 'PASS' else 1)
