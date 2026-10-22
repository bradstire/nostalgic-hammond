"""HHS H v4 (Brad 10-22 13:13): jersey letter rebuilt from Manufacturing Consent's own vector parts, laid out by hand
to the jersey's proportions (measured on the v2 trace, normalised to cap height 1000):
  spur stroke  = MC capital H left element (top flag, stem, mid spur, sweeping foot), x ~4-33% of width
  h body       = MC lowercase h (flagged ascender, shoulder, descending leg), stem at ~40%, leg to ~85%
  ear          = MC h's own flag, mirrored, on the top-right of the h ascender (jersey's ball/hook)
One shared lean (~7 deg). Shapes are the font's; only scale/position chosen."""
import re, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/lib")
from newsprint import vectorize, render_svg
FONT = f"{HB}/fonts_bl/ManufacturingConsent-Regular.ttf"
P = dict(L_h=1000, L_x=0, L_y=0,                 # spur stroke height / position
         h_h=930, h_x=330, h_y=70,               # lowercase h (descender trimmed)
         ear_s=0.42, ear_dx=-30, ear_dy=-35,      # ear (MC's own shoulder flag) scale and offset from the ascender top-right
         cond=0.8, lean=-0.12)
if len(sys.argv) > 1:
    for kv in sys.argv[1:]: k, v = kv.split("="); P[k] = float(v)

def glyph(ch, size=1600):
    f = ImageFont.truetype(FONT, size); im = Image.new("L", (2600, 2600), 0)
    ImageDraw.Draw(im).text((300, 2000), ch, font=f, fill=255, anchor="ls")
    a = np.array(im) > 127; ys, xs = np.where(a); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def crop(a): ys, xs = np.where(a); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def scale_to_h(a, h, xs=1.0): return cv2.resize(a.astype(np.uint8), (max(1, int(a.shape[1] * h / a.shape[0] * xs)), int(h)), interpolation=cv2.INTER_AREA) > 0

H = glyph("H"); yy, xx = np.mgrid[:H.shape[0], :H.shape[1]]
L = H & (xx < 425)                                                            # left element = x 0-395 (gap 395-456 before the hairline)
L &= ~((yy < 230) & (xx > 300 + (230 - yy) * 0.35))                           # top swash ends on a pen-angle diagonal
L = crop(L)
h = glyph("h"); hy, hx = np.mgrid[:h.shape[0], :h.shape[1]]
h = h & ~((hy > 1012) | ((hx > 330) & (hy > 955 + (hx - 330) * 0.35)))       # leg ends on a pen angle at the baseline (no Fraktur tail)
h = crop(h)
asc_top_right_x = 267                                                         # MC h ascender spans x 88-267 (1600px)
# ear = MC's own i-dot diamond on a short pen-angle neck (the jersey's ball-ended hook, connected per Brad 10-21)
i_ = glyph("i"); n_, lab_, st_, _ = cv2.connectedComponentsWithStats(i_.astype(np.uint8), 8)
dot = crop(lab_ == (1 + int(np.argmin(st_[1:, 1]))))                          # top-most component = the dot
neck_w = int(dot.shape[0] * 0.36); neck_len = int(dot.shape[1] * 0.45)
ear = np.zeros((dot.shape[0] + neck_len, dot.shape[1] + neck_len), bool)
ear[:dot.shape[0], neck_len:] |= dot
for t in range(neck_len + dot.shape[1] // 3):                                  # diagonal neck from bottom-left up into the dot
    y = ear.shape[0] - 1 - t; x = t
    if 0 <= y < ear.shape[0]: ear[max(0, y - neck_w // 2):y + neck_w // 2, x:x + neck_w // 2] = True
ear = crop(ear)

def build(P):
    Ls = scale_to_h(L, P["L_h"], P["cond"]); hs = scale_to_h(h, P["h_h"], P["cond"]); k = P["h_h"] / h.shape[0]
    es = scale_to_h(ear, ear.shape[0] * k * P["ear_s"], 1.0)
    Wc, Hc = 1400, 1400; c = np.zeros((Hc, Wc), bool); ox, oy = 100, 100
    def put(m, x, y):
        x, y = int(x) + ox, int(y) + oy; c[y:y + m.shape[0], x:x + m.shape[1]] |= m
    put(Ls, P["L_x"], P["L_y"]); put(hs, P["h_x"], P["h_y"])
    put(es, P["h_x"] + asc_top_right_x * k * P["cond"] + P["ear_dx"], P["h_y"] + P["ear_dy"])
    c = crop(c); Hh, Ww = c.shape; M = np.float32([[1, P["lean"], max(0, -P["lean"] * Hh)], [0, 1, 0]])
    return crop(cv2.warpAffine(c.astype(np.uint8), M, (int(Ww + abs(P["lean"]) * Hh) + 2, Hh)) > 0)

M = build(P)
m = np.pad(M, 40); svg_out = vectorize(m, turdsize=60, alphamax=1.0, opttolerance=0.2)
open(f"{HB}/ref/hhs/hhs_H_v4.svg", "w").write(svg_out)
tiles = [np.array(Image.open(f"{HB}/ref/hhs/h_fused_bw.png").convert("L")) < 128]
s = open(f"{HB}/ref/hhs/hhs_oldenglish_H_connected.svg").read(); a, b = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', s)[0]]
tiles.append(crop(render_svg(s, int(a * 600 / b), 600)))
tiles.append(crop(render_svg(svg_out, m.shape[1], m.shape[0])))
cell = 640; B = Image.new("L", (cell * 3, cell + 40), 255); d = ImageDraw.Draw(B)
for i, (t, lab_) in enumerate(zip(tiles, ["1983 jersey (7-view fusion)", "v2 photo trace", "v4: Manufacturing Consent parts in the jersey's structure"])):
    t = t.astype(np.uint8) * 255; sc = 600 / t.shape[0]; t = cv2.resize(t, (int(t.shape[1] * sc), 600), interpolation=cv2.INTER_AREA)
    B.paste(Image.fromarray(255 - t), (i * cell + (cell - t.shape[1]) // 2, 10)); d.text((i * cell + 20, cell + 12), lab_, fill=0)
B.save(f"{HB}/hhs/hhs_H_v4_compare.png"); print("ok", M.shape, P)
