#!/usr/bin/env python3
"""Fiesta Club logo v3 (HQ 2026-10-25). Input: hammond/wave2/fiesta_club_logo_v2.png (lounge line recentred).
1. "Town & Country Plaza": traced letters (clogged counters, wobble) re-set in League Spartan 800,
   fitted to the traced line's cap height and width; every counter >= 0.05 in at 10 in print.
2. "Club": traced letters (1.0 deg tilt, wobble) re-set in League Spartan 900 on a level baseline;
   oversized cap C kept (430 px tall, as traced); 0.05 in letter gaps.
3. Confetti squiggles thickened to >= 0.034 in and held >= 0.036 in clear of every other shape.
The FIESTA block (hand-drawn reversed letters) is kept exactly as traced, by design.
Usage: python3 fiesta_v3_build.py IN.png OUT.png
"""
import sys, os
import numpy as np
from scipy import ndimage
from skimage.morphology import skeletonize
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'toolkit'))
from vec import smooth_mask  # noqa: E402

FONT = os.environ.get('LEAGUE_SPARTAN', '/home/claude/hbsite/fonts/LeagueSpartan.ttf')
PRINT_W_IN = 10.0
SS = 3


def glyph(ch, size, wght):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([wght])
    L = Image.new('L', (int(size * 1.7), int(size * 1.7)), 0)
    ImageDraw.Draw(L).text((size * 0.2, size * 0.1), ch, font=f, fill=255)
    return L.crop(L.getbbox())


def set_line(text, cap_px, wght, target_w, track_frac, round_px):
    f = ImageFont.truetype(FONT, 100); f.set_variation_by_axes([wght])
    cb = f.getbbox('H'); size = int(100 * cap_px * SS / (cb[3] - cb[1]))
    f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([wght])
    track = track_frac * cap_px * SS
    adv = [f.getlength(c) for c in text]
    L = Image.new('L', (int(sum(adv) + track * len(text)) + 300, int(size * 1.8)), 0)
    d = ImageDraw.Draw(L); x = 150
    for c, av in zip(text, adv):
        d.text((x, 20), c, font=f, fill=255); x += av + track
    L = L.crop(L.getbbox())
    sx = min(max(target_w / (L.width / SS), 0.9), 1.12)
    L = L.resize((int(L.width * sx), L.height), Image.LANCZOS)
    L = L.filter(ImageFilter.GaussianBlur(round_px * SS)).point(lambda v: 255 if v >= 128 else 0)
    return np.asarray(L.resize((L.width // SS, L.height // SS), Image.LANCZOS)) >= 128


def main(src, dst):
    a = np.asarray(Image.open(src).convert('RGBA')).copy()
    H, W = a.shape[:2]; ppi = W / PRINT_W_IN
    op = a[..., 3] > 128
    ink = np.concatenate([a[op][:, :3].mean(0).astype(np.uint8), [255]]).astype(np.uint8)
    lab, n = ndimage.label(op); objs = ndimage.find_objects(lab)
    areas = ndimage.sum(op, lab, range(1, n + 1))
    block = int(np.argmax(areas)) + 1
    bx1 = objs[block - 1][1].stop
    # Club = large shapes right of the block's left half, above the plaza line
    club = [i for i, sl in enumerate(objs, 1) if i != block and areas[i - 1] > 30000 and sl[0].stop < 625]
    plaza = [i for i, sl in enumerate(objs, 1) if sl[0].start >= 600 and (sl[0].stop - sl[0].start) >= 60]
    # the swirl's top hook is fused to the traced C: split it off (thin stroke) and keep it as confetti
    cid = min(club, key=lambda i: objs[i - 1][1].start)
    cfull = lab == cid
    body = ndimage.binary_opening(cfull, structure=np.ones((19, 19)))
    bl, bn = ndimage.label(body)
    body = bl == (np.argmax(ndimage.sum(body, bl, range(1, bn + 1))) + 1)
    body = ndimage.binary_dilation(body, iterations=9) & cfull
    hook = cfull & ~body
    hl_, hn_ = ndimage.label(hook)
    hook = np.isin(hl_, [j for j in range(1, hn_ + 1) if (hl_ == j).sum() > 200])
    lab = lab.copy(); lab[hook] = n + 1; n += 1
    objs = ndimage.find_objects(lab)
    areas = ndimage.sum(lab > 0, lab, range(1, n + 1))
    cx0 = min(objs[i - 1][1].start for i in club); cx1 = max(objs[i - 1][1].stop for i in club)
    px0 = min(objs[i - 1][1].start for i in plaza); px1 = max(objs[i - 1][1].stop for i in plaza)
    ptop = min(objs[i - 1][0].start for i in plaza)
    a[np.isin(lab, club + plaza) & ~hook] = 0
    keep_ids = set(club + plaza + [block])
    conf_ids = [i for i in range(1, n + 1) if i not in keep_ids]
    a[hook] = ink            # the hook stays (confetti)

    # 1. plaza line
    m = set_line('Town & Country Plaza', 97, 800, px1 - px0, 0.08, 2)
    lh, lw = m.shape; ox = int((px0 + px1) / 2 - lw / 2)
    a[ptop:ptop + lh, ox:ox + lw][m] = ink

    # 2. Club
    f = ImageFont.truetype(FONT, 1000); f.set_variation_by_axes([900]); bb = f.getbbox('u')
    size = int(1000 * 247 * SS / (bb[3] - bb[1]))
    gl = {c: glyph(c, size, 900) for c in 'lub'}
    # the cap C keeps the traced C's footprint and lean: its left edge is fitted to the traced C's
    # left edge at the shoulder and the foot, so the swirl ornament beside it keeps its room
    c_sl = ndimage.find_objects(body.astype(int))[0]
    cw, ch = c_sl[1].stop - c_sl[1].start, c_sl[0].stop - c_sl[0].start
    cy0 = c_sl[0].start
    tC = body
    def left_at(mask, y):
        xs = np.nonzero(mask[y])[0]
        return xs.min() if len(xs) else None
    yA, yB = cy0 + int(0.21 * ch), cy0 + int(0.86 * ch)
    tA, tB = left_at(tC, yA), left_at(tC, yB)
    C = glyph('C', size, 900).resize((cw, ch), Image.LANCZOS)
    cm = np.asarray(C) >= 128
    gA, gB = left_at(cm, int(0.21 * ch)), left_at(cm, int(0.86 * ch))
    # x' = x + dx + s * (yB_rel - y_rel): solve so the glyph's left edge hits tA at yA and tB at yB
    s_ = ((tA - c_sl[1].start - gA) - (tB - c_sl[1].start - gB)) / (0.65 * ch)
    dx = tB - c_sl[1].start - gB
    Cs = C.transform((cw + 120, ch), Image.AFFINE, (1, s_, -dx - s_ * 0.86 * ch, 0, 1, 0), resample=Image.BICUBIC)
    Cs = Cs.crop((0, 0, Cs.getbbox()[2], ch))
    gl['C'] = Cs.resize((Cs.width * SS, ch * SS), Image.LANCZOS)
    c_left = c_sl[1].start
    gap = int(0.05 * ppi * SS)
    rest = sum(gl[c].width for c in 'lub')
    sx = ((cx1 - c_left) * SS - 3 * gap - gl['C'].width) / rest
    for c in 'lub':
        gl[c] = gl[c].resize((int(gl[c].width * sx), gl[c].height), Image.LANCZOS)
    print('C body %dx%d at y%d  lean s=%.3f dx=%d  lub scale %.3f' % (cw, ch, cy0, s_, dx, sx))
    L = Image.new('L', (W * SS, H * SS), 0); x = cx0 * SS; base = 590 * SS
    for c in 'Club':
        g = gl[c]
        yb = base + (int(0.012 * g.height) if c == 'C' else 0)   # round C overshoots the baseline
        L.paste(g, (int(x), int(yb - g.height)), g)
        x += g.width + gap
    L = L.filter(ImageFilter.GaussianBlur(2 * SS)).point(lambda v: 255 if v >= 128 else 0)
    a[np.asarray(L.resize((W, H), Image.LANCZOS)) >= 128] = ink

    # 3. confetti
    op = a[..., 3] > 128
    conf = np.isin(lab, conf_ids) & op
    keep = op & ~conf
    dt = ndimage.distance_transform_edt(conf)
    target = 0.034 * ppi
    new = np.zeros_like(conf)
    for i in conf_ids:
        sl = objs[i - 1]; pad = 10
        y0, y1 = max(0, sl[0].start - pad), min(H, sl[0].stop + pad)
        x0, x1 = max(0, sl[1].start - pad), min(W, sl[1].stop + pad)
        mm = lab[y0:y1, x0:x1] == i
        sk = skeletonize(mm)
        w = 2 * np.percentile(dt[y0:y1, x0:x1][sk], 10) if sk.sum() > 3 else target
        r = int(np.ceil(max(0, (target - w) / 2)))
        if r > 0:
            yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
            mm = ndimage.binary_dilation(mm, structure=(xx ** 2 + yy ** 2) <= r * r)
        new[y0:y1, x0:x1] |= mm
    far = ndimage.distance_transform_edt(~keep) > 0.036 * ppi
    new = smooth_mask(new & far, 2.0, min_area=10) & far
    # keep confetti pieces >= 0.036 in from each other too: each later piece is trimmed back from earlier ones
    pl, pn = ndimage.label(new)
    placed = np.zeros_like(new)
    for jj in range(1, pn + 1):
        piece = pl == jj
        if placed.any():
            piece &= ndimage.distance_transform_edt(~placed) > 0.036 * ppi
        placed |= piece
    new = placed
    a[conf] = 0; a[new] = ink
    # 4. open every tiny enclosed space (block letters' eyes, confetti loops) to >= 0.032 in
    op = a[..., 3] > 128
    blk = op
    holes = ndimage.binary_fill_holes(blk) & ~blk
    hl, hn = ndimage.label(holes)
    dth = ndimage.distance_transform_edt(holes)
    for j in range(1, hn + 1):
        reg = hl == j
        w = 2 * dth[reg].max()
        if w < 0.032 * ppi:
            r = int(np.ceil((0.032 * ppi - w) / 2)) + 1
            yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
            grown = ndimage.binary_dilation(reg, structure=(xx ** 2 + yy ** 2) <= r * r)
            a[grown & blk] = 0
    Image.fromarray(a).save(dst, optimize=True)
    print('wrote', dst, 'club x', cx0, cx1, 'plaza x', px0, px1, 'confetti', len(conf_ids))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
