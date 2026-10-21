"""Culpepper duck — face-detail redraw on the exact 1968 silhouette.
Cues read from the print: pie-cut eye (white slit at bill base), cap brim, bill.
Coordinates are duck_gray.png pixels (offset (1152,1152) in culp_gray_3150)."""
import cv2, numpy as np, sys
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/culpepper"

def face_cuts_hat(ink):
    """Embroidery weight: every cut and the pupil >= ~1.2 mm at 1.75in hat height (duck scale ~0.41)."""
    out = ink.copy().astype(np.uint8)
    P = lambda pts: np.array(pts, np.int32)
    cv2.ellipse(out, (338, 246), (38, 48), -10, 0, 360, 0, -1)                                            # big white eye
    cv2.ellipse(out, (352, 258), (20, 30), -10, 0, 360, 1, -1)                                            # pupil (>=1.2mm)
    return out > 0

def face_cuts(ink, k=1.0, line=8, eye_grow=0):
    """ink: bool duck mask in duck_gray coords (scale k). Cuts white face detail; returns bool."""
    out = ink.copy().astype(np.uint8)
    P = lambda pts: (np.array(pts, np.float32) * k).astype(np.int32)
    t = max(2, int(line * k))
    e = eye_grow
    # 1) cap/head keyline: cap's lower edge, back of head -> under the brim (stops above the eye)
    cv2.polylines(out, [P([(160, 250), (225, 256), (276, 244), (300, 214), (322, 182), (348, 152)])], False, 0, t, cv2.LINE_AA)
    # 2) eye: solid white oval, pupil pushed forward (looking at the spray gun), pie-cut highlight
    cv2.ellipse(out, (int(336 * k), int(246 * k)), (int((27 + e) * k), int((36 + e) * k)), -10, 0, 360, 0, -1)
    cv2.ellipse(out, (int(347 * k), int(252 * k)), (int(14 * k), int(22 * k)), -10, 0, 360, 1, -1)
    cv2.fillPoly(out, [P([(347, 252), (343, 230), (353, 232)])], 0)
    # 3) bill: mouth line separating upper/lower bill
    cv2.polylines(out, [P([(396, 276), (444, 262), (492, 241), (536, 218)])], False, 0, t, cv2.LINE_AA)
    return out > 0

if __name__ == "__main__":
    g = cv2.imread(f"{D}/duck_gray.png", 0)
    ink = g < 140
    red = face_cuts(ink)
    v = np.hstack([np.where(ink[:560, :760], 0, 255), np.full((560, 20), 180), np.where(red[:560, :760], 0, 255)]).astype(np.uint8)
    cv2.imwrite(f"{D}/face_redraw_compare.png", cv2.resize(v, None, fx=0.9, fy=0.9))
    print("ok")
