"""Old English capital H = narrow spur stroke + textura 'h'. Build that from ONE open-licensed family
(left element of its own 'H' + its own lowercase 'h' raised to cap height) and score vs the 1983 fused letter."""
import glob, os, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/hhs")
N = 256
tgt_raw = np.array(Image.open(f"{HB}/ref/hhs/h_fused_bw.png").convert("L")) < 128

def crop(m):
    ys, xs = np.where(m); return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def norm(m):
    m = crop(m).astype(np.float32); return cv2.resize(m, (N, N), interpolation=cv2.INTER_AREA) > 0.5
tgt = norm(tgt_raw)

def render(path, ch, size=600, var=None):
    f = ImageFont.truetype(path, size)
    if var:
        try: f.set_variation_by_axes(var)
        except Exception: pass
    im = Image.new("L", (1600, 1200), 0); ImageDraw.Draw(im).text((300, 150), ch, font=f, fill=255)
    a = np.array(im) > 127; return a if a.any() else None

def left_element(H):
    """Split H into components; the left element = components whose centroid is left of the widest vertical gap,
    or (if the H is one piece) the columns left of the thinnest column-run in the middle third."""
    H = crop(H); n, lab, st, cen = cv2.connectedComponentsWithStats(H.astype(np.uint8), 8)
    if n > 2:
        big = [i for i in range(1, n) if st[i, 4] > 0.02 * H.sum()]
        big.sort(key=lambda i: cen[i][0])
        return crop(np.isin(lab, big[:1]) | (np.isin(lab, [i for i in range(1, n) if st[i, 4] <= 0.02 * H.sum() and cen[i][0] < cen[big[0]][0] + st[big[0], 2] / 2])))
    w = H.shape[1]; prof = H.sum(0); a, b = int(w * 0.3), int(w * 0.62)
    cut = a + int(np.argmin(prof[a:b])); return crop(H[:, :cut])

def compose(path, var=None, gap_frac=0.04):
    H = render(path, "H", var=var); h = render(path, "h", var=var)
    if H is None or h is None: return None
    L = left_element(H); Hc = crop(H); hh = crop(h)
    capH = Hc.shape[0]
    hh = cv2.resize(hh.astype(np.uint8), (int(hh.shape[1] * capH / hh.shape[0]), capH), interpolation=cv2.INTER_AREA) > 0
    Lr = cv2.resize(L.astype(np.uint8), (L.shape[1], capH), interpolation=cv2.INTER_AREA) > 0 if L.shape[0] != capH else L
    gap = int(capH * gap_frac)
    out = np.zeros((capH, Lr.shape[1] + gap + hh.shape[1]), bool)
    out[:, :Lr.shape[1]] |= Lr; out[:, Lr.shape[1] + gap:] |= hh
    return out

def score(m):
    best = (0, 0, None)
    for sh in np.linspace(-0.3, 0.3, 13):
        Hh, Ww = m.shape; M = np.float32([[1, sh, max(0, -sh * Hh)], [0, 1, 0]])
        s = cv2.warpAffine(m.astype(np.uint8), M, (int(Ww + abs(sh) * Hh) + 2, Hh)) > 0
        n = norm(s)
        for dx in (-8, -4, 0, 4, 8):
            for dy in (-6, 0, 6):
                t = np.roll(np.roll(n, dx, 1), dy, 0); iou = (t & tgt).sum() / (t | tgt).sum()
                if iou > best[0]: best = (iou, sh, t)
    return best

if __name__ == "__main__":
    fonts = sorted(glob.glob(f"{HB}/fonts_bl/*.ttf"))
    rows = []
    for p in fonts:
        nm = os.path.basename(p)[:-4]
        for var in ([None] if "wght" not in nm else ([[700], [900]] if "opsz" not in nm else [[24, 700], [24, 900]])):
            for gf in (0.0, 0.05):
                m = compose(p, var, gf)
                if m is None: continue
                iou, sh, t = score(m); rows.append((iou, nm + ("" if var is None else str(var)), gf, sh, m, t))
    rows.sort(key=lambda r: -r[0])
    seen = set(); top = []
    for r in rows:
        if r[1] in seen: continue
        seen.add(r[1]); top.append(r)
    for iou, nm, gf, sh, *_ in top: print(f"{iou:.3f} {nm:38s} gap {gf} shear {sh:+.2f}")
    cell = 240; T = top[:8]
    B = Image.new("RGB", ((len(T) + 1) * cell, 2 * cell + 34), (255, 255, 255)); d = ImageDraw.Draw(B)
    B.paste(Image.fromarray(((~tgt) * 255).astype(np.uint8)).resize((cell - 20, cell - 20)).convert("RGB"), (10, 10)); d.text((10, 2 * cell + 6), "1983 fused", fill=(0, 0, 0))
    for i, (iou, nm, gf, sh, m, t) in enumerate(T, 1):
        sc = (cell - 20) / max(m.shape); g = cv2.resize(m.astype(np.uint8) * 255, (int(m.shape[1] * sc), int(m.shape[0] * sc)))
        tile = Image.new("L", (cell - 20, cell - 20), 255); tile.paste(Image.fromarray(255 - g), ((cell - 20 - g.shape[1]) // 2, (cell - 20 - g.shape[0]) // 2))
        B.paste(tile.convert("RGB"), (i * cell + 10, 10))
        ov = np.full((N, N, 3), 255, np.uint8); ov[tgt & ~t] = (230, 80, 80); ov[t & ~tgt] = (80, 120, 230); ov[t & tgt] = (40, 40, 40)
        B.paste(Image.fromarray(ov).resize((cell - 20, cell - 20)), (i * cell + 10, cell + 10))
        d.text((i * cell + 10, 2 * cell + 2), nm[:30], fill=(0, 0, 0)); d.text((i * cell + 10, 2 * cell + 16), f"IoU {iou:.3f}", fill=(0, 0, 0))
    B.save(f"{HB}/hhs/compose_board.png")
