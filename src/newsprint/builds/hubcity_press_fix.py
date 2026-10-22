"""Hub City v3 = v2 art (approved) + press compensation for DTG on a WHITE cotton tee (MC1082, no underbase).
Measured on v2: smallest copy ~14pt (fine); its strokes ~1pt / 4-5px (at the floor); halftones carry thousands of
dots and shadow openings under 0.007in -> on cotton, highlight dots drop out and shadow holes plug.
Fix: (1) small-copy strokes rebuilt to >= 1.5pt (0.021in) on their own centreline; (2) halftone minimum feature
0.01in: highlight dots grown to a 3px disc, shadow openings opened to a 3px disc. Screen ruling + look unchanged.
Also renders an ink-spread simulation (blur sigma 1.2px, threshold 0.42) before/after for the press-check sheet."""
import sys, numpy as np, cv2
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/lib")
from PIL import Image, ImageDraw, ImageFont
from embcheck import enforce_min_stroke
from teemock import place_print
D = f"{HB}/hubcity/press"
SRC = "/home/claude/nh-recovered/print-assets-repo/hattiesburg/hubcity_ad_front.png"
m = np.array(Image.open(SRC))[..., 3] > 127
boxes = np.load(f"{D}/photo_boxes.npy")
pm = np.zeros_like(m)
for x, y, w, h in boxes: pm[y:y + h, x:x + w] = True

# (1) text/linework: >= 1.5pt strokes (tips left tapered)
txt = m & ~pm
txt2 = enforce_min_stroke(txt, 0.021, margin_px=0)

# (2) halftone: minimum printable feature 0.01in (3px disc)
ph = m & pm
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)); disc[0, 0] = disc[0, 2] = disc[2, 0] = disc[2, 2] = 0
n, lab, st, cen = cv2.connectedComponentsWithStats(ph.astype(np.uint8), 8)
grow = np.zeros_like(ph)
for i in np.where(st[1:, 4] < 7)[0] + 1:
    cx, cy = int(round(cen[i][0])), int(round(cen[i][1])); grow[max(0, cy - 1):cy + 2, max(0, cx - 1):cx + 2] |= disc[:min(3, ph.shape[0] - cy + 1), :min(3, ph.shape[1] - cx + 1)].astype(bool)[:grow[max(0, cy - 1):cy + 2, max(0, cx - 1):cx + 2].shape[0], :grow[max(0, cy - 1):cy + 2, max(0, cx - 1):cx + 2].shape[1]]
ph2 = ph | (grow & pm)
inv = (~ph2) & pm
n, lab, st, cen = cv2.connectedComponentsWithStats(inv.astype(np.uint8), 8)
opn = np.zeros_like(ph)
for i in np.where(st[1:, 4] < 7)[0] + 1:
    cx, cy = int(round(cen[i][0])), int(round(cen[i][1])); opn[max(0, cy - 1):cy + 2, max(0, cx - 1):cx + 2] = True
ph2 = ph2 & ~(opn & pm & cv2.erode(pm.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool))
v3 = txt2 | ph2
rgba = np.zeros((*v3.shape, 4), np.uint8); rgba[v3, :3] = 17; rgba[v3, 3] = 255
Image.fromarray(rgba, "RGBA").save(f"{D}/hubcity_ad_front_v3.png", dpi=(300, 300))
print("v3 saved", v3.shape, "ink v2 %.3f v3 %.3f" % (m.mean(), v3.mean()))

def press(mask):   # ink spread on cotton: tiny dots vanish, tiny holes plug
    return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.2) > 0.42

def fabric(mask, scale=1):
    """Render printed mask as black ink on white cotton with weave texture."""
    h, w = mask.shape; rng = np.random.default_rng(3)
    weave = (np.sin(np.arange(w)[None, :] * 1.9) * np.sin(np.arange(h)[:, None] * 1.9) * 6 + rng.normal(0, 4, (h, w)))
    base = 244 + weave
    ink = 34 + rng.normal(0, 6, (h, w))
    out = np.where(mask, ink, base).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out).convert("RGB")

# press-check sheet
crops = {"Smallest copy ('Would you believe...' paragraph), 100% = 1in": (slice(2380, 2620), slice(60, 1260)),
         "Ford Mustang photo highlights + shadows, 100%": (slice(1150, 1390), slice(300, 1500)),
         "Corvair photo, 100%": (slice(1300, 1540), slice(1750, 2950))}
rows = []
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
for title, (ys, xs) in crops.items():
    a, b, c = fabric(press(m[ys, xs])), fabric(press(v3[ys, xs])), fabric(m[ys, xs])
    strip = Image.new("RGB", (a.width * 3 + 40, a.height + 40), (255, 255, 255)); d = ImageDraw.Draw(strip)
    for i, (im, lab_) in enumerate(((c, "file as designed"), (a, "v2 printed (simulated)"), (b, "v3 printed (simulated)"))):
        strip.paste(im, (i * (a.width + 20), 36)); d.text((i * (a.width + 20), 6), lab_, fill=(0, 0, 0), font=F)
    rows.append((title, strip))
tee = place_print(f"{D}/hubcity_ad_front_v3.png", (250, 250, 250), None, 10.5, 1100, 3.0, label="White tee (MC1082) — Hub City v3 at true 10.5in width")
Wd = max(tee.width, max(s.width for _, s in rows)); Hs = tee.height + sum(s.height + 50 for _, s in rows) + 20
sheet = Image.new("RGB", (Wd, Hs), (236, 234, 230)); d = ImageDraw.Draw(sheet)
sheet.paste(tee, ((Wd - tee.width) // 2, 0)); y = tee.height + 10
for title, s in rows:
    d.text((10, y), title, fill=(30, 30, 30), font=F); sheet.paste(s, (10, y + 30)); y += s.height + 50
sheet.save(f"{D}/hubcity_white_tee_press_check.jpg", quality=90)
print("sheet", sheet.size)
