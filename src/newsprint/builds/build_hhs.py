"""HHS blackletter workaround variants (R17). Generic font letterforms only (never a trace of the jersey 'h').
One school color per product (signal-stack guardrail); no tiger, no 'HHS', no school name."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/lib")
from newsprint import render_text, to_rgba_ink
from teemock import place_print, sheet, chest

D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/hhs"
PURPLE, GOLD = (58, 16, 85), (184, 134, 11)

def m(text, font, ax, tr=0.0, xs=1.0, w=None, h=None):
    a, _ = render_text(text, font, 170, ax, tr, xs)
    ys, x_ = np.where(a > 0.5); a = a[ys.min():ys.max() + 1, x_.min():x_.max() + 1]
    sc = min(w / a.shape[1] if w else 1e9, h / a.shape[0] if h else 1e9)
    return cv2.resize(a, (int(a.shape[1] * sc), int(a.shape[0] * sc)), interpolation=cv2.INTER_AREA) > 0.5

def vstack(parts, gaps, W=None):
    W = W or max(p.shape[1] for p in parts)
    H = sum(p.shape[0] for p in parts) + sum(gaps)
    out = np.zeros((H, W), bool); y = 0
    for i, p in enumerate(parts):
        x = (W - p.shape[1]) // 2; out[y:y + p.shape[0], x:x + p.shape[1]] = p; y += p.shape[0] + (gaps[i] if i < len(gaps) else 0)
    return out

GR = "Graduate-Regular.ttf"
# V1: capital blackletter H over PHYS. ED. (Grenze Gotisch — generic textura capital)
H1 = m("H", "GrenzeGotisch[wght].ttf", {"wght": 800}, h=1500)
v1 = vstack([H1, m("PHYS. ED.", GR, None, 0.06, w=1500)], [110])
# V2: lowercase blackletter h (UnifrakturCook — font glyph, not the jersey device) + town line
H2 = m("h", "GrenzeGotisch[wght].ttf", {"wght": 820}, h=1550)
v2 = vstack([H2, m("HATTIESBURG", GR, None, 0.08, w=1900), m("PHYSICAL EDUCATION", GR, None, 0.10, w=1500)], [120, 50])
# V3: wordmark — Hattiesburg in blackletter, PHYS. ED. DEPT. beneath
v3 = vstack([m("Hattiesburg", "GrenzeGotisch[wght].ttf", {"wght": 760}, 0.0, 0.92, w=3000),
             m("PHYS. ED. DEPT.", GR, None, 0.10, w=1500)], [90])
designs = {"H_physed": v1, "h_hattiesburg": v2, "wordmark": v3}
paths = {}
for k, ink in designs.items():
    ink = np.pad(ink, 16)
    for n, rgb in (("purple", PURPLE), ("gold", GOLD)):
        p = f"{D}/hhs_{k}_{n}.png"; to_rgba_ink(ink, rgb).save(p, dpi=(300, 300)); paths[(k, n)] = p
    print(k, ink.shape, round(ink.shape[1] / 300, 2), "x", round(ink.shape[0] / 300, 2), "in")

NAT, WHITE, BLACK = (236, 228, 210), (250, 250, 250), (24, 24, 26)
combos = [("H_physed", "purple", NAT, (25, 25, 25), 6.0, "Natural ringer (black trim) / H Phys Ed / purple"),
          ("h_hattiesburg", "purple", NAT, (25, 25, 25), 7.0, "Natural ringer / h Hattiesburg / purple"),
          ("wordmark", "purple", WHITE, None, 10.5, "White tee / wordmark / purple"),
          ("H_physed", "gold", BLACK, None, 6.0, "Black tee / H Phys Ed / gold"),
          ("h_hattiesburg", "gold", BLACK, None, 7.0, "Black tee / h Hattiesburg / gold"),
          ("wordmark", "gold", BLACK, None, 10.5, "Black tee / wordmark / gold")]
sheet([chest(paths[(k, n)], g, print_w_in=w, W=560, top_in=2.6, label=l, ringer=r) for k, n, g, r, w, l in combos], cols=3).save(f"{D}/hhs_mocks.jpg", quality=88)
print("done")
