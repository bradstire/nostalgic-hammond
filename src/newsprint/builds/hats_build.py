"""Embroidery hat fronts (Printful dad hat: 3.5-4.0in W x 1.75-2.0in H; text >= 0.25in; lines >= 0.05in = 15px @300dpi).
Each file: PNG 300dpi, flat thread colors, binary alpha. Embroidery-check: min stroke + min text height reported."""
import sys, numpy as np, cv2, re
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text, render_svg
from PIL import Image, ImageDraw
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
D = f"{HB}/hats"
DPI = 300

def crop(a):
    ys, xs = np.where(a > 0.5); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def word(text, font, ax=None, w=None, h=None, tr=0.0, xs=1.0, round_px=0):
    a, _ = render_text(text, font, 170, ax, tr, xs)
    if round_px: a = cv2.GaussianBlur(a, (0, 0), round_px)
    a = crop(a)
    sc = min(w / a.shape[1] if w else 1e9, h / a.shape[0] if h else 1e9)
    return cv2.resize(a, (int(a.shape[1] * sc), int(a.shape[0] * sc)), interpolation=cv2.INTER_AREA) > 0.5
def vstack(parts, gaps):
    W = max(p.shape[1] for p in parts); H = sum(p.shape[0] for p in parts) + sum(gaps)
    out = np.zeros((H, W), bool); y = 0
    for i, p in enumerate(parts):
        x = (W - p.shape[1]) // 2; out[y:y + p.shape[0], x:x + p.shape[1]] = p; y += p.shape[0] + (gaps[i] if i < len(gaps) else 0)
    return out
def min_stroke(m):
    """Approx thinnest stroke in px via distance transform on ink skeleton-ish percentile."""
    dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    vals = dt[dt > 0]; return float(np.percentile(vals[vals >= np.percentile(vals, 50)], 5) * 2) if vals.size else 0
def gain(m, px):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * px + 1, 2 * px + 1))
    return cv2.dilate(m.astype(np.uint8), k) > 0

def save(m, color, name, notes):
    m = np.pad(m, 12)
    rgba = np.zeros((*m.shape, 4), np.uint8); rgba[m, :3] = color; rgba[m, 3] = 255
    Image.fromarray(rgba, "RGBA").save(f"{D}/{name}.png", dpi=(DPI, DPI))
    w_in, h_in = m.shape[1] / DPI, m.shape[0] / DPI
    ok = (w_in <= 4.05 and h_in <= 2.05)
    print(f"{name}: {w_in:.2f} x {h_in:.2f} in  size_ok={ok}  {notes}")
    return f"{D}/{name}.png"

files = {}
# 1) Hub City — authentic SR headline letterforms, two lines, black thread on white/stone hat
hc = cv2.imread(f"{HB}/hubcity/sr_gray_3150.png", 0)
hb_ = hc[65:241, 89:2615] < 140
hb_[150 - 65:, 2572 - 89:] = False   # drop "May 22, 1966" that abuts the Y
head = crop(hb_.astype(np.float32))      # "HUB CITY DRAG RACEWAY" (without SUNDAY block)
H_ = head.shape[0]; xs = np.where(head.any(axis=0))[0]
# split after 'CITY' : find the widest gap in the first 55% of width
cols = head.any(axis=0); gaps = []; run = 0
for x in range(len(cols)):
    if not cols[x]: run += 1
    else:
        if run > 25: gaps.append((x - run, x))
        run = 0
cut = sorted(gaps, key=lambda g: abs((g[0] + g[1]) / 2 - head.shape[1] * 0.42))[0]
l1, l2 = crop(head[:, :cut[0]].astype(np.float32)) > 0.5, crop(head[:, cut[1]:].astype(np.float32)) > 0.5
W_in = 3.6 * DPI
l2s = cv2.resize(l2.astype(np.float32), (int(W_in), int(l2.shape[0] * W_in / l2.shape[1])), interpolation=cv2.INTER_AREA) > 0.5
l1s = cv2.resize(l1.astype(np.float32), (int(l1.shape[1] * l2s.shape[0] / l1.shape[0]), l2s.shape[0]), interpolation=cv2.INTER_AREA) > 0.5
hub = vstack([l1s, l2s], [int(0.12 * DPI)])
hub = cv2.morphologyEx(hub.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
hub = gain(hub, 4)
files["hubcity"] = save(hub, (20, 20, 20), "hat_hubcity_black", f"cap height ~{l2s.shape[0] / DPI:.2f}in")

# 2) Camelot — 1974 sign wordmark, chain red (thread on navy/white/black hat)
cam = vstack([word("Camelot", "GrenzeGotisch[wght].ttf", {"wght": 880}, h=int(0.86 * DPI), xs=0.9), word("Music", "GrenzeGotisch[wght].ttf", {"wght": 880}, h=int(0.86 * DPI), xs=0.9)], [int(0.06 * DPI)])
cam = gain(cam, 2)
files["camelot"] = save(cam, (198, 40, 50), "hat_camelot_red", f"height {cam.shape[0] / DPI:.2f}in")
files["camelot_w"] = save(cam, (250, 250, 250), "hat_camelot_white", "white thread (black/navy hat)")

# 3) Mississippi Britches — logotype, white/cream thread on maroon/navy hat
br = vstack([word("mississippi", "Inter[opsz,wght].ttf", {"wght": 760, "opsz": 32}, w=int(3.5 * DPI), tr=-0.03, xs=1.04), word("britches", "Inter[opsz,wght].ttf", {"wght": 760, "opsz": 32}, h=None, w=int(2.55 * DPI), tr=-0.03, xs=1.04)], [int(0.08 * DPI)])
br = gain(br, 2)
files["britches"] = save(br, (239, 230, 210), "hat_britches_cream", f"x-height ok, height {br.shape[0] / DPI:.2f}in")

# 3b) Britches wooden-nickel badge (1971 token): arched name + HATTIESBURG, 1.95in circle
R = int(0.975 * DPI); C = R + 10
badge = np.zeros((2 * C, 2 * C), np.uint8)
cv2.circle(badge, (C, C), R, 1, 18)                                   # outer ring (0.06in)
def arc_text(img, text, radius, start_deg, end_deg, font, size_px, top=True):
    n = len(text); angs = np.linspace(start_deg, end_deg, n)
    for ch, a in zip(text, angs):
        if ch == " ": continue
        g = word(ch, font, None, h=size_px) if ch.isalpha() else word(ch, font, None, h=int(size_px * 0.9))
        th = np.deg2rad(a)
        rot = (90 - a) if top else (-90 - a)
        gi = Image.fromarray((g * 255).astype(np.uint8)).rotate(rot, expand=True, resample=Image.BICUBIC)
        ga = np.array(gi) > 127
        cx = int(C + radius * np.cos(th)); cy = int(C - radius * np.sin(th))
        y0, x0 = cy - ga.shape[0] // 2, cx - ga.shape[1] // 2
        img[y0:y0 + ga.shape[0], x0:x0 + ga.shape[1]] |= ga
txt_h = int(0.25 * DPI)
arc_text(badge, "MISSISSIPPI BRITCHES", R - 58, 158, 22, "Graduate-Regular.ttf", txt_h, top=True)
arc_text(badge, "HATTIESBURG", R - 58, 214, 326, "Graduate-Regular.ttf", txt_h, top=False)
star = word("★", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf".split("/")[-1], None, h=60) if False else None
mid = word("1971", "Graduate-Regular.ttf", None, h=int(0.36 * DPI), tr=0.04)
badge[C - mid.shape[0] // 2:C - mid.shape[0] // 2 + mid.shape[0], C - mid.shape[1] // 2:C - mid.shape[1] // 2 + mid.shape[1]] |= mid
Image.fromarray(((badge > 0) * 255).astype(np.uint8)).save(f"{D}/concept_britches_nickel_badge_print.png", dpi=(DPI, DPI))  # print/patch concept, not embroidery

# 4) Albert Speed's — two-line sign lettering, rounded (neon), red thread on cream hat
sp = vstack([word("ALBERT", "Archivo[wdth,wght].ttf", {"wght": 880, "wdth": 82}, h=int(0.42 * DPI), tr=0.08, round_px=6),
             word("SPEED'S", "Archivo[wdth,wght].ttf", {"wght": 880, "wdth": 82}, h=int(0.62 * DPI), tr=0.05, round_px=6),
             word("RESTAURANT", "Archivo[wdth,wght].ttf", {"wght": 880, "wdth": 82}, w=int(3.7 * DPI), h=int(0.42 * DPI), tr=0.08, round_px=6)],
            [int(0.08 * DPI), int(0.08 * DPI)])
sp = gain(sp, 2)
files["speeds"] = save(sp, (178, 46, 34), "hat_speeds_red", "2nd line height check below")

# 5) HHS — reconstructed 1983 Old English H, single color
svg = open(f"{HB}/ref/hhs/hhs_oldenglish_H_s9.svg").read()
w0, h0 = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', svg)[0]]
hh = int(1.85 * DPI); H_h = render_svg(svg, int(w0 * hh / h0), hh)
files["hhs_p"] = save(H_h, (58, 16, 85), "hat_hhs_oldenglishH_purple", "purple thread on white/natural hat")
files["hhs_g"] = save(H_h, (184, 134, 11), "hat_hhs_oldenglishH_gold", "gold thread on black hat")

# embroidery checks (stroke + text heights)
for k, p in files.items():
    a = np.array(Image.open(p))[..., 3] > 127
    print(f"  check {k}: est. min stroke {min_stroke(a) / DPI:.3f}in (need >= 0.05)")
