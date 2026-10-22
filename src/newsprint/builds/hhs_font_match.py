"""Score blackletter capital H candidates against the H fused from 7 views of the 1983 HHS team photo.
Metric: IoU after bbox normalisation + small search over shear / aspect / offset (fabric + perspective tolerance)."""
import glob, os, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
FD = f"{HB}/fonts_bl"
N = 256

def norm(mask):
    ys, xs = np.where(mask); m = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1].astype(np.float32)
    return cv2.resize(m, (N, N), interpolation=cv2.INTER_AREA) > 0.5, m.shape[1] / m.shape[0]

tgt_raw = np.array(Image.open(f"{HB}/ref/hhs/h_fused_bw.png").convert("L")) < 128
tgt, tgt_aspect = norm(tgt_raw)

def glyph(path, ch="H", variation=None):
    f = ImageFont.truetype(path, 600)
    if variation:
        try: f.set_variation_by_axes(variation)
        except Exception: pass
    im = Image.new("L", (1400, 1100), 0); ImageDraw.Draw(im).text((200, 100), ch, font=f, fill=255)
    a = np.array(im) > 127
    return a if a.any() else None

def best_iou(m):
    best = (0, None, None)
    ys, xs = np.where(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    for sh in np.linspace(-0.3, 0.3, 13):
        Hh, Ww = m.shape; M = np.float32([[1, sh, max(0, -sh * Hh)], [0, 1, 0]])
        s = cv2.warpAffine(m.astype(np.uint8), M, (int(Ww + abs(sh) * Hh) + 2, Hh)) > 0
        n, _ = norm(s)
        for dx in (-8, -4, 0, 4, 8):
            for dy in (-6, 0, 6):
                t = np.roll(np.roll(n, dx, 1), dy, 0)
                iou = (t & tgt).sum() / (t | tgt).sum()
                if iou > best[0]: best = (iou, sh, t)
    return best

cands = []
for p in sorted(glob.glob(f"{FD}/*.ttf")):
    name = os.path.basename(p)[:-4]
    vars_ = [None]
    if "wght" in name: vars_ = [[400], [700], [900]] if "opsz" not in name else [[24, 400], [24, 700], [24, 900]]
    for v in vars_:
        g = glyph(p, "H", v)
        if g is None: continue
        iou, sh, t = best_iou(g)
        ys, xs = np.where(g); asp = (xs.max() - xs.min()) / (ys.max() - ys.min())
        cands.append((iou, f"{name}{'' if v is None else ' ' + str(v)}", sh, asp, t, p, v))
cands.sort(key=lambda c: -c[0])
print(f"target aspect {tgt_aspect:.2f}")
for iou, name, sh, asp, *_ in cands: print(f"{iou:.3f}  {name:40s} shear {sh:+.2f} aspect {asp:.2f}")

# visual board: target + top 12 glyphs (raw glyph, not warped) + overlay of warped vs target
cell = 220; top = cands[:12]
board = Image.new("RGB", ((len(top) + 1) * cell, cell * 2 + 30), (255, 255, 255)); d = ImageDraw.Draw(board)
board.paste(Image.fromarray(((~tgt) * 255).astype(np.uint8)).resize((cell - 20, cell - 20)).convert("RGB"), (10, 10)); d.text((10, cell * 2 + 8), "1983 fused", fill=(0, 0, 0))
for i, (iou, name, sh, asp, t, p, v) in enumerate(top, 1):
    g = glyph(p, "H", v); ys, xs = np.where(g); g = g[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sc = (cell - 20) / max(g.shape); gi = cv2.resize(g.astype(np.uint8) * 255, (int(g.shape[1] * sc), int(g.shape[0] * sc)))
    tile = Image.new("L", (cell - 20, cell - 20), 255); tile.paste(Image.fromarray(255 - gi), ((cell - 20 - gi.shape[1]) // 2, (cell - 20 - gi.shape[0]) // 2))
    board.paste(tile.convert("RGB"), (i * cell + 10, 10))
    ov = np.full((N, N, 3), 255, np.uint8); ov[tgt & ~t] = (230, 80, 80); ov[t & ~tgt] = (80, 120, 230); ov[t & tgt] = (40, 40, 40)
    board.paste(Image.fromarray(ov).resize((cell - 20, cell - 20)), (i * cell + 10, cell + 10))
    d.text((i * cell + 10, cell * 2 + 2), name[:28], fill=(0, 0, 0)); d.text((i * cell + 10, cell * 2 + 14), f"IoU {iou:.3f}", fill=(0, 0, 0))
board.save(f"{HB}/hhs/font_match_board.png")
