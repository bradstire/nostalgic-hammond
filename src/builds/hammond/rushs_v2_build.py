"""Rush's v2 (HQ 2026-10-25, S9): identical to v1 except (a) NO roughen() on type - type is rendered straight
from the font (S9: typeset text is never screened, traced or textured), (b) photo frame 0.03 in (was 0.02).
v1 notes: Rush's (1722 West Thomas St., Hammond) — the drive-in's own ad ("In Hammond It's RUSH'S / Louisiana's Finest
Drive In"), rebuilt as a print (IMG_7163/7162/7179). Pipeline B: copy re-typeset in matched faces (Century Schoolbook ->
TeX Gyre Schola, GUST; Futura Bold -> Jost, OFL) at the ad's proportions; the photo of the twin-cupola stand
Real-ESRGAN x4plus -> grayscale -> re-screened round-dot halftone (prints clean on DTG).
PROVISIONAL: a live 'Rush's' drive-in chain operates in Columbia, SC — federal trademark check pending."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from hmlib import build_multi, remove_small
from newsprint import render_text, halftone, roughen
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/rushs"
INK = (40, 34, 30)
W = 3000                                                  # 10 in @ 300 dpi
def line(text, font, h, axes=None, tr=0.0):
    a, (x0, y0, x1, y1) = render_text(text, font, 300, axes, tr)
    a = a[y0:y1, x0:x1]; s = h / a.shape[0]
    a = cv2.resize(a, (int(a.shape[1] * s), int(h)), interpolation=cv2.INTER_AREA)
    return np.pad(a, 8) > 0.5                                        # crisp: straight from the font (no roughen, S9)
# ad proportions (from the 7163 zoom: cap/x heights relative to the RUSH'S cap height)
CAP = 230                                                  # text block ~0.6 of the photo width (the yearbook ad runs ~0.35: too small to read on a shirt)
l_in = line("In Hammond It's", "texgyreschola-bold.otf", CAP * 0.36, tr=0.015)   # v2: Bold - Regular's hairlines < 0.015 in
l_rush = line("RUSH’S", "Jost[wght].ttf", CAP, {"wght": 760}, 0.01)
l_fin = line("“Louisiana's Finest Drive In”", "texgyreschola-bold.otf", CAP * 0.36, tr=0.015)
l_addr = line("1722 West Thomas Street", "texgyreschola-bold.otf", CAP * 0.33, tr=0.015)
l_rt = line("Rt. 1, Box 4-X", "texgyreschola-bold.otf", CAP * 0.33, tr=0.015)
# photo: the stand, re-screened
ph = cv2.imread(f"{D}/photo_x4.png", cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
pw = int(W * 0.92); ph = cv2.resize(ph, (pw, int(ph.shape[0] * pw / ph.shape[1])), interpolation=cv2.INTER_AREA)
lo, hi = np.percentile(ph, 1.5), np.percentile(ph, 99.0)
g = np.clip((ph - lo) / (hi - lo), 0, 1)
g = cv2.GaussianBlur(g, (0, 0), 0.8)
dots = halftone(g, cell=9.0, angle=45, gamma=1.08)
dots = remove_small(dots, 3)
FR = 9                                                             # 0.03 in frame (v1: 6 px = 0.02 in)
frame = np.zeros_like(dots); frame[:FR] = frame[-FR:] = True; frame[:, :FR] = frame[:, -FR:] = True
photo = dots | frame
parts = [(l_in, 70), (l_rush, 90), (l_fin, 110), (photo, 110), (l_addr, 60), (l_rt, 0)]
Hc = sum(p.shape[0] + g_ for p, g_ in parts) + 160
c = np.zeros((Hc, W), bool); y = 80; boxes = []
for p, g_ in parts:
    x = (W - p.shape[1]) // 2; c[y:y + p.shape[0], x:x + p.shape[1]] |= p; boxes.append((x, y, x + p.shape[1], y + p.shape[0])); y += p.shape[0] + g_
ys, xs = np.where(c); cy0, cx0 = ys.min() - 20, xs.min() - 20
c = c[ys.min() - 20:ys.max() + 21, xs.min() - 20:xs.max() + 21]
from PIL import Image
rgba = np.zeros((*c.shape, 4), np.uint8); rgba[c, :3] = INK; rgba[c, 3] = 255
OUT = sys.argv[1] if len(sys.argv) > 1 else f"{D}/rushs_ad_v2.png"
Image.fromarray(rgba, "RGBA").save(OUT, dpi=(300, 300))
import json, os
fonts = ["TeX Gyre Schola Bold", "Jost 760", "TeX Gyre Schola Bold", None, "TeX Gyre Schola Bold", "TeX Gyre Schola Bold"]
json.dump({"typeset": [[[int(b[0] - cx0), int(b[1] - cy0), int(b[2] - cx0), int(b[3] - cy0)], f] for b, f in zip(boxes, fonts) if f], "exempt": []},
          open(os.path.splitext(OUT)[0] + ".prov.json", "w"), indent=1)      # raster (halftone) master, 10 in wide
print(c.shape)
