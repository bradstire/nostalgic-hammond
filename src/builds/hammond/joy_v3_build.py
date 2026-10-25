#!/usr/bin/env python3
"""Joy Drive-In courtesy pass v3 (HQ 2026-10-25, S9). Input: v2 (joy_v2_build.py output: lines levelled).
The pass was photographed worn: traced letters are deformed at shape level (uneven weights, lumpy J/O), which
smoothing cannot fix. Every slab line is re-set in Arvo Bold / Bold Italic (OFL; a geometric slab in the
Memphis/Beton family the card is printed in), fitted to the traced line's cap height, width and position.
Fidelity detail: the card's single-storey 'a' is built from Arvo's own 'd' cut at x-height.
Border beads, fill-in rules and the Schola Bold bottom line are kept from v2; the border rule is
thickened to 0.03 in (prints reliably; beads unchanged).
Usage: joy_v3_build.py V2.png OUT.png
"""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
F = '/home/claude/hbsite/fonts/'
ARVO_B = F + 'arvo-latin-700-normal.woff'
ARVO_BI = F + 'arvo-latin-700-italic.woff'
PRINT_W = 9.0
SS = 4

LINES = [  # (text, font, align, index of a reference capital among the line's shapes, left to right)
    ('Driver\u2019s  Courtesy  Pass', ARVO_B, 'c', 0),
    ('JOY DRIVE-IN THEATRE', ARVO_B, 'c', 2),        # J dips below the baseline; Y is a clean cap
    ('Hammond, La.', ARVO_B, 'c', 0),
    ('Admit One Driver', ARVO_BI, 'c', 0),
    ('Issued to.', ARVO_B, 'l', 0),
    ('Void after.', ARVO_B, 'l', 0),
    ('By.', ARVO_B, 'l', 0),
    ('\u2014 This Pass Not Transferable \u2014', ARVO_B, 'c', 'max'),   # T after the dash; Arvo: no hairlines at 0.12 in
]


def glyph_img(ch, f, base, single_a=True):
    """Glyph drawn on the baseline y=base (anchor 'ls'). 'a' -> single-storey (Arvo 'd' cut at x-height)."""
    src = 'd' if (ch == 'a' and single_a) else ch
    im = Image.new('L', (int(f.getlength(src)) + f.size, int(f.size * 2.0)), 0)
    ImageDraw.Draw(im).text((f.size // 4, base), src, font=f, fill=255, anchor='ls')
    if ch == 'a' and single_a:
        xtop = base - (f.getbbox('x', anchor='ls')[3] - f.getbbox('x', anchor='ls')[1])
        xtop = base + f.getbbox('x', anchor='ls')[1]
        arr = np.asarray(im).copy(); arr[:xtop, :] = 0
        im = Image.fromarray(arr)
    return im, f.getlength(src)


def render_line(text, font, cap_px, target_w, track_frac=None):
    f0 = ImageFont.truetype(font, 200); cb = f0.getbbox('H', anchor='ls')
    size = int(200 * cap_px * SS / (cb[3] - cb[1]))
    f = ImageFont.truetype(font, size)
    nat = sum(f.getlength(c) for c in text)
    if track_frac is None:
        # fill the traced width with tracking first (>= 4 % of cap), then at most +/-6 % horizontal scale
        track = max(0.035 * cap_px * SS, (target_w * SS / 1.0 - nat) / max(1, len(text) - 1))
        track = min(track, 0.30 * cap_px * SS)
    else:
        track = track_frac * cap_px * SS
    base = int(size * 1.3)
    Wd = int(sum(f.getlength(c) for c in text) + track * len(text) + size * 2)
    Hd = int(size * 2.0)
    L = Image.new('L', (Wd, Hd), 0)
    x = size * 0.5
    for ch in text:
        g, adv = glyph_img(ch, f, base)
        L.paste(g, (int(x - size // 4), 0), g)
        x += adv + track
    bb = L.getbbox()
    L = L.crop((bb[0], 0, bb[2], Hd))
    sx = min(max(target_w * 1.04 * SS / L.width, 0.88), 1.06) if L.width > target_w * SS else min(target_w * SS / L.width, 1.06)
    L = L.resize((int(L.width * sx), Hd), Image.LANCZOS)
    m = np.asarray(L.resize((L.width // SS, Hd // SS), Image.LANCZOS)) >= 128
    return m, base // SS, sx


def main(src, dst):
    a = np.asarray(Image.open(src).convert('RGBA')).copy()
    H, W = a.shape[:2]; ppi = W / PRINT_W
    op = a[..., 3] > 128
    ink = np.concatenate([a[op][:, :3].mean(0).astype(np.uint8), [255]]).astype(np.uint8)
    lab, n = ndimage.label(op); objs = ndimage.find_objects(lab)
    struct = np.zeros_like(op)
    for i, sl in enumerate(objs, 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if w > 8 * h or h > 8 * w or (h > 0.6 * H and w > 0.6 * W) or (max(h, w) < 0.035 * ppi):
            struct |= lab == i
    text = op & ~struct
    # bands of text rows
    rows = text.any(1)
    bands = []; y = 0
    while y < H:
        if rows[y]:
            y0 = y
            while y < H and rows[y]:
                y += 1
            bands.append((y0, y))
        y += 1
    bands = [b for b in bands if b[1] - b[0] > 0.04 * ppi]
    print('bands', bands)
    assert len(bands) == len(LINES), f'expected {len(LINES)} text bands, got {len(bands)}'
    # the bottom line's em dashes were classed as rules: clear everything inside the border on that band
    yb0, yb1 = bands[-1]
    inner = np.zeros_like(op); inner[yb0 - 8:yb1 + 8, int(0.6 * ppi):W - int(0.6 * ppi)] = True   # border sides stay
    full_bottom = op & inner
    xs_b = np.nonzero(full_bottom.any(0))[0]; bottom_x = (xs_b.min(), xs_b.max())
    struct &= ~full_bottom
    text[yb0 - 8:yb1 + 8, :] |= full_bottom[yb0 - 8:yb1 + 8, :]
    # fill-in rules: record (y, thickness, x_end) and take them out; redrawn after their labels are set
    rules = []
    rl_, rn_ = ndimage.label(struct)
    for j, sl_ in enumerate(ndimage.find_objects(rl_), 1):
        h_ = sl_[0].stop - sl_[0].start; w_ = sl_[1].stop - sl_[1].start
        if w_ > 8 * h_ and w_ < 0.9 * W and sl_[0].start > 0.25 * H and sl_[0].stop < bands[-1][0]:
            comp = rl_ == j
            th = int(round(comp.sum() / w_))
            rules.append(((sl_[0].start + sl_[0].stop) / 2, th, sl_[1].stop))
            struct &= ~comp
    out = np.zeros_like(a)
    # border rule thickening: struct pixels on the border ring get dilated to 0.03 in where thinner
    ring = struct & ~ndimage.binary_opening(struct, iterations=int(0.012 * ppi))
    dt = ndimage.distance_transform_edt(struct)
    thick = ndimage.binary_dilation(struct, iterations=max(0, int(round((0.03 * ppi - 2 * dt[struct].mean()) / 2))))
    struct2 = struct | (thick & ndimage.binary_dilation(ring, iterations=3))
    out[struct2] = ink
    prov = {'typeset': [], 'exempt': []}
    for (y0, y1), (txt, font, al, ref) in zip(bands, LINES):
        m = text[y0 - 8:y1 + 8] if txt.startswith('\u2014') else text[y0:y1]
        yo = y0 - 8 if txt.startswith('\u2014') else y0
        lab2, n2 = ndimage.label(m)
        sls = sorted([s_ for s_ in ndimage.find_objects(lab2) if (s_[0].stop - s_[0].start) > 0.03 * ppi],
                     key=lambda s_: s_[1].start)
        if ref == 'max':
            r_ = max(sls, key=lambda s_: s_[0].stop - s_[0].start)
            cap = int(0.97 * (r_[0].stop - r_[0].start))      # ascenders run ~3 % over cap height
            base_y = yo + int(np.median([s_[0].stop for s_ in sls if (s_[0].stop - s_[0].start) > 0.6 * cap]))
        else:
            cap = sls[ref][0].stop - sls[ref][0].start
            base_y = yo + sls[ref][0].stop
        xs = np.nonzero(m.any(0))[0]; x0, x1 = xs.min(), xs.max()
        if txt.startswith('\u2014'):
            # the card sets this line compact: ~59 % of the border width (source photo), natural spacing
            border_w = W - 2 * int(0.45 * ppi)
            cap = max(cap, int(0.21 * ppi))   # >= 0.21 in cap keeps Arvo Bold's e/a eyes >= 0.025 in
            mm, base_in, sx = render_line(txt, font, cap, int(0.62 * border_w), track_frac=0.05)
            x0, x1 = W // 2 - 1, W // 2 + 1
        else:
            mm, base_in, sx = render_line(txt, font, cap, x1 - x0)
        lh, lw = mm.shape
        ox = int((x0 + x1) / 2 - lw / 2) if al == 'c' else int(x0)
        oy = int(base_y - base_in)
        sub = out[oy:oy + lh, ox:ox + lw]
        sub[mm[:sub.shape[0], :sub.shape[1]]] = ink
        prov['typeset'].append([[ox, oy, ox + lw, oy + lh], os.path.basename(font).replace('.woff', '')])
        if al == 'l':   # fill-in rule redrawn: starts 0.05 in after the label, round caps, original y/weight/end
            r_ = min(rules, key=lambda r: abs(r[0] - base_y)) if rules else None
            if r_ and abs(r_[0] - base_y) < 0.15 * ppi:
                yc, th, xe = r_
                xs_l = ox + int(np.nonzero(mm.any(0))[0].max()) + int(0.05 * ppi)
                Lr = Image.new('L', (W * 2, H * 2), 0); dr = ImageDraw.Draw(Lr)
                dr.line([(xs_l * 2, yc * 2), (xe * 2, yc * 2)], fill=255, width=th * 2)
                for xx in (xs_l, xe):
                    dr.ellipse([(xx - th / 2) * 2, (yc - th / 2) * 2, (xx + th / 2) * 2, (yc + th / 2) * 2], fill=255)
                rm = np.asarray(Lr.resize((W, H), Image.LANCZOS)) >= 128
                out[rm] = ink
        print(f'{txt!r:32s} cap {cap}px ({cap / ppi:.3f} in)  width {x1 - x0}->{lw}  sx {sx:.3f}')
    # keep the bottom line's provenance (Schola, from v2's sidecar)
    Image.fromarray(out).save(dst, optimize=True)
    json.dump(prov, open(os.path.splitext(dst)[0] + '.prov.json', 'w'), indent=1)
    print('wrote', dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
