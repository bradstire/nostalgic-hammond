"""Printful Sublimation Socks — basic template (same art both sides): 4.49 x 18.85 in (size M) @300dpi.
Full-bleed RGB JPEG/PNG, sRGB. Top of strip = cuff; leg ~0-8in; heel ~8-11in; foot ~11-18.85in."""
import sys, numpy as np, cv2, re
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text, render_svg
from PIL import Image, ImageDraw
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
D = f"{HB}/socks"
DPI = 300; W, H = int(4.49 * DPI), int(18.85 * DPI)

def crop(a):
    ys, xs = np.where(a > 0.5); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def word(text, font, ax=None, w=None, h=None, tr=0.0, xs=1.0, round_px=0):
    a, _ = render_text(text, font, 170, ax, tr, xs)
    if round_px: a = cv2.GaussianBlur(a, (0, 0), round_px)
    a = crop(a); sc = min(w / a.shape[1] if w else 1e9, h / a.shape[0] if h else 1e9)
    return cv2.resize(a, (int(a.shape[1] * sc), int(a.shape[0] * sc)), interpolation=cv2.INTER_AREA) > 0.5
class Strip:
    def __init__(self, bg): self.a = np.zeros((H, W, 3), np.uint8); self.a[:] = bg
    def band(self, y0, y1, c): self.a[int(y0):int(y1)] = c
    def put(self, m, c, y, x=None):
        x = (W - m.shape[1]) // 2 if x is None else x; y = int(y)
        sub = self.a[y:y + m.shape[0], x:x + m.shape[1]]; sub[m[:sub.shape[0], :sub.shape[1]]] = c
        return y + m.shape[0]
    def save(self, name):
        Image.fromarray(self.a).save(f"{D}/{name}.png", dpi=(DPI, DPI)); return f"{D}/{name}.png"
IN = DPI
out = {}
# 1) HHS gym sock — white, purple stripes, Old English H (one school color)
P = (58, 16, 85); s = Strip((246, 246, 244))
for i in range(3): s.band(0.55 * IN + i * 0.42 * IN, 0.55 * IN + i * 0.42 * IN + 0.22 * IN, P)
svg = open(f"{HB}/ref/hhs/hhs_oldenglish_H_connected.svg").read(); w0, h0 = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', svg)[0]]
hh = int(2.6 * IN); Hm = render_svg(svg, int(w0 * hh / h0), hh)
y = s.put(Hm, P, 2.3 * IN)
s.put(word("PHYS. ED.", "Graduate-Regular.ttf", None, w=int(2.6 * IN), tr=0.06), P, y + 0.25 * IN)
for i in range(2): s.band(17.6 * IN + i * 0.36 * IN, 17.6 * IN + i * 0.36 * IN + 0.18 * IN, P)   # toe stripes
out["hhs"] = s.save("sock_hhs_gym_purple")

# 2) Camelot — white, royal-blue groove stripes, red stacked inline blackletter (1970s bag system)
RED, BLUE = (198, 40, 50), (46, 73, 184); s = Strip((250, 249, 246))
for i, t in enumerate((0.30, 0.18, 0.12)): s.band(0.4 * IN + i * 0.38 * IN, 0.4 * IN + i * 0.38 * IN + t * IN, BLUE)
def inline(m, gap=7, stroke=6):
    p = gap + stroke + 2; m = np.pad(m, p); k = lambda r: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return m | ((cv2.dilate(m.astype(np.uint8), k(gap + stroke)) > 0) & ~(cv2.dilate(m.astype(np.uint8), k(gap)) > 0))
y = s.put(inline(word("Camelot", "GrenzeGotisch[wght].ttf", {"wght": 760}, w=int(3.9 * IN), xs=0.9)), RED, 2.0 * IN)
y = s.put(inline(word("Music", "GrenzeGotisch[wght].ttf", {"wght": 760}, w=int(3.2 * IN), xs=0.9)), RED, y + 0.1 * IN)
s.put(word("HATTIESBURG · 1974", "Jost[wght].ttf", {"wght": 700}, w=int(3.2 * IN), tr=0.10), RED, y + 0.35 * IN)
# record on the foot: concentric blue grooves
rec = np.zeros((int(3.6 * IN), W), np.uint8); c = (W // 2, rec.shape[0] // 2)
for r, t in ((int(1.6 * IN), 40), (int(1.25 * IN), 24), (int(0.95 * IN), 16)): cv2.circle(rec, c, r, 1, t)
cv2.circle(rec, c, int(0.32 * IN), 1, -1)
s.put(rec > 0, BLUE, 12.6 * IN)
out["camelot"] = s.save("sock_camelot")

# 3) Hub City — checkered cuff, stacked authentic headline letters, FORD vs. CHEVY! on the foot
s = Strip((248, 248, 246)); K = (18, 18, 18); sq = int(0.28 * IN)
for r in range(4):
    for cidx in range(W // sq + 1):
        if (r + cidx) % 2 == 0: s.a[int(0.3 * IN) + r * sq:int(0.3 * IN) + (r + 1) * sq, cidx * sq:(cidx + 1) * sq] = K
hc = cv2.imread(f"{HB}/hubcity/sr_gray_3150.png", 0)
hb_ = hc[65:241, 89:2615] < 140; hb_[85:, 2572 - 89:] = False
head = crop(hb_.astype(np.float32)) > 0.5
cols = head.any(axis=0); gaps = []; run = 0
for x in range(len(cols)):
    if not cols[x]: run += 1
    else:
        if run > 25: gaps.append((x - run, x))
        run = 0
words_ = []; prev = 0
for g in gaps: words_.append(head[:, prev:g[0]]); prev = g[1]
words_.append(head[:, prev:])
y = 2.1 * IN
for wd in words_[:4]:
    wd = crop(wd.astype(np.float32)) > 0.5
    sc = min(3.9 * IN / wd.shape[1], 1.15 * IN / wd.shape[0])
    m = cv2.resize(wd.astype(np.float32), (int(wd.shape[1] * sc), int(wd.shape[0] * sc)), interpolation=cv2.INTER_AREA) > 0.5
    y = s.put(m, K, y) + 0.22 * IN
band_ = hc[506:669, 354:2850] < 140
cols = band_.any(axis=0); gaps = []; run = 0
for x in range(len(cols)):
    if not cols[x]: run += 1
    else:
        if run > 22: gaps.append((x - run, x))
        run = 0
bounds = [0] + [g for gp in gaps for g in gp] + [band_.shape[1]]
wds = [band_[:, bounds[2 * i]:bounds[2 * i + 1]] for i in range(len(bounds) // 2)]
wds = [crop(w.astype(np.float32)) > 0.5 for w in wds if w.any()]
ford_vs = np.hstack([wds[-3], np.zeros((wds[-3].shape[0], 30), bool), np.pad(wds[-2], ((wds[-3].shape[0] - wds[-2].shape[0], 0), (0, 0)))]) if wds[-2].shape[0] <= wds[-3].shape[0] else wds[-3]
y = 12.9 * IN
for wd in (ford_vs, wds[-1]):
    sc = min(3.9 * IN / wd.shape[1], 0.95 * IN / wd.shape[0])
    m = cv2.resize(wd.astype(np.float32), (int(wd.shape[1] * sc), int(wd.shape[0] * sc)), interpolation=cv2.INTER_AREA) > 0.5
    y = s.put(m, K, y) + 0.2 * IN
for r in range(2):
    for cidx in range(W // sq + 1):
        if (r + cidx) % 2 == 0: s.a[int(17.9 * IN) + r * sq:int(17.9 * IN) + (r + 1) * sq, cidx * sq:(cidx + 1) * sq] = K
out["hubcity"] = s.save("sock_hubcity")

# 4) Albert Speed's — cream, red sign block with rounded lettering, green neon bars
CR, R2, DR, GR = (240, 230, 206), (178, 46, 34), (104, 22, 16), (48, 132, 78)
s = Strip(CR)
s.band(0.35 * IN, 0.55 * IN, GR); s.band(0.62 * IN, 0.70 * IN, CR); s.band(0.70 * IN, 0.9 * IN, GR)
s.a[int(1.5 * IN):int(7.4 * IN), int(0.25 * IN):W - int(0.25 * IN)] = DR
s.a[int(1.6 * IN):int(7.3 * IN), int(0.35 * IN):W - int(0.35 * IN)] = R2
def speeds_sock(lines, name):
    s = Strip(CR)
    s.band(0.35 * IN, 0.55 * IN, GR); s.band(0.62 * IN, 0.70 * IN, CR); s.band(0.70 * IN, 0.9 * IN, GR)
    s.a[int(1.5 * IN):int(7.4 * IN), int(0.25 * IN):W - int(0.25 * IN)] = DR
    s.a[int(1.6 * IN):int(7.3 * IN), int(0.35 * IN):W - int(0.35 * IN)] = R2
    ms = [word(t, "Archivo[wdth,wght].ttf", {"wght": 760, "wdth": 82}, w=int(3.5 * IN), h=int(h * IN), tr=0.04, round_px=6) for t, h in lines]
    if [t for t, _ in lines][-2:] == ["RESTAU", "RANT"]:   # one word split across two lines: same letter height
        ms[-1] = word("RANT", "Archivo[wdth,wght].ttf", {"wght": 760, "wdth": 82}, h=ms[-2].shape[0], tr=0.04, round_px=6)
    gap = 0.12 * IN
    total = sum(m.shape[0] for m in ms) + gap * (len(ms) - 1)
    y = 1.6 * IN + ((7.3 - 1.6) * IN - total) / 2          # center the stack in the red panel
    for m in ms: y = s.put(m, CR, y) + gap
    s.put(word("304 BROADWAY DR.", "Jost[wght].ttf", {"wght": 700}, w=int(3.4 * IN), tr=0.08), R2, 12.9 * IN)
    s.put(word("HATTIESBURG · 1966", "Jost[wght].ttf", {"wght": 700}, w=int(3.4 * IN), tr=0.08), R2, 13.55 * IN)
    s.band(17.7 * IN, 17.9 * IN, GR)
    return s.save(name)
# primary: stacked sign-style split, no hyphen (Brad 10-21)
out["speeds"] = speeds_sock((("ALBERT", 1.05), ("SPEED'S", 1.35), ("RESTAU", 1.0), ("RANT", 1.0)), "sock_speeds")
# alternate: RESTAURANT on one line
out["speeds_alt"] = speeds_sock((("ALBERT", 1.15), ("SPEED'S", 1.5), ("RESTAURANT", 0.62)), "sock_speeds_oneline")

# mock: render each strip as a sock silhouette (leg + foot)
def sock_mock(p, label):
    a = Image.open(p).convert("RGB"); wpx = 150; hpx = int(a.height * wpx / a.width); a = a.resize((wpx, hpx))
    leg_h = int(hpx * 0.52)
    canvas = Image.new("RGB", (330, 470), (236, 234, 230)); d = ImageDraw.Draw(canvas)
    leg = a.crop((0, 0, wpx, leg_h)); canvas.paste(leg, (40, 30))
    foot = a.crop((0, leg_h, wpx, hpx)).rotate(90, expand=True)     # foot runs horizontally
    fw, fh = foot.size; foot = foot.resize((min(fw, 250), wpx))
    canvas.paste(foot, (40, 30 + leg_h - 10))
    d.text((8, 6), label, fill=(80, 80, 80)); return canvas
import sys as _s; _s.path.insert(0, f"{HB}/lib"); from teemock import sheet
sheet([sock_mock(out[k], l) for k, l in (("hhs", "HHS gym sock"), ("camelot", "Camelot"), ("hubcity", "Hub City"), ("speeds", "Albert Speed's"))], cols=4).save(f"{D}/socks_mocks.jpg", quality=88)
# flat strips sheet (true art)
flat = [Image.open(out[k]).convert("RGB").resize((180, int(180 * H / W))) for k in ("hhs", "camelot", "hubcity", "speeds", "speeds_alt")]
fs = Image.new("RGB", (5 * 200, flat[0].height + 20), (236, 234, 230))
for i, f in enumerate(flat): fs.paste(f, (10 + i * 200, 10))
fs.save(f"{D}/socks_flat.jpg", quality=88)
print("done", W, H)
