import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text, to_rgba_ink
from teemock import place_print, sheet, chest

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/camelot"
W = 3000

def crop_ink(a):
    ys, xs = np.where(a > 0.5); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def line(text, f, ax, tr, xs, target_w):
    a, _ = render_text(text, f, 140, ax, tr, xs)
    sub = crop_ink(a)
    return cv2.resize(sub, (target_w, int(sub.shape[0] * target_w / sub.shape[1])), interpolation=cv2.INTER_AREA)

logo = line("Camelot Music", "GrenzeGotisch[wght].ttf", {"wght": 700}, 0.01, 0.86, W - 120) > 0.5
small_txt = "CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974"
small = line(small_txt, "Jost[wght].ttf", {"wght": 560}, 0.16, 1.0, int(W * 0.70)) > 0.5

def raised(ink, dx=34, dy=30, gap=12):
    """Single-color raised-letter effect: offset shadow, separated from the face by a knockout gap."""
    H, Wd = ink.shape
    pad = max(dx, dy) + gap + 4
    face = np.pad(ink, pad)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * gap + 1, 2 * gap + 1))
    halo = cv2.dilate(face.astype(np.uint8), k) > 0
    shadow = np.zeros_like(face)
    for t in np.linspace(0, 1, 18):  # extrude the shadow along the offset vector
        M = np.float32([[1, 0, dx * t], [0, 1, dy * t]])
        shadow |= cv2.warpAffine(face.astype(np.uint8), M, (face.shape[1], face.shape[0])) > 0
    return face | (shadow & ~halo)

def stack(top, bottom, gap_ratio=0.16):
    gap = int(top.shape[0] * gap_ratio)
    Wd = max(top.shape[1], bottom.shape[1])
    out = np.zeros((top.shape[0] + gap + bottom.shape[0], Wd), bool)
    out[:top.shape[0], (Wd - top.shape[1]) // 2:(Wd - top.shape[1]) // 2 + top.shape[1]] = top
    out[top.shape[0] + gap:, (Wd - bottom.shape[1]) // 2:(Wd - bottom.shape[1]) // 2 + bottom.shape[1]] = bottom
    return out

designs = {
    "flat": stack(logo, small),
    "raised": stack(raised(logo), small, 0.10),
    "flat_logo_only": logo,
}
INKS = {"white": (255, 255, 255), "black": (17, 17, 17), "gold": (184, 134, 11)}
paths = {}
for k, ink in designs.items():
    ink = np.pad(ink, 16)
    for n, rgb in INKS.items():
        p = f"{D}/camelot_hattiesburg_{k}_{n}.png"
        to_rgba_ink(ink, rgb).save(p, dpi=(300, 300)); paths[(k, n)] = p
    print(k, ink.shape, round(ink.shape[1] / 300, 2), "x", round(ink.shape[0] / 300, 2), "in")

combos = [("flat", "white", (20, 20, 22), "Black tee / flat / white"),
          ("raised", "white", (20, 20, 22), "Black tee / raised / white"),
          ("raised", "gold", (20, 20, 22), "Black tee / raised / gold"),
          ("flat", "black", (236, 228, 210), "Natural tee / flat / black"),
          ("raised", "black", (236, 228, 210), "Natural tee / raised / black"),
          ("raised", "white", (38, 52, 92), "Navy tee / raised / white")]
sheet([chest(paths[(k, n)], g, print_w_in=10.5, W=560, top_in=3.0, label=l) for k, n, g, l in combos], cols=3).save(f"{D}/camelot_mocks.jpg", quality=88)
print("done")
