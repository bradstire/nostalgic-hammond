"""Rebuild place tiles from the CURRENT production masters on the print-assets branch (art audit 2026-11-21).

Usage: PRINT_ASSETS=/path/to/print-assets python3 scripts/place_tiles_from_masters.py
Writes public/images/<hm|sfv>/places/<tile>-{900,600}.{webp,avif} and -900.jpg.
Rule: a place tile always shows the master the live product prints from, never an earlier trace.
"""
import os
from PIL import Image, ImageFilter
PA = os.environ.get('PRINT_ASSETS', '/home/claude/pa')
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'images')
W, H = 900, 675
CARD = (243, 234, 208)

def hex2(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def art(rel): return Image.open(os.path.join(PA, rel)).convert('RGBA')

def fit(im, w, h):
    s = min(w / im.width, h / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)

def contain(im, bg, pad=0.1):
    c = Image.new('RGB', (W, H), bg)
    r = fit(im, W * (1 - 2 * pad), H * (1 - 2 * pad))
    c.paste(r, ((W - r.width) // 2, (H - r.height) // 2), r)
    return c

def card(im, w, h, margin=0.07, paper=CARD):
    """The art on a flat paper card (for ink-only masters)."""
    c = Image.new('RGBA', (w, h), paper + (255,))
    r = fit(im, w * (1 - 2 * margin), h * (1 - 2 * margin))
    c.alpha_composite(r, ((w - r.width) // 2, (h - r.height) // 2))
    return c

def place(canvas, im, x, y, shadow=True):
    if shadow:
        sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
        sh.paste((0, 0, 0, 90), (x + 4, y + 6, x + 4 + im.width, y + 6 + im.height))
        sh = sh.filter(ImageFilter.GaussianBlur(7))
        canvas.alpha_composite(sh)
    canvas.alpha_composite(im, (x, y))

def save(im, town, name):
    d = os.path.join(PUB, town, 'places'); p = os.path.join(d, name)
    im = im.convert('RGB')
    for w in (900, 600):
        r = im if w == W else im.resize((w, round(H * w / W)), Image.LANCZOS)
        r.save(f'{p}-{w}.webp', quality=82); r.save(f'{p}-{w}.avif', quality=60)
        if w == 900: r.save(f'{p}-{w}.jpg', quality=85)

HM = 'hammond/wave2/'
tiles = {}
# Hammond: seven wave-2 tiles were built 2026-10-23 from first-pass traces; the products print from these masters.
tiles['hm', 'didi-wa'] = contain(art(HM + 'didiwa_sign_charcoal_v2.png'), hex2('#f6f1e6'), 0.11)
tiles['hm', 'fiesta-club'] = contain(art(HM + 'fiesta_club_logo_v4.png'), hex2('#e9a23b'), 0.12)
tiles['hm', 'magnolia-inn'] = contain(art(HM + 'magnolia_sign_hammond_v5.png'), hex2('#dfe9e6'), 0.06)
tiles['hm', 'casa-de-fresa'] = contain(art(HM + 'casa_mark_v2.png'), hex2('#f1e8d2'), 0.08)

c = Image.new('RGBA', (W, H), hex2('#efe5cf') + (255,))
sign = fit(art(HM + 'toggery_sign_1color_wine_v2.png'), 260, 570)
logo = fit(art(HM + 'toggery_logo_leftchest_wine_v3.png'), 430, 300)
c.alpha_composite(sign, (110, (H - sign.height) // 2))
c.alpha_composite(logo, (400, (H - logo.height) // 2))
tiles['hm', 'toggery-shop'] = c

c = Image.new('RGBA', (W, H), hex2('#14171c') + (255,))
joy = card(art(HM + 'joy_pass_ink_v3.png'), 470, 327, 0.0)
gal = fit(art(HM + 'galaxy_pass_card_v2.png'), 470, 300)
place(c, joy, 70, 60); place(c, gal, 360, 350)
tiles['hm', 'joy-galaxy-drive-in'] = c

c = Image.new('RGBA', (W, H), hex2('#e6dcc3') + (255,))
ad = card(art(HM + 'rushs_ad_v2.png'), 590, 590, 0.05, (240, 232, 212))
place(c, ad, (W - 590) // 2, (H - 590) // 2)
tiles['hm', 'rushs-drive-in'] = c

# SFV: three wave-2 masters changed after the tiles were cut (same recipe as scripts/sfv_site_images.py).
S2 = 'sfv/wave2/'
tiles['sfv', 'after-dark'] = contain(art(S2 + 'sfv_fm_station.png'), hex2('#0e0e0e'), 0.1)
tiles['sfv', 'records-books'] = contain(art(S2 + 'sfv_moby_disc.png'), hex2('#a9dff6'), 0.08)
tiles['sfv', 'devonshire-downs'] = contain(art(S2 + 'sfv_devonshire_downs.png'), hex2('#f3ecdd'), 0.1)

for (town, name), im in tiles.items():
    save(im, town, name); print('built', town, name)
