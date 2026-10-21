"""Dad-hat mockups (front + back) for embroidery files. Scale-true: PPI px per inch of hat."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/hats"
PPI = 90
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def _art(path):
    a = Image.open(path).convert("RGBA")
    w, h = a.size
    return a.resize((max(1, int(w / 300 * PPI)), max(1, int(h / 300 * PPI))), Image.LANCZOS)

def _shade(c, k): return tuple(int(max(0, min(255, v * k))) for v in c)

def front(path, hat, label):
    W, H = int(8.2 * PPI), int(6.4 * PPI)
    im = Image.new("RGB", (W, H), (236, 233, 226)); d = ImageDraw.Draw(im)
    cx = W // 2; base = int(4.6 * PPI)
    # bill (under crown)
    d.ellipse([cx - 3.9 * PPI, base - 0.55 * PPI, cx + 3.9 * PPI, base + 1.55 * PPI], fill=_shade(hat, 0.82))
    # crown: half-ellipse 7.0in wide, 4.0in tall
    d.pieslice([cx - 3.5 * PPI, base - 4.0 * PPI, cx + 3.5 * PPI, base + 4.0 * PPI], 180, 360, fill=hat)
    d.line([cx, base - 3.95 * PPI, cx, base], fill=_shade(hat, 0.9), width=2)          # centre seam
    d.ellipse([cx - 0.18 * PPI, base - 4.08 * PPI, cx + 0.18 * PPI, base - 3.86 * PPI], fill=_shade(hat, 0.9))  # button
    a = _art(path)
    y = int(base - 0.55 * PPI - a.size[1]); im.paste(a, (cx - a.size[0] // 2, y), a)
    d.text((10, H - 22), label, fill=(70, 70, 70), font=ImageFont.truetype(FONT, 14))
    return im

def back(path, hat, label):
    W, H = int(8.2 * PPI), int(6.4 * PPI)
    im = Image.new("RGB", (W, H), (236, 233, 226)); d = ImageDraw.Draw(im)
    cx = W // 2; base = int(5.2 * PPI)
    d.pieslice([cx - 3.5 * PPI, base - 4.0 * PPI, cx + 3.5 * PPI, base + 4.0 * PPI], 180, 360, fill=hat)
    d.line([cx, base - 3.95 * PPI, cx, base - 1.25 * PPI], fill=_shade(hat, 0.9), width=2)
    # closure opening (~2.6in wide, 1.2in tall arch) + strap
    d.pieslice([cx - 1.3 * PPI, base - 1.2 * PPI, cx + 1.3 * PPI, base + 1.2 * PPI], 180, 360, fill=(236, 233, 226))
    d.rectangle([cx - 1.45 * PPI, base - 0.28 * PPI, cx + 1.45 * PPI, base - 0.02 * PPI], fill=_shade(hat, 0.86))
    d.rectangle([cx + 0.55 * PPI, base - 0.34 * PPI, cx + 0.85 * PPI, base + 0.04 * PPI], fill=(176, 160, 120))  # buckle
    a = _art(path)
    y = int(base - 1.2 * PPI - 0.18 * PPI - a.size[1]); im.paste(a, (cx - a.size[0] // 2, y), a)
    d.text((10, H - 22), label, fill=(70, 70, 70), font=ImageFont.truetype(FONT, 14))
    return im

def sheet(ims, cols, out):
    w, h = ims[0].size; rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * w + (cols + 1) * 12, rows * h + (rows + 1) * 12), (255, 255, 255))
    for i, m in enumerate(ims):
        S.paste(m, (12 + (i % cols) * (w + 12), 12 + (i // cols) * (h + 12)))
    S.save(out, quality=90); return out

if __name__ == "__main__":
    STONE, WHITE, BLACK, NAVY, MAROON, CREAM, KHAKI = (196, 182, 150), (244, 242, 236), (34, 34, 36), (31, 42, 68), (104, 30, 40), (232, 222, 196), (186, 168, 128)
    sheet([front(f"{D}/hat_culpepper_duck_black.png", STONE, "Culpepper — FRONT: duck (black thread, stone hat)"),
           back(f"{D}/hat_culpepper_back_black.png", STONE, "Culpepper — BACK: arched CULPEPPER / BODY & PAINT")], 2, f"{D}/culpepper_hat_front_back_mock.jpg")
    sheet([front(f"{D}/hat_hubcity_black.png", WHITE, "Hub City — black on white"),
           front(f"{D}/hat_camelot_red.png", WHITE, "Camelot — red on white"),
           front(f"{D}/hat_camelot_white.png", NAVY, "Camelot — white on navy"),
           front(f"{D}/hat_britches_cream.png", MAROON, "Britches — cream on maroon"),
           front(f"{D}/hat_speeds_red.png", CREAM, "Speed's — red on cream"),
           front(f"{D}/hat_hhs_oldenglishH_purple.png", WHITE, "HHS H — purple on white"),
           front(f"{D}/hat_hhs_oldenglishH_gold.png", BLACK, "HHS H — gold on black"),
           front(f"{D}/hat_culpepper_duck_black.png", STONE, "Culpepper duck — front"),
           back(f"{D}/hat_culpepper_back_black.png", STONE, "Culpepper — back arch")], 3, f"{D}/hats_mocks.jpg")
    print("ok")
