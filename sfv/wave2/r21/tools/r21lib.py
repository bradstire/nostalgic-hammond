"""R21 trace-prep helpers: colour select, clean inside the source shapes, rectify, preview."""
import numpy as np
from PIL import Image
from scipy import ndimage as nd
import cv2

SP = '/tmp/claude-0/-home-claude/3ad67d26-ad11-5829-ad96-2a5bc3109ee4/scratchpad'


def load(p):
    return np.array(Image.open(p).convert('RGB')).astype(np.int16)


def lum(im):
    return (im[..., 0] * 0.299 + im[..., 1] * 0.587 + im[..., 2] * 0.114)


def clean(m, speck=200, hole=150, open_r=0, close_r=0):
    """Remove specks, fill small holes (ink dropouts) - cleanup inside the source shapes only."""
    m = m.astype(bool)
    if open_r:
        m = nd.binary_opening(m, structure=disk(open_r))
    if close_r:
        m = nd.binary_closing(m, structure=disk(close_r))
    lab, n = nd.label(m)
    if n:
        sz = nd.sum(m, lab, range(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sz >= speck
        m = keep[lab]
    inv = ~m
    lab, n = nd.label(inv)
    if n:
        sz = nd.sum(inv, lab, range(1, n + 1))
        small = np.zeros(n + 1, bool); small[1:] = sz < hole
        m = m | small[lab]
    return m


def disk(r):
    y, x = np.mgrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def keep_largest(m, n=1):
    lab, k = nd.label(m)
    if k <= n:
        return m
    sz = nd.sum(m, lab, range(1, k + 1))
    idx = np.argsort(sz)[::-1][:n] + 1
    return np.isin(lab, idx)


def rectify(img, src_pts, dst_pts, size, interp=cv2.INTER_CUBIC):
    H = cv2.getPerspectiveTransform(np.float32(src_pts), np.float32(dst_pts))
    if img.dtype == bool:
        out = cv2.warpPerspective(img.astype(np.uint8) * 255, H, size, flags=cv2.INTER_LINEAR)
        return out > 127
    return cv2.warpPerspective(img.astype(np.uint8), H, size, flags=interp, borderMode=cv2.BORDER_REPLICATE).astype(np.int16)


def save(m, p, pad=0):
    m = m.astype(bool)
    if pad:
        m = np.pad(m, pad)
    Image.fromarray((m * 255).astype(np.uint8)).save(p)
    return p


def crop_to(m, pad=20):
    ys, xs = np.where(m)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), ys.max() + pad, max(xs.min() - pad, 0), xs.max() + pad
    return m[y0:y1 + 1, x0:x1 + 1], (x0, y0)


def preview(im, m, p, maxw=1400):
    """Source on the left, mask (ink black on white) on the right, same scale."""
    a = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)) if im is not None else None
    b = Image.fromarray(np.where(m, 0, 255).astype(np.uint8)).convert('RGB')
    if a is None:
        out = b
    else:
        out = Image.new('RGB', (a.width + b.width + 20, max(a.height, b.height)), 'white')
        out.paste(a, (0, 0)); out.paste(b, (a.width + 20, 0))
    if out.width > maxw:
        out = out.resize((maxw, int(out.height * maxw / out.width)), Image.LANCZOS)
    out.save(p)
    return p
