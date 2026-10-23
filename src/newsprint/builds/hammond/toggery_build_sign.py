"""Toggery Shop (105 W. Thomas St., Hammond) — the projecting Art Deco neon blade sign, redrawn flat (front view)
from the color photo in Brad's asset dump (IMG_7190). Geometry measured off the photo (x3 from the 500x950 crop):
disc top with 'T', vertical panel O-G-G-E-R-Y, paired fin tubes on the right, three-tube mounting arm to the left,
wide SHOP panel with ribs + tube below. Letters: high-contrast Roman like the sign's channel letters ->
Playfair Display Bold (OFL). Inks: wine (the shop's wine Carrara-glass front) + cream (unlit neon letters)."""
import sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
from hmlib import build_multi
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/toggery"
FONTS = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts"
WINE, CREAM = (110, 30, 42), (242, 232, 210)
SS = 2                                   # supersample
W, H = 1260 * SS, 2380 * SS
def P(v): return int(round(v * SS))
oy = 150                                 # shift down so the disc clears the top

def font(size, wght=700):
    f = ImageFont.truetype(f"{FONTS}/PlayfairDisplay[wght].ttf", int(size * SS))
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

wine = Image.new("L", (W, H), 0); cream = Image.new("L", (W, H), 0)
dw, dc = ImageDraw.Draw(wine), ImageDraw.Draw(cream)
cx = 870
# vertical panel + disc
px0, px1 = 738, 1032; disc_r = 196; disc_cy = 135 + oy
dw.rectangle([P(px0), P(disc_cy), P(px1), P(1690 + oy)], fill=255)
dw.ellipse([P(cx - disc_r), P(disc_cy - disc_r), P(cx + disc_r), P(disc_cy + disc_r)], fill=255)
# neon ring around the disc (cream) and inset border on the panels (cream keyline)
ring = 10
dc.ellipse([P(cx - disc_r + 18), P(disc_cy - disc_r + 18), P(cx + disc_r - 18), P(disc_cy + disc_r - 18)], outline=255, width=P(ring))
# mask the ring where the panel continues below the disc
dc.rectangle([P(px0 + 18), P(disc_cy + 60), P(px1 - 18), P(disc_cy + disc_r)], fill=0)
dc.line([P(px0 + 18 + ring / 2), P(disc_cy + 80), P(px0 + 18 + ring / 2), P(1690 + oy - 18)], fill=255, width=P(ring))
dc.line([P(px1 - 18 - ring / 2), P(disc_cy + 80), P(px1 - 18 - ring / 2), P(1690 + oy - 18)], fill=255, width=P(ring))
# mounting arm: three tubes from the disc to the wall (left)
for i, y in enumerate((70, 122, 174)):
    dw.rounded_rectangle([P(300), P(y + oy - 17), P(cx - 60), P(y + oy + 17)], radius=P(17), fill=255)
dw.rectangle([P(270), P(40 + oy), P(318), P(205 + oy)], fill=255)        # wall bracket
# paired fin tubes on the right edge, between letters
for y in (465, 700, 935, 1170, 1405):
    for dy in (-20, 20):
        dw.rounded_rectangle([P(px1 - 10), P(y + dy - 9 + oy), P(px1 + 92), P(y + dy + 9 + oy)], radius=P(9), fill=255)
# SHOP panel (wider, extends toward the wall) + inset keyline
sx0, sx1, sy0, sy1 = 315, 1140, 1665 + oy, 1986 + oy
dw.rectangle([P(sx0), P(sy0), P(sx1), P(sy1)], fill=255)
dc.rectangle([P(sx0 + 18), P(sy0 + 18), P(sx1 - 18), P(sy1 - 18)], outline=255, width=P(ring))
dw.rounded_rectangle([P(sx1 - 10), P((sy0 + sy1) / 2 - 9), P(sx1 + 92), P((sy0 + sy1) / 2 + 9)], radius=P(9), fill=255)
# ribs + tube under the SHOP panel (left end)
for x in (345, 410, 475):
    dw.rounded_rectangle([P(x), P(sy1 - 5), P(x + 34), P(sy1 + 215)], radius=P(17), fill=255)
dw.rounded_rectangle([P(470), P(sy1 + 40), P(990), P(sy1 + 74)], radius=P(17), fill=255)
dw.rounded_rectangle([P(950), P(sy1 + 40), P(984), P(sy1 + 150)], radius=P(17), fill=255)

# letters (cream), centred on the panel / disc
def letter(ch, cxl, cyl, cap):
    f = font(cap * 1.36)
    bb = dc.textbbox((0, 0), ch, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    dc.text((P(cxl) - w / 2 - bb[0], P(cyl) - h / 2 - bb[1]), ch, font=f, fill=255)
cap = 150
letter("T", cx, disc_cy + 8, cap)
for i, ch in enumerate("OGGERY"):
    letter(ch, cx, 345 + oy + i * 234, cap)
f = font(170 * 1.36)
txt = "SHOP"; bb = dc.textbbox((0, 0), txt, font=f, spacing=0)
# letter-spaced SHOP
chars = list(txt); ws = [dc.textbbox((0, 0), c, font=f)[2] - dc.textbbox((0, 0), c, font=f)[0] for c in chars]
track = P(26); tot = sum(ws) + track * (len(chars) - 1); x = P((sx0 + sx1) / 2) - tot / 2
for c, w in zip(chars, ws):
    b = dc.textbbox((0, 0), c, font=f); hh = b[3] - b[1]
    dc.text((x - b[0], P((sy0 + sy1) / 2) - hh / 2 - b[1]), c, font=f, fill=255); x += w + track

wa = np.array(wine) > 127; ca = np.array(cream) > 127
wa &= ~ca
# downsample to working res (keeps edges clean for potrace)
wa = cv2.resize(wa.astype(np.float32), (W // SS * 2, H // SS * 2), interpolation=cv2.INTER_AREA) > 0.5
ca = cv2.resize(ca.astype(np.float32), (W // SS * 2, H // SS * 2), interpolation=cv2.INTER_AREA) > 0.5
ys, xs = np.where(wa | ca); y0, y1, x0, x1 = ys.min() - 20, ys.max() + 21, xs.min() - 20, xs.max() + 21
wa, ca = wa[y0:y1, x0:x1], ca[y0:y1, x0:x1]
Hh, Ww = wa.shape
build_multi([(wa, WINE), (ca, CREAM)], Ww, Hh, 1500, f"{D}/toggery_sign")             # 5 in wide x ~10 in tall
build_multi([(wa, WINE)], Ww, Hh, 1500, f"{D}/toggery_sign_1color_wine")               # letters = garment (natural/white)
print(Ww, Hh)
