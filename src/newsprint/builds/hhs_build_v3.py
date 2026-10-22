"""HHS v3 (R17, Brad 10-22): Old English H from a real typeface — Manufacturing Consent (OFL) capital H,
the closest commercially usable match to the 1983 jersey letter (see make_H.py / font_match.py), leaned to the jersey slant."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text, to_rgba_ink, render_svg
from teemock import sheet, chest
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/hhs"
R = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/ref/hhs"
PURPLE, GOLD = (58, 16, 85), (184, 134, 11)
svg = open(f"{R}/hhs_H_v3.svg").read()
import re
w0, h0 = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', svg)[0]]
def letter(h):
    w = int(w0 * h / h0); return render_svg(svg, w, h)
def word(text, font, ax, w, tr=0.06):
    a, _ = render_text(text, font, 170, ax, tr)
    ys, xs = np.where(a > 0.5); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return cv2.resize(a, (w, int(a.shape[0] * w / a.shape[1])), interpolation=cv2.INTER_AREA) > 0.5
def vstack(parts, gaps):
    W = max(p.shape[1] for p in parts); H = sum(p.shape[0] for p in parts) + sum(gaps)
    out = np.zeros((H, W), bool); y = 0
    for i, p in enumerate(parts):
        x = (W - p.shape[1]) // 2; out[y:y + p.shape[0], x:x + p.shape[1]] = p; y += p.shape[0] + (gaps[i] if i < len(gaps) else 0)
    return out
GR = "Graduate-Regular.ttf"
H = letter(1400)
designs = {
    "H_physed": vstack([H, word("PHYS. ED.", GR, None, int(H.shape[1] * 0.92))], [120]),
    "H_hattiesburg_physed": vstack([H, word("HATTIESBURG", GR, None, 1900, 0.08), word("PHYSICAL EDUCATION", GR, None, 1500, 0.10)], [130, 50]),
    "H_only_leftchest": letter(1050),   # 3.5in left-chest mark
}
paths = {}
for k, m in designs.items():
    m = np.pad(m, 14)
    for n, rgb in (("purple", PURPLE), ("gold", GOLD)):
        p = f"{D}/hhs_v3_{k}_{n}.png"; to_rgba_ink(m, rgb).save(p, dpi=(300, 300)); paths[(k, n)] = p
    print(k, m.shape, round(m.shape[1] / 300, 2), "x", round(m.shape[0] / 300, 2), "in")
NAT, BLACK, WHITE = (236, 228, 210), (24, 24, 26), (250, 250, 250)
combos = [("H_physed", "purple", NAT, (25, 25, 25), 5.0, "Natural ringer / Old English H + PHYS. ED. / purple"),
          ("H_hattiesburg_physed", "purple", NAT, (25, 25, 25), 6.3, "Natural ringer / H + Hattiesburg Physical Education"),
          ("H_only_leftchest", "purple", WHITE, None, 3.5, "White tee / left-chest H (shown centered)"),
          ("H_physed", "gold", BLACK, None, 5.0, "Black tee / H + PHYS. ED. / gold"),
          ("H_hattiesburg_physed", "gold", BLACK, None, 6.3, "Black tee / H + Hattiesburg PE / gold"),
          ("H_physed", "purple", WHITE, None, 5.0, "White tee / H + PHYS. ED. / purple")]
sheet([chest(paths[(k, n)], g, print_w_in=w, W=560, top_in=2.6, label=l, ringer=r) for k, n, g, r, w, l in combos], cols=3).save(f"{D}/hhs_v3_mocks.jpg", quality=88)
# evidence board: jersey (7-view fusion) | v2 photo trace | v3 typeface letter (made by make_H.py)
from PIL import Image
Image.open(f"{D}/hhs_H_v3_compare.png").convert("RGB").save(f"{D}/hhs_v3_evidence.jpg", quality=90)
print("done")
