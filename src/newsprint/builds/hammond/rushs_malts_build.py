"""Rush's Drive-In - the second yearbook ad ("In Hammond / We Appreciate Our Ponchatoula Customers / Finest in Malts,
Sundaes / Shakes, Drinks and Sandwiches", IMG_7180/7181) rebuilt as a print. Pipeline B: Real-ESRGAN x4plus -> every line of
type traced (the ad's own Futura-style RUSH'S and Century-style roman, clean at x4); the photo of the twin-cupola stand
re-screened as a round-dot halftone; the ad's frame redrawn as a clean rule (the scan cuts its bottom edge off)."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from hmlib import remove_small, fill_small_holes
from newsprint import halftone
from PIL import Image
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/rushs2"
INK = (40, 34, 30)
im = cv2.imread(f"{D}/ad7180_x4.png").astype(np.float32); g = im.mean(2)
H0, W0 = g.shape
# photo bounds: strongest brightness steps around the expected box (view 390-1113 x 255-555, x3)
px0, py0, px1, py1 = 1170, 765, 3339, 1662
def edge(arr, lo, hi):
    d = np.abs(np.diff(arr[lo:hi])); return lo + int(np.argmax(d)) + 1
rowm = g[:, 1500:3000].mean(1); colm = g[900:1500].mean(0)
py0 = edge(rowm, 730, 800); px0 = edge(colm, 1130, 1210); px1 = edge(colm, 3300, 3380)
py1 = min(py1, 1665)
bg = cv2.GaussianBlur(g, (0, 0), 45)
soft = cv2.GaussianBlur(np.clip((bg - g - 45) / 55.0, 0, 1), (0, 0), 1.5)
ink = remove_small(soft > 0.5, 35)                    # keeps the small i-dots
yy, xx = np.mgrid[:H0, :W0]
ink &= ~((xx >= px0 - 6) & (xx <= px1 + 6) & (yy >= py0 - 6) & (yy <= py1 + 6))   # photo out (re-screened below)
ink &= (xx > 110) & (xx < W0 - 140) & (yy > 110) & (yy < 1700)                     # frame lines out (redrawn)
n, lab, st, _ = cv2.connectedComponentsWithStats(ink.astype(np.uint8), 8)
txt = np.zeros_like(ink)
for i in range(1, n):
    x, y, w, h, a = st[i]
    if h >= 18 and w < 700 and h < 200: txt[lab == i] = True                        # letters, apostrophe, dot of i
    elif a > 35 and h < 32 and w < 40 and h > 8: txt[lab == i] = True              # i-dots / periods
txt = fill_small_holes(txt, 120)
# photo, re-screened
ph = g[py0:py1, px0:px1] / 255.0
lo, hi = np.percentile(ph, 1.5), np.percentile(ph, 99.0)
gg = cv2.GaussianBlur(np.clip((ph - lo) / (hi - lo), 0, 1), (0, 0), 1.0)
dots = halftone(gg, cell=11.0, angle=45, gamma=1.05)
c = txt.copy(); c[py0:py1, px0:px1] |= dots
cc = c.astype(np.uint8)
cv2.rectangle(cc, (62, 72), (W0 - 92, 1745), 1, 9)                                 # the ad's frame
c = cc[40:1780, 30:W0 - 60] > 0
Hc, Wc = c.shape
s_ = 3000 / Wc; cs = cv2.resize(c.astype(np.float32), (3000, int(Hc * s_)), interpolation=cv2.INTER_AREA) > 0.5
rgba = np.zeros((*cs.shape, 4), np.uint8); rgba[cs, :3] = INK; rgba[cs, 3] = 255
Image.fromarray(rgba, "RGBA").save(f"{D}/rushs_ad_malts.png", dpi=(300, 300))       # raster master, 10 in wide
print((px0, py0, px1, py1), cs.shape)
