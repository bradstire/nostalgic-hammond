"""Printful Sublimation Socks v3 (spec re-checked 10-22 from Printful's own templates, product 882):
file per face 1347 x 5657 px @300 dpi (M; S/L templates differ by <0.3in), FRONT and BACK are separate files,
red safe box x 263-1083 px (2.73in centred), front safe y 1169-5030 (M), back = calf box + sole box with the heel between.
v2 broke this (art 3.5-3.9in wide starting 1.5in from the top = wrapped round the leg / inside the cuff zone).
v3: every mark sits inside the overlap of the S/M/L safe boxes; backgrounds + bands run full-bleed (they wrap by design).
Camelot letters solid (an inline at sock scale won't survive knit stretch); Speed's = one-line RESTAURANT (Brad's pick)."""
import sys, re, io, numpy as np, cv2
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/lib")
from PIL import Image, ImageDraw
from vtype import run, text_geom, svg_doc, affinity
from newsprint import render_svg
import cairosvg
D = f"{HB}/socks"; DPI = 300; W, H = 1347, 5657
SAFE_X = (280, 1066)                       # inside red box x 263-1083 for every size
FRONT_Y = (1540, 4810)                     # overlap of S 1517-4940, M 1169-5030, L 741-4831
CALF_Y, SOLE_Y = (1520, 2560), (4270, 5010)
SW = SAFE_X[1] - SAFE_X[0]                 # 786 px = 2.62in usable width

def gmask(g, w=None, h=None):
    b = g.bounds; s = min(w / (b[2] - b[0]) if w else 1e9, h / (b[3] - b[1]) if h else 1e9)
    g = affinity.scale(g, s, s, origin=(0, 0)); b = g.bounds; g = affinity.translate(g, -b[0] + 2, -b[1] + 2)
    Wd, Hd = int(b[2] - b[0] + 4), int(b[3] - b[1] + 4)
    png = cairosvg.svg2png(bytestring=svg_doc([(g, "#000000")], Wd, Hd).encode(), output_width=Wd, output_height=Hd)
    a = np.array(Image.open(io.BytesIO(png)).convert("RGBA"))[..., 3] >= 128
    ys, xs = np.where(a); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def txt(text, font, var=None, tr=0.04, w=None, h=None, skew=0):
    g = run([(text, font, 900, var, tr, 0)])
    if skew: g = affinity.skew(g, xs=skew, origin=(0, 0))
    return gmask(g, w, h)

class Face:
    def __init__(self, bg): self.a = np.zeros((H, W, 3), np.uint8); self.a[:] = bg
    def band(self, y0, y1, c): self.a[int(y0):int(y1)] = c
    def put(self, m, c, y, cx=None):
        cx = (SAFE_X[0] + SAFE_X[1]) // 2 if cx is None else cx
        x = int(cx - m.shape[1] / 2); y = int(y); sub = self.a[y:y + m.shape[0], x:x + m.shape[1]]
        sub[m[:sub.shape[0], :sub.shape[1]]] = c; return y + m.shape[0]
    def save(self, name):
        Image.fromarray(self.a).save(f"{D}/{name}.png", dpi=(DPI, DPI)); return f"{D}/{name}.png"

def centered_stack(face, items, y0, y1):
    """items: list of (mask, color, gap_after_px). Vertically centre the stack inside [y0, y1]."""
    tot = sum(m.shape[0] + g for m, c, g in items) - items[-1][2]
    assert tot <= y1 - y0, f"stack {tot}px > zone {y1 - y0}px"
    y = y0 + (y1 - y0 - tot) // 2
    for m, c, g in items: y = face.put(m, c, y) + g

out = {}
G, GV, MC = "GrenzeGotisch[wght].ttf", [900], "ManufacturingConsent-Regular.ttf"
HEROS = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts/texgyreheros-bold.otf"
GRAD = "Graduate-Regular.ttf"

# 1) HHS gym sock — white, purple bands, v3 Old English H + PHYS. ED.
P, WH = (107, 82, 148), (246, 246, 244)        # purple matches the hat thread family
svg = open(f"{HB}/ref/hhs/hhs_H_v3.svg").read(); w0, h0 = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', svg)[0]]
Hm = render_svg(svg, int(w0 * 1.9 * DPI / h0), int(1.9 * DPI)); ys, xs = np.where(Hm); Hm = Hm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
if Hm.shape[1] > SW * 0.9: Hm = cv2.resize(Hm.astype(np.float32), (int(SW * 0.9), int(Hm.shape[0] * SW * 0.9 / Hm.shape[1])), interpolation=cv2.INTER_AREA) > 0.5
pe = txt("PHYS. ED.", GRAD, None, 0.06, w=int(SW * 0.9))
for face_name in ("front", "back"):
    f = Face(WH)
    for i in range(3): f.band(1580 + i * 120, 1580 + i * 120 + 64, P)            # gym stripes (wrap the leg)
    if face_name == "front":
        centered_stack(f, [(Hm, P, 150), (pe, P, 0)], 2050, 3700)
    f.band(4560, 4610, P); f.band(4660, 4710, P)                                    # toe stripes
    out[f"hhs_{face_name}"] = f.save(f"sock_hhs_gym_purple_{face_name}")

# 2) Camelot — white, royal-blue groove bands, solid red stacked wordmark, record on the foot
RED, BLUE, OFF = (198, 40, 50), (46, 73, 184), (250, 249, 246)
cam = gmask(run([("C", MC, 1180, None, 0, 0.02), ("amelot", G, 1000, GV, 0.06, 0)]), w=int(SW))
mus = gmask(run([("Music", G, 1000, GV, 0.06, 0)]), h=int(cam.shape[0] * 0.97))
loc = gmask(affinity.skew(text_geom("HATTIESBURG · 1974", HEROS, 400, None, 0.08)[0], xs=-12, origin=(0, 0)), w=int(SW * 0.86))
rec = np.zeros((int(2.2 * DPI), int(2.2 * DPI)), np.uint8); c = (rec.shape[1] // 2, rec.shape[0] // 2)
for r, t in ((int(1.0 * DPI), 26), (int(0.78 * DPI), 18), (int(0.58 * DPI), 14)): cv2.circle(rec, c, r, 1, t)
cv2.circle(rec, c, int(0.2 * DPI), 1, -1); rec = rec > 0
for face_name in ("front", "back"):
    f = Face(OFF)
    for i, t in enumerate((96, 60, 40)): f.band(1580 + i * 116, 1580 + i * 116 + t, BLUE)
    if face_name == "front":
        centered_stack(f, [(cam, RED, 40), (mus, RED, 110), (loc, RED, 0)], 2000, 3150)
        f.put(rec, BLUE, 3600)
    else:
        f.put(rec, BLUE, SOLE_Y[0] + (SOLE_Y[1] - SOLE_Y[0] - rec.shape[0]) // 2) if rec.shape[0] <= SOLE_Y[1] - SOLE_Y[0] else None
    out[f"camelot_{face_name}"] = f.save(f"sock_camelot_{face_name}")

# 3) Hub City — checkered bands, stacked authentic headline words, FORD vs. CHEVY! on the foot
K, WH2 = (18, 18, 18), (248, 248, 246)
hc = cv2.imread(f"{HB}/hubcity/sr_gray_3150.png", 0)
hb_ = hc[65:241, 89:2615] < 140; hb_[85:, 2572 - 89:] = False
crop = lambda a: a[np.where(a.any(1))[0].min():np.where(a.any(1))[0].max() + 1, np.where(a.any(0))[0].min():np.where(a.any(0))[0].max() + 1]
head = crop(hb_)
cols = head.any(axis=0); gaps = []; run_ = 0
for x in range(len(cols)):
    if not cols[x]: run_ += 1
    else:
        if run_ > 25: gaps.append((x - run_, x))
        run_ = 0
words, prev = [], 0
for gp in gaps: words.append(crop(head[:, prev:gp[0]])); prev = gp[1]
words.append(crop(head[:, prev:]))
def fitm(m, w=None, h=None):
    s = min(w / m.shape[1] if w else 1e9, h / m.shape[0] if h else 1e9)
    return cv2.resize(m.astype(np.float32), (int(m.shape[1] * s), int(m.shape[0] * s)), interpolation=cv2.INTER_AREA) > 0.5
hw = [fitm(wd, w=SW, h=int(0.72 * DPI)) for wd in words[:4]]
band_ = hc[506:669, 354:2850] < 140
cols = band_.any(axis=0); gaps = []; run_ = 0
for x in range(len(cols)):
    if not cols[x]: run_ += 1
    else:
        if run_ > 22: gaps.append((x - run_, x))
        run_ = 0
bounds = [0] + [g for gp in gaps for g in gp] + [band_.shape[1]]
wds = [crop(band_[:, bounds[2 * i]:bounds[2 * i + 1]]) for i in range(len(bounds) // 2) if band_[:, bounds[2 * i]:bounds[2 * i + 1]].any()]
ford_vs = np.hstack([wds[-3], np.zeros((wds[-3].shape[0], 30), bool), np.pad(wds[-2], ((max(0, wds[-3].shape[0] - wds[-2].shape[0]), 0), (0, 0)))[:wds[-3].shape[0]]])
fv = fitm(ford_vs, w=SW); ch = fitm(wds[-1], w=SW)
sq = int(0.25 * DPI)
def checker(f, y0, rows=2):
    for r in range(rows):
        for ci in range(W // sq + 1):
            if (r + ci) % 2 == 0: f.a[y0 + r * sq:y0 + (r + 1) * sq, ci * sq:(ci + 1) * sq] = K
for face_name in ("front", "back"):
    f = Face(WH2); checker(f, 1580, 2)
    if face_name == "front":
        centered_stack(f, [(m, K, 70) for m in hw[:-1]] + [(hw[-1], K, 0)], 1800, 3450)
        centered_stack(f, [(fv, K, 60), (ch, K, 0)], 3550, 4350)
    checker(f, 4560, 1)
    out[f"hubcity_{face_name}"] = f.save(f"sock_hubcity_{face_name}")

# 4) Albert Speed's — cream, green neon bars, red sign panel (wraps the leg), one-line RESTAURANT (primary)
CR, R2, DR, GR = (240, 230, 206), (178, 46, 34), (104, 22, 16), (48, 132, 78)
AR, AV = "Archivo[wdth,wght].ttf", [780, 82]          # axes order = (Weight, Width)
a1 = txt("ALBERT", AR, AV, 0.05, w=int(SW * 0.86)); a2 = txt("SPEED'S", AR, AV, 0.04, w=int(SW * 0.98))
a3 = txt("RESTAURANT", AR, AV, 0.04, w=int(SW * 0.98))
addr1 = txt("304 BROADWAY DR.", "Jost[wght].ttf", [700], 0.08, w=int(SW * 0.95)); addr2 = txt("HATTIESBURG · 1966", "Jost[wght].ttf", [700], 0.08, w=int(SW * 0.95))
for face_name in ("front", "back"):
    f = Face(CR)
    f.band(1580, 1640, GR); f.band(1680, 1740, GR)
    f.band(1840, 3460, DR); f.band(1870, 3430, R2)        # sign panel, full wrap
    if face_name == "front":
        centered_stack(f, [(a1, CR, 70), (a2, CR, 70), (a3, CR, 0)], 1900, 3400)
        centered_stack(f, [(addr1, R2, 50), (addr2, R2, 0)], 3700, 4300)
    f.band(4600, 4660, GR)
    out[f"speeds_{face_name}"] = f.save(f"sock_speeds_{face_name}")

# QA sheet: every face with the Printful M template's safe box drawn on top
tpl = {k: np.array(Image.open(f"/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/dl_socks/x/SublimationSocks_Template_{k} M.png").convert("RGBA")) for k in ("Front", "Back")}
tiles = []
for key in ("hhs", "camelot", "hubcity", "speeds"):
    for face_name in ("front", "back"):
        im = Image.open(out[f"{key}_{face_name}"]).convert("RGBA")
        t = tpl["Front" if face_name == "front" else "Back"].copy()
        red = (t[..., 0] > 180) & (t[..., 1] < 90) & (t[..., 2] < 90) & (t[..., 3] > 0)
        hatch = (t[..., :3].sum(-1) < 400) & (t[..., 3] > 0) & ~red
        o = np.array(im); o[hatch] = (o[hatch] * 0.55 + np.array([120, 120, 120, 255]) * 0.45).astype(np.uint8); o[red] = (230, 30, 30, 255)
        tiles.append(Image.fromarray(o).convert("RGB").resize((180, int(180 * H / W))))
sheet = Image.new("RGB", (len(tiles) * 196 + 16, tiles[0].height + 46), (236, 234, 230)); d = ImageDraw.Draw(sheet)
for i, t in enumerate(tiles):
    sheet.paste(t, (16 + i * 196, 30)); d.text((16 + i * 196, 8), ["HHS", "Camelot", "Hub City", "Speed's"][i // 2] + (" front" if i % 2 == 0 else " back"), fill=(40, 40, 40))
sheet.save(f"{D}/socks_v3_template_check.jpg", quality=90)
flat = Image.new("RGB", (8 * 196 + 16, tiles[0].height + 46), (236, 234, 230)); d = ImageDraw.Draw(flat)
for i, key in enumerate([f"{k}_{s}" for k in ("hhs", "camelot", "hubcity", "speeds") for s in ("front", "back")]):
    flat.paste(Image.open(out[key]).convert("RGB").resize((180, int(180 * H / W))), (16 + i * 196, 30)); d.text((16 + i * 196, 8), key.replace("_", " "), fill=(40, 40, 40))
flat.save(f"{D}/socks_v3_flat.jpg", quality=90)
print("done", {k: v.split("/")[-1] for k, v in out.items()})
