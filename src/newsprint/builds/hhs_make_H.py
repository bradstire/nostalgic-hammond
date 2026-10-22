"""HHS 'H' v3 — from real typefaces (OFL), not the photo trace.
TESTED   : Pirata One (OFL). Textura capital H built the textura way = the face's own H left stroke
           (stem + crossbar spur, spur cut on a pen angle) + the face's own lowercase h at cap height,
           leaned to the 1983 jersey's slant.
CHOSEN   : Manufacturing Consent (OFL) capital H as drawn (classic Old English H: top flag, mid spur, sweeping foot = the jersey letter's left half), leaned to the jersey slant. Pirata composite read as lowercase "lh" -> rejected.
Output: high-res raster from font outlines -> potrace -> SVG (clean curves) -> 300dpi renders downstream."""
import sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
HB = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb"
sys.path.insert(0, f"{HB}/lib")
from newsprint import vectorize, render_svg
FD = f"{HB}/fonts_bl"
SZ = 3000            # glyph em size in px -> ~2000 px cap height: clean outlines for tracing
LEAN = -0.18         # x shift per px of height (matches the jersey's forward slant, ~10 deg)

def glyph(path, ch):
    f = ImageFont.truetype(path, SZ); im = Image.new("L", (int(SZ * 1.6), int(SZ * 1.4)), 0)
    ImageDraw.Draw(im).text((int(SZ * 0.2), int(SZ * 0.1)), ch, font=f, fill=255)
    a = np.array(im) > 127; ys, xs = np.where(a); return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def lean(m, sh=LEAN):
    H, W = m.shape; M = np.float32([[1, sh, max(0, -sh * H)], [0, 1, 0]])
    o = cv2.warpAffine(m.astype(np.uint8) * 255, M, (int(W + abs(sh) * H) + 4, H), flags=cv2.INTER_CUBIC) > 127
    ys, xs = np.where(o); return o[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def pirata_H():
    p = f"{FD}/PirataOne-Regular.ttf"
    H = glyph(p, "H"); h = glyph(p, "h")
    w = H.shape[1]; prof = H.sum(0); a, b = int(w * 0.3), int(w * 0.62)
    cut = a + int(np.argmin(prof[a:b]))                       # thinnest column between the stems = the crossbar
    L = H[:, :cut].copy()
    # stem's right edge at crossbar height -> cut the spur on a 45-degree pen angle instead of a flat chop
    rows = np.where(L[:, -3])[0]                              # crossbar rows at the cut
    if rows.size:
        y0, y1 = rows.min(), rows.max(); stem_r = np.where(L[(y0 - 40), :])[0].max()
        spur_len = int((cut - stem_r) * 0.55)
        yy, xx = np.mgrid[0:L.shape[0], 0:L.shape[1]]
        kill = (xx > stem_r + spur_len - (yy - y0) * 0.9) & (yy >= y0 - 2) & (yy <= y1 + 2) & (xx > stem_r)
        L[kill] = False
    ys, xs = np.where(L); L = L[:, xs.min():xs.max() + 1]      # keep vertical registration with H
    capH = H.shape[0]
    hh = cv2.resize(h.astype(np.uint8) * 255, (int(h.shape[1] * capH / h.shape[0]), capH), interpolation=cv2.INTER_AREA) > 127
    gap = int(capH * 0.05)                                    # two separate pieces, like the jersey; >= 0.05in at hat size
    out = np.zeros((capH, L.shape[1] + gap + hh.shape[1]), bool)
    out[:, :L.shape[1]] |= L[:capH]; out[:, L.shape[1] + gap:] |= hh
    return lean(out)

def mc_H():
    return lean(glyph(f"{FD}/ManufacturingConsent-Regular.ttf", "H"))

def to_svg(m, name):
    m = np.pad(m, 40)
    svg = vectorize(m, turdsize=80, alphamax=1.0, opttolerance=0.2)
    open(f"{HB}/ref/hhs/{name}.svg", "w").write(svg)
    r = render_svg(svg, m.shape[1] // 4, m.shape[0] // 4)
    return svg, r

if __name__ == "__main__":
    for fn, name in ((mc_H, "hhs_H_v3"),):
        m = fn(); svg, r = to_svg(m, name)
        n, _ = cv2.connectedComponents(r.astype(np.uint8)); print(name, m.shape, "pieces", n - 1)
    # comparison board: jersey (fused) | v2 trace | v3 primary | v3 alternate
    tiles = [np.array(Image.open(f"{HB}/ref/hhs/h_fused_bw.png").convert("L")) < 128]
    import re
    for f in ("hhs_oldenglish_H_connected", "hhs_H_v3"):
        s = open(f"{HB}/ref/hhs/{f}.svg").read(); w0, h0 = [int(v) for v in re.findall(r'width="(\d+)" height="(\d+)"', s)[0]]
        tiles.append(render_svg(s, int(w0 * 600 / h0), 600))
    cell = 640; B = Image.new("L", (cell * 3, cell + 40), 255); d = ImageDraw.Draw(B)
    for i, (t, lab) in enumerate(zip(tiles, ["1983 jersey (7-view fusion)", "v2 (photo trace, sent 10-21)", "v3: Manufacturing Consent H (OFL), jersey lean"])):
        t = t.astype(np.uint8) * 255; sc = 600 / t.shape[0]; t = cv2.resize(t, (int(t.shape[1] * sc), 600), interpolation=cv2.INTER_AREA)
        B.paste(Image.fromarray(255 - t), (i * cell + (cell - t.shape[1]) // 2, 10)); d.text((i * cell + 20, cell + 12), lab, fill=0)
    B.save(f"{HB}/hhs/hhs_H_v3_compare.png")
