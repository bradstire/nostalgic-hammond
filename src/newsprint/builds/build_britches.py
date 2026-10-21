import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text, to_rgba_ink, SS
from teemock import place_print, sheet, chest
from PIL import Image

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/britches"
W = 3000  # 10.0 in @300dpi
LOGO_F, LOGO_AX, LOGO_TR, LOGO_XS = "Inter[opsz,wght].ttf", {"wght": 580, "opsz": 32}, -0.042, 1.04
SMALL_F, SMALL_AX, SMALL_TR = "Inter[opsz,wght].ttf", {"wght": 430, "opsz": 14}, 0.07

def crop_ink(a):
    ys, xs = np.where(a > 0.5); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def line(text, f, ax, tr, xs, target_w):
    a, bb = render_text(text, f, 120, ax, tr, xs)
    sub = crop_ink(a)
    h = int(sub.shape[0] * target_w / sub.shape[1])
    return cv2.resize(sub, (target_w, h), interpolation=cv2.INTER_AREA)

logo = line("mississippi britches", LOGO_F, LOGO_AX, LOGO_TR, LOGO_XS, W)
xh = logo.shape[0]
variants = {
    "logo": None,
    "hours": "OPEN MON-SAT 10AM-9PM SUN 1PM-5PM CLOVERLEAF MALL",
    "cloverleaf": "CLOVERLEAF MALL · HATTIESBURG, MISS.",
}
outs = {}
for k, small in variants.items():
    if small is None:
        a = logo
    else:
        sw = int(W * (0.82 if k == "hours" else 0.62))
        sm = line(small, SMALL_F, SMALL_AX, SMALL_TR, 1.0, sw)
        gap = int(xh * 0.30)
        a = np.zeros((logo.shape[0] + gap + sm.shape[0], W), np.float32)
        a[:logo.shape[0]] = logo
        x0 = (W - sw) // 2
        a[logo.shape[0] + gap:, x0:x0 + sw] = sm
    ink = a > 0.5
    pad = 20
    ink = np.pad(ink, pad)
    for name, rgb in (("white", (255, 255, 255)), ("cream", (239, 230, 210))):
        p = f"{D}/britches_{k}_{name}.png"
        to_rgba_ink(ink, rgb).save(p, dpi=(300, 300))
        outs[(k, name)] = p
    print(k, ink.shape, "=", round(ink.shape[1] / 300, 2), "x", round(ink.shape[0] / 300, 2), "in")

GARMENTS = {"Maroon": (92, 30, 44), "Cardinal": (139, 30, 46), "Burgundy": (110, 34, 52), "Brick (garment-dyed)": (150, 62, 58)}
tiles = []
for k in variants:
    for name in ("white", "cream"):
        tiles.append(place_print(outs[(k, name)], GARMENTS["Maroon"], print_w_in=10.0, W=520, top_in=3.2,
                                 label=f"Maroon / {k} / {name}"))
sheet(tiles, cols=3).save(f"{D}/britches_layouts.jpg", quality=88)
tiles = [chest(outs[("hours", "cream")], rgb, print_w_in=10.0, W=520, top_in=3.2, label=f"{g} / hours / cream")
         for g, rgb in GARMENTS.items()]
sheet(tiles, cols=4).save(f"{D}/britches_garments.jpg", quality=88)
print("mocks done")
