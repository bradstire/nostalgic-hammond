"""Embroidery file checker against Printful's flat-embroidery rules (checked 2026-10-22):
  front 5.5 x 2.0 in; side/back 2.0 x 1.0 in; letters >= 0.25 in tall; details >= 0.05 in;
  side/back text <= 5 characters per inch; negative space ideally >= 0.25 in (flat) — we hard-flag < 0.05 in;
  satin covers 0.05-0.5 in widths, wider areas become fill (fine), <= 6 thread colors.
Stroke and gap widths are measured on the medial axis (skeleton x 2 x distance), ignoring the last ~0.03 in
of tapered tips, and reported as the 2nd percentile ('thinnest sustained')."""
import numpy as np, cv2
from skimage.morphology import skeletonize
DPI = 300

def _ridge_widths(mask, tip_ignore_px=9):
    if not mask.any(): return np.array([])
    dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 5)
    sk = skeletonize(mask)
    # drop skeleton pixels near endpoints (tapered tips / serifs) — walk tip_ignore_px back from each endpoint
    k = np.ones((3, 3), np.uint8); nb = cv2.filter2D(sk.astype(np.uint8), -1, k) - sk
    ends = sk & (nb == 1)
    near_end = cv2.dilate(ends.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * tip_ignore_px + 1,) * 2)) > 0
    w = 2 * dt[sk & ~near_end]
    return w

def check(rgba_or_mask, placement="front", text=None):
    """placement: 'front' | 'back'. text: list of (string, cap_height_in, line_width_in) for the cpi/height checks."""
    if isinstance(rgba_or_mask, np.ndarray) and rgba_or_mask.dtype == bool: m = rgba_or_mask
    else: m = np.array(rgba_or_mask)[..., 3] > 127
    ys, xs = np.where(m); m = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    W, H = m.shape[1] / DPI, m.shape[0] / DPI
    limW, limH = (5.5, 2.0) if placement == "front" else (2.0, 1.0)
    ink_w = _ridge_widths(m)
    # white: gaps inside the design's bounding box (counters, letter spacing, cut lines); background beyond bbox excluded
    merges, closed = gap_events(m, 0.05)
    res = {"size_in": (round(W, 2), round(H, 2)), "size_ok": W <= limW + 0.01 and H <= limH + 0.01,
           "min_line_in": round(float(np.percentile(ink_w, 2)) / DPI, 3) if ink_w.size else None,
           "gaps_merging": merges, "holes_closing": closed}
    res["line_ok"] = res["min_line_in"] is not None and res["min_line_in"] >= 0.05 - 0.004
    res["gap_ok"] = merges == 0 and closed == 0
    if text:
        for s, cap, lw in text:
            n = len(s.replace(" ", "")) if placement == "front" else len(s)
            cpi = n / lw
            res.setdefault("text", []).append((s, cap, round(cpi, 2), cap >= 0.25 - 0.005 and (placement == "front" or cpi <= 5.0)))
    res["pass"] = res["size_ok"] and res["line_ok"] and res["gap_ok"] and all(t[3] for t in res.get("text", []))
    return res

def gap_events(m, gap_in=0.05):
    """Stitch test: grow thread by half the minimum gap. Count separate parts that merge and enclosed
    white areas (counters, cuts) that vanish."""
    r = int(round(gap_in * DPI / 2))
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    g = cv2.dilate(m.astype(np.uint8), k) > 0
    n0 = cv2.connectedComponents(m.astype(np.uint8), connectivity=8)[0]
    n1 = cv2.connectedComponents(g.astype(np.uint8), connectivity=8)[0]
    def holes(x):
        inv = np.pad(~x, 1, constant_values=True).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(inv, connectivity=4)
        return sum(1 for i in range(1, n) if lab[0, 0] != i and st[i, 4] >= 6)
    return max(0, n0 - n1), max(0, holes(m) - holes(g))

def enforce_min_stroke(m, min_in=0.05, margin_px=2, tip_ignore_px=9):
    """Rebuild every stroke thinner than min_in to exactly that width around its own medial axis.
    Tapered tips (last ~0.03in of a stroke) are left tapered — digitizers finish satin columns to a point."""
    min_px = min_in * DPI + margin_px
    dt = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
    sk = skeletonize(m)
    k3 = np.ones((3, 3), np.uint8); nb = cv2.filter2D(sk.astype(np.uint8), -1, k3) - sk
    ends = sk & (nb == 1)
    near_end = cv2.dilate(ends.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * tip_ignore_px + 1,) * 2)) > 0
    thin = sk & (2 * dt < min_px) & ~near_end
    r = int(np.ceil(min_px / 2))
    return m | (cv2.dilate(thin.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))) > 0)
