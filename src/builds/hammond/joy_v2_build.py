#!/usr/bin/env python3
"""Joy Drive-In courtesy pass v2 (HQ 2026-10-25, S9 art gate).
Input: hammond/wave2/joy_pass_ink.png (v1: traced slab lines, ~1 deg off level vs the level rules; trace wobble;
bottom line typeset but deliberately roughened).
1. Every traced text line is levelled about its own centre (baseline tilt measured by the gate's line finder).
2. Traced letters get corner-preserving smoothing: serif tips and junctions pinned, runs between them smoothed,
   so the Memphis-style slabs keep their shapes (incl. the single-storey a) and lose the trace wobble.
3. "— This Pass Not Transferable —" re-set crisp in TeX Gyre Schola Bold (no roughening, ever: S9).
Border beads and fill-in rules are clean vector already and are not touched.
Usage: joy_v2_build.py IN.png OUT.png
"""
import sys, os, json
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageFilter
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'toolkit')
sys.path.insert(0, T)
import art_qa as Q  # noqa: E402
from vec import smooth_mask_corners, level_lines  # noqa: E402
SCHOLA_B = '/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreschola-bold.otf'
PRINT_W = 9.0


def set_line(text, font, cap_px, target_w, SS=3, round_px=0):
    f = ImageFont.truetype(font, 100); cb = f.getbbox('H')
    size = int(100 * cap_px * SS / (cb[3] - cb[1]))
    f = ImageFont.truetype(font, size)
    L = Image.new('L', (int(f.getlength(text)) + size, int(size * 1.8)), 0)
    ImageDraw.Draw(L).text((size // 2, size // 3), text, font=f, fill=255)
    L = L.crop(L.getbbox())
    sx = min(max(target_w * SS / L.width, 0.9), 1.1)
    L = L.resize((int(L.width * sx), L.height), Image.LANCZOS)
    if round_px:
        L = L.filter(ImageFilter.GaussianBlur(round_px * SS)).point(lambda v: 255 if v >= 128 else 0)
    return np.asarray(L.resize((L.width // SS, L.height // SS), Image.LANCZOS)) >= 128


def main(src, dst):
    a = np.asarray(Image.open(src).convert('RGBA')).copy()
    H, W = a.shape[:2]; ppi = W / PRINT_W
    op = a[..., 3] > 128
    ink = np.concatenate([a[op][:, :3].mean(0).astype(np.uint8), [255]]).astype(np.uint8)
    lab, n = ndimage.label(op); objs = ndimage.find_objects(lab)
    # structure = border ring + rules + beads (long/thin or tiny round) ; text = the rest
    struct = np.zeros_like(op)
    for i, sl in enumerate(objs, 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if w > 8 * h or h > 8 * w or (h > 0.6 * H and w > 0.6 * W) or (max(h, w) < 0.035 * ppi):
            struct |= lab == i
    text = op & ~struct
    # bottom line (typeset, roughened in v1): find it as the lowest text line, re-set crisp
    tl, lines = Q.text_lines(text, ppi, np.zeros_like(op))
    lines = sorted(lines, key=lambda ln: -max(c['y1'] for c in ln))
    bottom = lines[0]
    bx0 = min(c['x0'] for c in bottom); bx1 = max(c['x1'] for c in bottom)
    by0 = min(c['y0'] for c in bottom); by1 = max(c['y1'] for c in bottom)
    cap = int(np.median([c['h'] for c in bottom if c['h'] > 0.6 * max(k['h'] for k in bottom)]))
    # the em dashes belong to the line: clear the whole band
    band = np.zeros_like(op); band[by0 - 6:by1 + 6, :] = True
    dash_and_text = text & band
    xs = np.nonzero(dash_and_text.any(0))[0]; fx0, fx1 = xs.min(), xs.max()
    text &= ~band
    nt = set_line('— This Pass Not Transferable —', SCHOLA_B, cap, fx1 - fx0)
    lh, lw = nt.shape
    ox = int((fx0 + fx1) / 2 - lw / 2); oy = int(by1 - lh)  # baseline-ish: bottoms aligned
    new_bottom = np.zeros_like(op); new_bottom[oy:oy + lh, ox:ox + lw] = nt
    # level the traced lines
    tl, lines = Q.text_lines(text, ppi, np.zeros_like(op))
    todo = []
    for ln in lines:
        ang, jit, p, h, nk = Q.fit_baseline(ln)
        reg = np.isin(tl, [c['id'] for c in ln])
        todo.append((reg, ang))
    # small marks not in any line (apostrophes, periods, hyphens) travel with their nearest line
    covered = np.zeros_like(op)
    for reg, _ in todo:
        covered |= reg
    rest = text & ~covered
    rl, rn = ndimage.label(rest)
    grown = []
    for reg, ang in todo:
        ys, xs = np.nonzero(reg)
        box = (ys.min() - 0.05 * ppi, ys.max() + 0.05 * ppi, xs.min() - 0.05 * ppi, xs.max() + 0.05 * ppi)
        add = np.zeros_like(op)
        for j, sl in enumerate(ndimage.find_objects(rl), 1):
            cy = (sl[0].start + sl[0].stop) / 2; cx = (sl[1].start + sl[1].stop) / 2
            if box[0] <= cy <= box[1] and box[2] <= cx <= box[3]:
                add |= rl == j
        grown.append((reg | add, ang))
    text2 = level_lines(text, grown)
    for reg, ang in grown:
        print('levelled %+.2f deg  (%d px wide)' % (ang, np.ptp(np.nonzero(reg.any(0))[0])))
    # corner-preserving smoothing of the traced letters
    text2 = smooth_mask_corners(text2, sigma_px=0.012 * ppi, corner_deg=38)
    out = np.zeros_like(a)
    out[struct] = ink; out[text2] = ink; out[new_bottom] = ink
    Image.fromarray(out).save(dst, optimize=True)
    # provenance sidecar: the bottom line is typeset
    json.dump({'typeset': [[[int(ox), int(oy), int(ox + lw), int(oy + lh)], 'TeX Gyre Schola Bold']], 'exempt': []},
              open(os.path.splitext(dst)[0] + '.prov.json', 'w'))
    print('wrote', dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
