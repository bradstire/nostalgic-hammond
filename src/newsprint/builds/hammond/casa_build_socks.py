"""Casa de Fresa — Printful sublimation socks (product 882): FRONT and BACK files, 1347 x 5657 px @300 dpi.
Marks inside the S/M/L safe-box overlap (x 280-1066; front y 1540-4810; back calf y 1520-2560).
The matchbook's cabana stripes run full-bleed (they wrap by design), at the matchbook's own stripe/pitch ratio.
Front: the red panel + ribbon (traced matchbook art) on a cream keyline. Back: the matchbook lettering, red, on cream."""
import sys, numpy as np, cv2
from PIL import Image
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
from hmlib import disk, fill_small_holes
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/casa"
DPI = 300; W, H = 1347, 5657
SAFE_X = (280, 1066); SW = SAFE_X[1] - SAFE_X[0]
FRONT_Y = (1540, 4810); CALF_Y = (1520, 2560)
RED, GREEN, CREAM = (206, 32, 46), (10, 104, 86), (243, 233, 207)

def stripes():
    a = np.zeros((H, W, 3), np.uint8); a[:] = CREAM
    pitch, sw = 101, 52                                   # matchbook: stripe ~51% of pitch
    x0 = (W // 2) - sw // 2                               # a stripe centred on the face
    for x in range(x0 % pitch - pitch, W, pitch): a[:, max(0, x):max(0, x + sw)] = GREEN
    return a

def scale(m, w=None, h=None):
    s = min(w / m.shape[1] if w else 1e9, h / m.shape[0] if h else 1e9)
    return cv2.resize(m.astype(np.float32), (int(m.shape[1] * s), int(m.shape[0] * s)), interpolation=cv2.INTER_AREA) > 0.5

rm, gm, zone = np.load(f"{D}/mark_red.npy"), np.load(f"{D}/mark_green.npy"), np.load(f"{D}/mark_zone.npy")
# close the ribbon's open right end (on the matchbook it runs off the cover) with a short end line, same weight
ys, xs = np.where(gm); xe = xs.max()
zone = zone & (np.arange(zone.shape[1])[None, :] <= xe)
col = zone[:, xe - 40:xe + 1].any(1); y_lo, y_hi = np.where(col)[0].min(), np.where(col)[0].max()
gm = gm.copy(); gm[y_lo + 10:y_hi - 10, xe - 30:xe + 1] = True
panel = fill_small_holes(rm, 10**8) & (cv2.connectedComponents(rm.astype(np.uint8))[1] == np.bincount(cv2.connectedComponents(rm.astype(np.uint8))[1].ravel())[1:].argmax() + 1)
halo = cv2.dilate((panel | zone).astype(np.uint8), disk(55)) > 0          # cream keyline, as on the matchbook
halo = fill_small_holes(halo, 10**7)

def put(face, m, color, x, y):
    sub = face[y:y + m.shape[0], x:x + m.shape[1]]; sub[m[:sub.shape[0], :sub.shape[1]]] = color

# ---- FRONT ----
f = stripes()
s = SW / halo.shape[1]
def sc(m): return cv2.resize(m.astype(np.float32), (int(m.shape[1] * s), int(m.shape[0] * s)), interpolation=cv2.INTER_AREA) > 0.5
Hh, Rr, Gg, Zz = sc(halo), sc(rm), sc(gm), sc(zone)
x = SAFE_X[0]; y = 1900
put(f, Hh, CREAM, x, y); put(f, Gg, GREEN, x, y); put(f, Rr, RED, x, y)
f[:110] = RED                                                            # cuff edge band
assert y + Hh.shape[0] <= FRONT_Y[1] and y >= FRONT_Y[0]
Image.fromarray(f).save(f"{D}/sock_casadefresa_front.png", dpi=(DPI, DPI))

# ---- BACK ----
b = stripes()
from build_hat_name import name_mask                                      # levelled matchbook lettering
nm = scale(name_mask(), w=SW - 60)
plate = cv2.dilate(nm.astype(np.uint8), disk(30)) > 0
plate = cv2.morphologyEx(plate.astype(np.uint8), cv2.MORPH_CLOSE, disk(40)) > 0
yb = (CALF_Y[0] + CALF_Y[1]) // 2 - plate.shape[0] // 2; xb = (SAFE_X[0] + SAFE_X[1]) // 2 - plate.shape[1] // 2
put(b, plate, CREAM, xb, yb); put(b, nm, RED, xb + (plate.shape[1] - nm.shape[1]) // 2, yb + (plate.shape[0] - nm.shape[0]) // 2)
b[:110] = RED
Image.fromarray(b).save(f"{D}/sock_casadefresa_back.png", dpi=(DPI, DPI))
print("front mark", Hh.shape, "at y", y, "| back plate", plate.shape, "at y", yb)
