"""Culpepper hat BACK embroidery: arched CULPEPPER over straight BODY & PAINT SHOP.
Printful dad-hat back area: 2.25-3.0in W x 0.75-1.0in H (above the closure). Text >= 0.25in, strokes >= 0.05in."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text
from PIL import Image
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/hats"
DPI = 300
F, AX = "Jost[wght].ttf", {"wght": 900}   # Futura-family caps, like the ad's headline

def glyph(ch, h):
    a, _ = render_text(ch, F, 220, AX, 0.0)
    ys, xs = np.where(a > 0.5); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return cv2.resize(a, (max(1, int(a.shape[1] * h / a.shape[0])), h), interpolation=cv2.INTER_AREA)

def arched(text, cap_h, radius, track):
    """Letters on a circle arc, centre of the word highest (classic back-of-cap arch)."""
    gl = [glyph(c, cap_h) if c != " " else None for c in text]
    widths = [g.shape[1] if g is not None else int(cap_h * 0.35) for g in gl]
    total = sum(widths) + track * (len(text) - 1)
    M = cap_h * 3
    W = int(total + 2 * M); H = int(cap_h * 2 + total ** 2 / (8 * radius) + 2 * M)
    canvas = np.zeros((H, W), np.float32)
    cx = W / 2; cy = M + cap_h + radius                 # arc apex sits at y = M + cap_h
    s = -total / 2
    for g, w in zip(gl, widths):
        mid = s + w / 2; s += w + track
        if g is None: continue
        theta = mid / radius
        # glyph centre sits half a cap-height above the arc (baseline on the arc)
        r_c = radius + cap_h / 2
        gx = cx + r_c * np.sin(theta); gy = cy - r_c * np.cos(theta)
        img = Image.fromarray((g * 255).astype(np.uint8))
        rot = np.array(img.rotate(-np.degrees(theta), expand=True, resample=Image.BICUBIC)) / 255.0
        x0 = int(round(gx - rot.shape[1] / 2)); y0 = int(round(gy - rot.shape[0] / 2))
        canvas[y0:y0 + rot.shape[0], x0:x0 + rot.shape[1]] = np.maximum(canvas[y0:y0 + rot.shape[0], x0:x0 + rot.shape[1]], rot)
    m = canvas > 0.5
    ys, xs = np.where(m); return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def straight(text, cap_h, xs=1.0, track=0.04):
    a, _ = render_text(text, F, 220, AX, track, xs)
    ys, x_ = np.where(a > 0.5); a = a[ys.min():ys.max() + 1, x_.min():x_.max() + 1]
    return cv2.resize(a, (int(a.shape[1] * cap_h / a.shape[0]), cap_h), interpolation=cv2.INTER_AREA) > 0.5

top = arched("CULPEPPER", int(0.32 * DPI), radius=int(5.5 * DPI), track=int(0.035 * DPI))
bot = straight("BODY & PAINT", int(0.26 * DPI), xs=1.0, track=0.07)
if bot.shape[1] > int(2.95 * DPI):
    sc = 2.95 * DPI / bot.shape[1]
    bot = cv2.resize(bot.astype(np.float32), (int(bot.shape[1] * sc), int(bot.shape[0] * sc)), interpolation=cv2.INTER_AREA) > 0.5
gap = int(0.08 * DPI)
Wd = max(top.shape[1], bot.shape[1]); Ht = top.shape[0] + gap + bot.shape[0]
out = np.zeros((Ht, Wd), bool)
out[:top.shape[0], (Wd - top.shape[1]) // 2:(Wd - top.shape[1]) // 2 + top.shape[1]] = top
out[top.shape[0] + gap:, (Wd - bot.shape[1]) // 2:(Wd - bot.shape[1]) // 2 + bot.shape[1]] = bot
out = cv2.dilate(out.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))) > 0   # +3px stroke gain (clears 0.05in min line)
out = np.pad(out, 12)
rgba = np.zeros((*out.shape, 4), np.uint8); rgba[out, :3] = (17, 17, 17); rgba[out, 3] = 255
Image.fromarray(rgba, "RGBA").save(f"{D}/hat_culpepper_back_black.png", dpi=(DPI, DPI))
dt = cv2.distanceTransform(out.astype(np.uint8), cv2.DIST_L2, 5); v = dt[dt > 0]
stroke = float(np.percentile(v[v >= np.percentile(v, 50)], 5) * 2) / DPI
print(f"back: {out.shape[1] / DPI:.2f} x {out.shape[0] / DPI:.2f} in (area 2.25-3.0 x 0.75-1.0); "
      f"cap heights 0.32/{bot.shape[0] / DPI:.2f} in; est. min stroke {stroke:.3f} in")
