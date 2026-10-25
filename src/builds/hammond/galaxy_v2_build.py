#!/usr/bin/env python3
"""Galaxy Drive-In courtesy pass card v2 (HQ 2026-10-25, S9). Input: hammond/wave2/galaxy_pass_card.png (v1).
v1 traced every line from a curled card: serif lines up to 1.1 deg off level vs the level rules, trace wobble.
1. COURTESY PASS, the address line and the Expires / Approved labels re-set in TeX Gyre Pagella Bold
   (Palatino; the card's face, heavier cut to match its ink weight), fitted to the traced cap height, width, position.
2. The brush script 'galaxy drive in theatre' is hand lettering: traced letterforms kept, outline-smoothed,
   and levelled as one unit (principal-axis tilt).
3. Fill-in rules redrawn: same y / weight / end, starting 0.05 in after each label, round caps.
Cream card layer kept as is.
Usage: galaxy_v2_build.py IN.png OUT.png
"""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit')
sys.path.insert(0, T)
from vec import smooth_mask  # noqa: E402
G = '/usr/share/texmf/fonts/opentype/public/tex-gyre/'
PB = G + 'texgyrepagella-bold.otf'
PRINT_W = 9.0
SS = 4
INK = (34, 31, 30, 255); CARD = (241, 232, 200, 255)


def render_line(text, font, cap_px, target_w, track_frac=0.03):
    f0 = ImageFont.truetype(font, 200); cb = f0.getbbox('H', anchor='ls')
    size = int(200 * cap_px * SS / (cb[3] - cb[1]))
    f = ImageFont.truetype(font, size)
    base = int(size * 1.3)
    nat = f.getlength(text)
    track = max(track_frac * cap_px * SS, (target_w * SS - nat) / max(1, len(text) - 1))
    track = min(track, 0.25 * cap_px * SS)
    L = Image.new('L', (int(nat + track * len(text) + size * 2), int(size * 2)), 0)
    d = ImageDraw.Draw(L); x = size * 0.5
    for ch in text:
        d.text((x, base), ch, font=f, fill=255, anchor='ls'); x += f.getlength(ch) + track
    bb = L.getbbox(); L = L.crop((bb[0], 0, bb[2], L.height))
    sx = min(max(target_w * SS / L.width, 0.9), 1.06) if L.width > target_w * SS else min(target_w * SS / L.width, 1.06)
    L = L.resize((int(L.width * sx), L.height), Image.LANCZOS)
    return np.asarray(L.resize((L.width // SS, L.height // SS), Image.LANCZOS)) >= 128, base // SS


def main(src, dst):
    a = np.asarray(Image.open(src).convert('RGBA'))
    H, W = a.shape[:2]; ppi = W / PRINT_W
    ink = (a[..., 3] > 128) & (np.abs(a[..., :3].astype(int) - np.array(INK[:3])).sum(2) < 90)
    card = (a[..., 3] > 128) & ~ink
    has_card = card.sum() > 0.2 * card.size          # the ink-only (natural tee) master has no card layer
    card_full = (ndimage.binary_fill_holes(card | ink) & (a[..., 3] > 128)) if has_card else np.zeros_like(ink)
    lab, n = ndimage.label(ink); objs = ndimage.find_objects(lab)
    rules = []; text = ink.copy()
    for j, sl in enumerate(objs, 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if w > 8 * h:
            comp = lab == j
            rules.append(((sl[0].start + sl[0].stop) / 2, int(round(comp.sum() / w)), sl[1].stop))
            text &= ~comp
    rows = text.any(1); bands = []; y = 0
    while y < H:
        if rows[y]:
            y0 = y
            while y < H and rows[y]:
                y += 1
            bands.append((y0, y))
        y += 1
    bands = [b for b in bands if b[1] - b[0] > 0.04 * ppi]
    print('bands', bands, 'rules', rules)
    if len(bands) == 4:
        # the script's descenders share rows with the address line: split by component (address glyphs are small, low)
        y0, y1 = bands[1]
        sub = text[y0:y1]; l2, _ = ndimage.label(sub)
        addr = np.zeros_like(sub)
        for j, sl in enumerate(ndimage.find_objects(l2), 1):
            if sl[0].start > 0.55 * (y1 - y0) and (sl[0].stop - sl[0].start) < 0.33 * ppi:
                addr |= l2 == j
        ya = y0 + np.nonzero(addr.any(1))[0].min(); yb = y0 + np.nonzero(addr.any(1))[0].max() + 1
        script_only = text.copy(); script_only[y0:y1] &= ~addr
        addr_only = np.zeros_like(text); addr_only[y0:y1] = addr
        BANDS = [(bands[0], text), ((y0, y1), script_only), ((ya, yb), addr_only), (bands[2], text), (bands[3], text)]
    else:
        BANDS = [(b, text) for b in bands]
    assert len(BANDS) == 5, bands
    out = np.zeros_like(a)
    out[card_full] = CARD
    prov = {'typeset': [], 'exempt': []}
    specs = [('COURTESY PASS', 'c', 0), (None, 'script', None), ('309 Natchez St. • Hammond, LA', 'c', 0),
             ('Expires', 'l', 0), ('Approved', 'l', 0)]
    for ((y0, y1), src_m), (txt, al, ref) in zip(BANDS, specs):
        m = src_m[y0:y1]
        if al == 'script':
            reg = np.zeros_like(ink); reg[y0:y1] = m
            ys, xs = np.nonzero(reg)
            cov = np.cov(np.stack([xs, ys]))
            ev, evec = np.linalg.eigh(cov); v = evec[:, np.argmax(ev)]
            ang = np.degrees(np.arctan2(v[1], v[0]))
            if ang > 90: ang -= 180
            if ang < -90: ang += 180
            cx, cy = xs.mean(), ys.mean()
            big = Image.fromarray((reg * 255).astype(np.uint8)).resize((W * SS, H * SS), Image.BILINEAR)
            big = big.rotate(ang, resample=Image.BICUBIC, center=(cx * SS, cy * SS))
            rot = np.asarray(big.resize((W, H), Image.LANCZOS)) >= 128
            rot = smooth_mask(rot, 0.008 * ppi)
            out[rot] = INK
            prov['exempt'].append([[int(xs.min()) - 20, int(y0) - 30, int(xs.max()) + 20, int(y1) + 30],
                                   'brush script "galaxy drive in theatre" - hand lettering (traced, smoothed, levelled %+.2f deg)' % -ang])
            print('script levelled %+.2f deg' % -ang)
            continue
        lab2, _ = ndimage.label(m)
        sls = sorted([s for s in ndimage.find_objects(lab2) if (s[0].stop - s[0].start) > 0.03 * ppi], key=lambda s: s[1].start)
        cap = sls[ref][0].stop - sls[ref][0].start
        base_y = y0 + sls[ref][0].stop
        xs = np.nonzero(m.any(0))[0]; x0, x1 = xs.min(), xs.max()
        mm, base_in = render_line(txt, PB, cap, x1 - x0)
        lh, lw = mm.shape
        ox = int((x0 + x1) / 2 - lw / 2) if al == 'c' else int(x0)
        oy = int(base_y - base_in)
        sub = out[oy:oy + lh, ox:ox + lw]; sub[mm[:sub.shape[0], :sub.shape[1]]] = INK
        prov['typeset'].append([[ox, oy, ox + lw, oy + lh], 'TeX Gyre Pagella Bold'])
        print(f'{txt!r:36s} cap {cap}px ({cap / ppi:.3f} in) width {x1 - x0}->{lw}')
        if al == 'l':
            r_ = min(rules, key=lambda r: abs(r[0] - base_y))
            yc, th, xe = r_
            xs_l = ox + int(np.nonzero(mm.any(0))[0].max()) + int(0.08 * ppi)
            Lr = Image.new('L', (W * 2, H * 2), 0); dr = ImageDraw.Draw(Lr)
            dr.line([(xs_l * 2, yc * 2), (xe * 2, yc * 2)], fill=255, width=th * 2)
            for xx in (xs_l, xe):
                dr.ellipse([(xx - th / 2) * 2, (yc - th / 2) * 2, (xx + th / 2) * 2, (yc + th / 2) * 2], fill=255)
            out[np.asarray(Lr.resize((W, H), Image.LANCZOS)) >= 128] = INK
    Image.fromarray(out).save(dst, optimize=True)
    json.dump(prov, open(os.path.splitext(dst)[0] + '.prov.json', 'w'), indent=1)
    print('wrote', dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
