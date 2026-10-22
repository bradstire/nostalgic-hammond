"""Duck v3 negative space (Brad 10-22: 'open up more negative space in the face and shirt area, arm').
The 1968 print is solid black there (ink spread; the registered original shows only glove-finger traces),
so these are drawn keylines in the ad's own cartoon idiom. Coordinates = FR region px (1267 x 1094, 3150-space).
w = keyline width in FR px: tee ~12, hat ~32 (= 0.05in at the 1.9in hat size)."""
import numpy as np, cv2
from face_redraw import face_cuts

KEYLINES = {
    "bill_base": [(398, 196), (388, 228), (390, 262), (402, 290)],          # bill meets face
    "collar":    [(300, 430), (338, 455), (362, 470), (392, 455), (430, 425)],  # collar V meeting the collar tab
    "sleeve":    [(330, 505), (312, 560), (296, 620), (300, 668)],          # near arm front edge down to the glove
    "armpit":    [(612, 552), (604, 500), (600, 452)],                       # spray arm vs torso (extends the white gap up)
    "cuff":      [(606, 352), (640, 340), (676, 326)],                       # spray-arm sleeve cuff at the wrist
}
FINGERS = [((664, 438), (16, 9), -20), ((676, 466), (16, 9), -20), ((684, 494), (14, 8), -20)]  # gun-hand glove (traces in the original)

def details(region, w=12, face_line=8):
    out = face_cuts(region, line=face_line).astype(np.uint8)
    for name, pts in KEYLINES.items():
        cv2.polylines(out, [np.array(pts, np.int32)], False, 0, thickness=w, lineType=cv2.LINE_8)
        for p in (pts[0], pts[-1]):                     # round caps
            cv2.circle(out, p, w // 2, 0, -1)
    s = max(1.0, w / 12)
    for c, ax, ang in FINGERS:
        cv2.ellipse(out, c, (int(ax[0] * s ** 0.5), int(ax[1] * s ** 0.5)), ang, 0, 360, 0, -1)
    return out > 0

def details_hat(region, w):
    """Embroidery weight (w = FR px for 0.05in at hat size): same face/keylines, every white cut >= w,
    eye and pupil enlarged so each stitches (pupil ~0.05in, white ring around it ~0.05in)."""
    out = region.copy().astype(np.uint8)
    P = lambda pts: np.array(pts, np.int32)
    cv2.polylines(out, [P([(150, 250), (205, 256), (232, 254)])], False, 0, int(w * 1.3))                                      # cap brim keyline (ends well behind the eye)
    cv2.ellipse(out, (344, 258), (int(w * 1.55), int(w * 1.75)), -10, 0, 360, 0, -1)                               # eye white: >= 0.05in black to the cap
    cv2.ellipse(out, (382, 264), (int(w * 0.55), int(w * 0.75)), -10, 0, 360, 1, -1)                               # pupil touches the front of the eye (pie-cut, looking at the gun): no floating island
    cv2.polylines(out, [P([(396, 276), (444, 262), (492, 241), (536, 218)])], False, 0, w)                         # bill line
    for name, pts in KEYLINES.items():
        if name in ("bill_base", "cuff"): continue   # bill_base merges with the eye, cuff pinches next to the gun at stitch width
        wk = int(w * 1.25)                         # 25% margin so cuts stay >= 0.05in after stroke rebuild
        cv2.polylines(out, [P(pts)], False, 0, thickness=wk)
        for p in (pts[0], pts[-1]): cv2.circle(out, p, wk // 2, 0, -1)
    # glove fingers omitted at hat size: the cuts are too small to stay open when stitched (kept on the tee)
    return out > 0

def thicken_outlines(b, min_px):
    """Grow black lines thinner than min_px — only into the background or large white areas
    (belly, cloud, tail), never into small white details."""
    def disk(r): return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    fat = cv2.morphologyEx(b.astype(np.uint8), cv2.MORPH_OPEN, disk(min_px // 2)) > 0
    thin = b & ~fat
    grow = (cv2.dilate(thin.astype(np.uint8), disk(min_px // 3)) > 0) & ~b
    inv = (~b).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(inv, 4)
    big = np.zeros(n, bool)
    for i in range(1, n):
        x, y, w_, h_, area = st[i]
        border = x == 0 or y == 0 or x + w_ >= b.shape[1] or y + h_ >= b.shape[0]
        big[i] = area > (min_px * 4) ** 2 and not border      # interior only: the outer silhouette is never bumped
    return b | (grow & big[lab])
