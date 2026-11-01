"""S9 gate-fix pass for colour-separated illustration masters (HQ 2026-11-01).
Uses the gate's own detectors (toolkit/art_qa.py) and repairs exactly what they flag, at print size:
  COUNTERS  a flagged enclosed space is filled with the ink around it (it would fill on press anyway);
  GAPS      a flagged near-touch is bridged inside a small disc with the nearer ink (it would bleed shut);
  STROKES   linework under 0.015 in grows 1 px into empty ground only (other inks are never overwritten).
Repeats until those three pass (max 12 rounds). LEVEL/EDGES are design calls, declared in the .prov.json."""
import sys, json, numpy as np, cv2
from scipy import ndimage
from PIL import Image
sys.path.insert(0, '/home/claude/print-assets/toolkit')
import art_qa as Q

def layers(a):
    op = a[..., 3] > 128
    cols, counts = np.unique(a[op][:, :3].reshape(-1, 3), axis=0, return_counts=True)
    return [tuple(int(v) for v in c) for c, n in zip(cols, counts) if n > 50]

def paint(a, mask, col):
    a[mask, :3] = col; a[mask, 3] = 255

def nearest_ink(a, cols, mask):
    """colour each pixel of mask with the nearest ink colour"""
    d = [ndimage.distance_transform_edt(~((a[..., 3] > 128) & np.all(a[..., :3] == c, -1))) for c in cols]
    best = np.argmin(np.stack(d), 0)
    for i, c in enumerate(cols):
        paint(a, mask & (best == i), c)

def one_round(a, ppi):
    op = a[..., 3] > 128
    cols = layers(a)
    excl = Q.halftone_zone(op, ppi)
    nC = nG = 0
    min_area = (0.025 * ppi) ** 2
    for col in cols + ['all']:
        m = op if col == 'all' else (op & np.all(a[..., :3] == col, -1))
        cs, bad = Q.check_counters(m, ppi, excl)
        if cs:
            nC += len(cs)
            if col == 'all': nearest_ink(a, cols, bad)
            else: paint(a, bad, col)
            op = a[..., 3] > 128
            m = op if col == 'all' else (op & np.all(a[..., :3] == col, -1))
        gs, _ = Q.check_gaps(m, ppi, excl, min_area)
        for g in gs:
            nG += 1
            r = max(3, int(round(2 * Q.LIMITS['gap_in'] * ppi)))
            y, x = g['y'], g['x']
            y0, y1, x0, x1 = max(0, y - r), y + r + 1, max(0, x - r), x + r + 1
            sub = m[y0:y1, x0:x1].astype(np.uint8)
            k = int(np.ceil(g['floor_in'] * ppi / 2)) + 1          # slim bridge: just wider than the gap floor
            closed = cv2.morphologyEx(sub, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))) > 0
            yy, xx = np.ogrid[y0:y1, x0:x1]
            disc = (yy - y) ** 2 + (xx - x) ** 2 <= r * r
            add = closed & ~sub.astype(bool) & ~op[y0:y1, x0:x1] & disc
            if not add.any() and col == OUTLINE:     # outline pieces split by a sub-floor sliver of a fill: join them
                add = closed & ~sub.astype(bool) & disc
            if not add.any() and col != 'all' and OUTLINE is not None and col != OUTLINE:
                # the space between is another ink (a drawn line): widen that line into this ink, never bridge over it
                sep = (a[y0:y1, x0:x1, 3] > 128) & np.all(a[y0:y1, x0:x1, :3] == OUTLINE, -1)
                if sep.any():
                    need = int(np.ceil((g['floor_in'] - g['gap_in']) * ppi / 2)) + 2
                    near = cv2.dilate(sep.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * need + 1, 2 * need + 1))) > 0
                    eat = near & sub.astype(bool) & disc
                    a[y0:y1, x0:x1][eat, :3] = OUTLINE; a[y0:y1, x0:x1][eat, 3] = 255
                continue
            if col == 'all':
                blk = np.zeros(op.shape, bool); blk[y0:y1, x0:x1] = add; nearest_ink(a, cols, blk)
            else:
                a[y0:y1, x0:x1][add, :3] = col; a[y0:y1, x0:x1][add, 3] = 255
        op = a[..., 3] > 128
    # thin strokes, per ink as the gate measures them: thicken to ~0.02 in (into ground or neighbouring ink)
    tots = [Q.thin_strokes(op & np.all(a[..., :3] == c, -1), ppi, excl) for c in cols]
    f = sum(t[0] for t in tots); n = sum(t[2] for t in tots)
    nS = 0
    if n and f / n > 0.008:
        for c, t in zip(cols, tots):
            if not t[0]: continue
            grow = cv2.dilate(t[3].astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) > 0
            grow &= ~(op & np.all(a[..., :3] == c, -1))
            if c != OUTLINE: grow &= ~op          # fills grow into empty ground only; only the outline ink may widen over others
            nS += int(grow.sum()); paint(a, grow, c)
    return a, nC, nG, nS

OUTLINE = None
if __name__ == '__main__':
    src, dst, width_in = sys.argv[1], sys.argv[2], float(sys.argv[3])
    if len(sys.argv) > 4: OUTLINE = tuple(int(sys.argv[4].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    a = np.array(Image.open(src).convert('RGBA'))
    # snap to flat inks (no anti-aliased in-betweens)
    cols = layers(a)
    ppi = a.shape[1] / width_in
    for k in range(int(__import__("os").environ.get("ROUNDS","6"))):
        a, nC, nG, nS = one_round(a, ppi)
        print('round', k, 'counters', nC, 'gaps', nG, 'thin px grown', nS, flush=True)
        if nC == 0 and nG == 0 and nS == 0: break
    Image.fromarray(a, 'RGBA').save(dst, dpi=(300, 300))
