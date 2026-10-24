"""Casa de Fresa hat + HAMMOND, LA. line (Brad 10-22 differentiation rule: never the bare name).
Name: the passed matchbook-lettering file. Locator: League Spartan Bold, tracked, 0.27 in caps, same thread."""
import sys, numpy as np
from PIL import Image
S="/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad"
sys.path.insert(0, f"{S}/hb/hats"); sys.path.insert(0, f"{S}/hb/lib")
from build_v3 import textline, vstack, THREAD, DPI, check, smooth
W="/home/claude/nh-recovered/print-assets-repo/hammond/wave2/hats"
name = np.array(Image.open(f"{W}/hat_casadefresa_red.png"))[..., 3] > 127
ys, xs = np.where(name); name = name[ys.min():ys.max()+1, xs.min():xs.max()+1]
loc = textline("HAMMOND, LA.", "LeagueSpartan[wght].ttf", var=[700], tr=0.14, h_in=0.34)
import cv2
def open_small_counters(m, need_in=0.065):
    inv = np.pad(~m, 1, constant_values=True).astype(np.uint8)
    nh, lab, st, _ = cv2.connectedComponentsWithStats(inv, 4); dt = cv2.distanceTransform(inv, cv2.DIST_L2, 5)
    for i in range(1, nh):
        if lab[0, 0] == i: continue
        w = 2 * dt[lab == i].max(); need = need_in * DPI
        if w < need:
            r = int(np.ceil((need - w) / 2)); k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
            m = m & ~(cv2.dilate((lab == i).astype(np.uint8), k)[1:-1, 1:-1] > 0)
    return m
loc = open_small_counters(loc)
m = vstack([name, loc], 0.13)
print("size in", m.shape[1]/DPI, m.shape[0]/DPI, "loc w", loc.shape[1]/DPI)
r = check(m, "front", [("CASA FRESA", 0.75, name.shape[1]/DPI), ("HAMMOND, LA.", 0.34, loc.shape[1]/DPI)])
print("PASS" if r["pass"] else "CHECK", r)
for thread in ("red", "white"):
    c = THREAD[thread]; rgba = np.zeros((*m.shape, 4), np.uint8)
    rgba[m, :3] = [int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)]; rgba[m, 3] = 255
    Image.fromarray(rgba, "RGBA").save(f"{W}/hat_casadefresa_hammond_{thread}.png", dpi=(DPI, DPI))
bg = Image.new("RGBA", (m.shape[1]+120, m.shape[0]+120), (214,203,180,255)); im=Image.open(f"{W}/hat_casadefresa_hammond_red.png"); bg.alpha_composite(im,(60,60)); bg.convert("RGB").save(f"{S}/hm2/casa_hat_locator_view.png")
