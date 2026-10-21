"""Flat tee mockup renderer (HQ). Places a binary-alpha print PNG on a tee silhouette.
Print scale: chest print width in inches -> pixels using a 22in-wide body (size L flat)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def tee_silhouette(W=1000, color=(255, 255, 255), ringer=None):
    H = int(W * 0.86)
    im = Image.new("RGB", (W, H), (236, 234, 230))
    d = ImageDraw.Draw(im)
    s = W / 1000.0
    body = [(300, 90), (390, 60), (430, 95), (500, 110), (570, 95), (610, 60), (700, 90),
            (900, 220), (830, 360), (745, 315), (745, 790), (255, 790), (255, 315), (170, 360), (100, 220)]
    body = [(x * s, y * s) for x, y in body]
    # soft shadow
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).polygon([(x + 8 * s, y + 10 * s) for x, y in body], fill=90)
    im.paste((200, 198, 194), mask=sh.filter(ImageFilter.GaussianBlur(10 * s)))
    d.polygon(body, fill=color)
    # collar
    trim = ringer or tuple(max(0, c - 22) for c in color)
    d.arc((390 * s, 40 * s, 610 * s, 150 * s), 20, 160, fill=trim, width=int(14 * s))
    if ringer:
        d.line([(900 * s, 220 * s), (830 * s, 360 * s)], fill=ringer, width=int(16 * s))
        d.line([(100 * s, 220 * s), (170 * s, 360 * s)], fill=ringer, width=int(16 * s))
    return im, s

def place_print(png_path_or_img, garment=(255, 255, 255), ink=None, print_w_in=10.5, W=1000, top_in=3.0, ringer=None, label=None):
    tee, s = tee_silhouette(W, garment, ringer)
    art = png_path_or_img if isinstance(png_path_or_img, Image.Image) else Image.open(png_path_or_img)
    art = art.convert("RGBA")
    if ink is not None:
        a = np.array(art); a[..., 0], a[..., 1], a[..., 2] = ink; art = Image.fromarray(a)
    body_w_px = 490 * s  # 22in body
    px_per_in = body_w_px / 22.0
    tw = int(print_w_in * px_per_in); th = int(art.height * tw / art.width)
    art = art.resize((tw, th), Image.LANCZOS)
    x = int(500 * s - tw / 2); y = int(150 * s + top_in * px_per_in)
    tee.paste(art, (x, y), art)
    if label:
        ImageDraw.Draw(tee).text((14 * s, 14 * s), label, fill=(90, 90, 90))
    return tee

def chest(png, garment, ink=None, print_w_in=10.5, W=900, top_in=3.0, label=None, ringer=None):
    """Crop of the chest area for legibility review."""
    t = place_print(png, garment, ink, print_w_in, W=W * 2, top_in=top_in, ringer=ringer)
    s = (W * 2) / 1000.0
    c = t.crop((int(230 * s), int(40 * s), int(770 * s), int(520 * s))).resize((W, int(W * 480 / 540)))
    if label:
        ImageDraw.Draw(c).text((10, 10), label, fill=(200, 200, 200) if sum(garment) < 380 else (80, 80, 80))
    return c

def sheet(images, cols=3, pad=16, bg=(236, 234, 230)):
    w, h = images[0].size
    rows = (len(images) + cols - 1) // cols
    out = Image.new("RGB", (cols * w + (cols + 1) * pad, rows * h + (rows + 1) * pad), bg)
    for i, im in enumerate(images):
        r, c = divmod(i, cols)
        out.paste(im, (pad + c * (w + pad), pad + r * (h + pad)))
    return out
