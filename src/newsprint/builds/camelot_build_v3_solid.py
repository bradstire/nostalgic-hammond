"""Camelot v3 SOLID letters (Brad 10-22 13:12: why keep the outline?). Reference check:
1970s paper bag = outlined (keyline + white channel); 1974 Cloverleaf storefront sign = solid raised letters;
1990s plastic bags = solid. So: sign + tri-stripe -> solid (reference-backed); bag design -> solid alternate offered."""
import sys
sys.path.insert(0, ".")
from build_v3 import *
if __name__ == "__main__":
    W = int(10.5 * DPI)
    cam = fit(camelot(), width_px=int(6.6 * DPI)); mus = fit(music(), width_px=int(5.3 * DPI))
    cx = W / 2; top = int(0.15 * DPI); R0 = int(4.6 * DPI); cy = top + R0 + int(0.12 * DPI)
    A = arcs(cx, cy, [R0 - i * int(0.42 * DPI) for i in range(3)], [int(0.24 * DPI)] * 3)
    cam = centered(cam, cx, cy - int(2.55 * DPI)); b = cam.bounds
    mus = centered(mus, cx, b[3] + int(0.16 * DPI)); b2 = mus.bounds
    loc = centered(locator("CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974", int(6.4 * DPI)), cx, max(b2[3], cy) + int(0.28 * DPI))
    H = int(loc.bounds[3] + 0.15 * DPI); word = unary_union([cam, mus])
    A = A.difference(word.buffer(0.12 * DPI, join_style="mitre", mitre_limit=2.5))
    save([(A, BLUE), (unary_union([word, loc]), RED)], W, H, "camelot_v3_bag1974_solid")
    one = at(fit(oneline(), width_px=int(10.0 * DPI)), int(0.25 * DPI), int(0.1 * DPI)); ob = one.bounds
    loc2 = centered(locator("CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974", int(6.8 * DPI)), (ob[0] + ob[2]) / 2, ob[3] + int(0.22 * DPI))
    H2 = int(loc2.bounds[3] + 0.1 * DPI); W2 = int(ob[2] + 0.25 * DPI)
    save([(one, RED), (loc2, BLUE)], W2, H2, "camelot_v3_sign_red_blue_solid")
    save([(one, RED), (loc2, WHITE)], W2, H2, "camelot_v3_sign_red_white_solid")
    sw = ob[2] - ob[0]; x0 = ob[0]; y0 = ob[3] + int(0.16 * DPI); bh = int(0.17 * DPI); gap = int(0.07 * DPI)
    bars = [box(x0, y0 + i * (bh + gap), x0 + sw, y0 + i * (bh + gap) + bh) for i in range(3)]
    loc3 = centered(locator("CLOVERLEAF MALL · HATTIESBURG, MISS. · EST. 1974", int(6.8 * DPI)), (ob[0] + ob[2]) / 2, y0 + 3 * (bh + gap) + int(0.12 * DPI))
    H3 = int(loc3.bounds[3] + 0.1 * DPI)
    save([(bars[0], YEL), (bars[1], CYAN), (unary_union([one, bars[2], loc3]), RED)], W2, H3, "camelot_v3_tristripe_solid")
