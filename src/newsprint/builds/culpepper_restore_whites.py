"""Restore the duck's white areas that the AI upscale filled in (Brad 10-22: open up face, shirt, arm).
Source of truth = the original 1968 scan (Kepper's post), registered to the 3150-px layout (corr 0.966).
White in the original + inside the upscaled silhouette (eroded by `outline`) is carved out, so every restored
white area keeps a clean black outline of controlled thickness — like the printed ad."""
import numpy as np, cv2
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb/culpepper"

def orig_in_layout(shape):
    o = cv2.imread(f"{D}/../ref/culpepper/post1.jpg", 0).astype(np.float32)
    M = np.load(f"{D}/sr2orig_affine.npy")
    up = cv2.warpAffine(o, M, (shape[1], shape[0]), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderValue=255)
    return cv2.bilateralFilter(up, 9, 40, 9)

def disk(r): return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))

def carve(sil, orig_gray, outline, min_area, thresh=140, min_width=0):
    """sil: bool silhouette (region), orig_gray: registered original (same region). Returns (new_ink, carve_mask)."""
    white = orig_gray >= thresh
    inner = cv2.erode(sil.astype(np.uint8), disk(outline)) > 0
    c = white & inner
    c = cv2.morphologyEx(c.astype(np.uint8), cv2.MORPH_OPEN, disk(3)) > 0
    if min_width:   # embroidery: drop white slivers narrower than min_width (they'd close up when stitched)
        c = cv2.morphologyEx(c.astype(np.uint8), cv2.MORPH_OPEN, disk(min_width // 2)) > 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(c.astype(np.uint8), 8)
    c = np.isin(lab, [i for i in range(1, n) if st[i, 4] >= min_area])
    c = cv2.morphologyEx(c.astype(np.uint8), cv2.MORPH_CLOSE, disk(4)) > 0     # smooth the carved shapes
    return sil & ~c, c
