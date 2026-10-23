"""Toggery Shop — 'the Toggery Shop' logotype from the store's 1960s newspaper ad (IMG_7170), Pipeline B:
Real-ESRGAN x4 -> ink threshold -> cleanup -> potrace. Logo letters + flourishes are the ad's own (traced).
Ad copy under it re-typeset (address only; the phone number is left off — reassigned numbers)."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from hmlib import remove_small, fill_small_holes, build_multi, disk
from newsprint import render_text, roughen
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/toggery"
WINE = (110, 30, 42)
im = cv2.imread(f"{D}/logo_x4.png").astype(np.float32)
gray = im.mean(2)
bg = cv2.GaussianBlur(gray, (0, 0), 60)                  # uneven newsprint tone
ink = gray < bg - 45
ink = cv2.morphologyEx(ink.astype(np.uint8), cv2.MORPH_OPEN, disk(2)) > 0
ink = fill_small_holes(remove_small(ink, 400), 250)
ink[:, :8] = False; ink[:, -8:] = False
up = 2                                                    # work at 2x for smoother curves
ink = cv2.resize(ink.astype(np.float32), (ink.shape[1] * up, ink.shape[0] * up), interpolation=cv2.INTER_CUBIC)
ink = cv2.GaussianBlur(ink, (0, 0), 2.2) > 0.5
ys, xs = np.where(ink); logo = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
# ink cleanup on the small 'the' (letters filled in on the newsprint): re-open the gaps and the e's eye
lg = logo.astype(np.uint8)
cv2.line(lg, (1483, 248), (1480, 312), 0, 10)            # t | h
cv2.line(lg, (1586, 196), (1584, 304), 0, 10)            # h | e
cv2.ellipse(lg, (1640, 214), (21, 13), -8, 0, 360, 0, -1)   # e eye
cv2.line(lg, (1645, 236), (1695, 236), 0, 9)             # e aperture under the bar
logo = lg > 0
np.save(f"{D}/logo_mask.npy", logo)
# address line, re-typeset to sit under the logo
a, (x0, y0, x1, y1) = render_text("105 W. THOMAS ST.  ·  HAMMOND, LA.", "LibreCaslonText[wght].ttf", 300, {"wght": 600}, 0.09)
addr = a[y0:y1, x0:x1]
s = (logo.shape[1] * 0.62) / addr.shape[1]
addr = cv2.resize(addr, (int(addr.shape[1] * s), int(addr.shape[0] * s)), interpolation=cv2.INTER_AREA)
addr = roughen(np.pad(addr, 10).astype(np.float32), spread=1.2, grain=0.12)
gap = int(logo.shape[0] * 0.10)
Wc = logo.shape[1] + 80; Hc = logo.shape[0] + gap + addr.shape[0] + 80
c = np.zeros((Hc, Wc), bool); c[40:40 + logo.shape[0], 40:40 + logo.shape[1]] = logo
xa = (Wc - addr.shape[1]) // 2; ya = 40 + logo.shape[0] + gap
c[ya:ya + addr.shape[0], xa:xa + addr.shape[1]] |= addr
build_multi([(c, WINE)], Wc, Hc, 2700, f"{D}/toggery_logo_address_wine")          # 9 in wide chest
lg = np.pad(logo, 40)
build_multi([(lg, WINE)], lg.shape[1], lg.shape[0], 1050, f"{D}/toggery_logo_leftchest_wine")   # 3.5 in
print(logo.shape, c.shape)
