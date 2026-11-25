"""Tiles for the business-name pages (/places/<name>), built from the CURRENT production masters on print-assets.

Usage: PRINT_ASSETS=/path/to/print-assets python3 scripts/name_tiles_from_masters.py
Writes public/images/<hb|sfv>/places/<tile>-{900,600}.{webp,avif} and -900.jpg (same recipe as place_tiles_from_masters.py).
Rule: a tile always shows the master the live product prints from, never an earlier trace.
"""
import os
from PIL import Image
PA = os.environ.get('PRINT_ASSETS', '/home/claude/pa')
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public', 'images')
W, H = 900, 675   # H is 900 for a tall master (the town file sets tileTall on that entry)

def hex2(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

def contain(rel, bg, pad, H=H):
    im = Image.open(os.path.join(PA, rel)).convert('RGBA')
    s = min(W * (1 - 2 * pad) / im.width, H * (1 - 2 * pad) / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c = Image.new('RGB', (W, H), bg)
    c.paste(r, ((W - r.width) // 2, (H - r.height) // 2), r)
    return c

def save(im, town, name):
    p = os.path.join(PUB, town, 'places', name)
    for w in (900, 600):
        r = im if w == W else im.resize((w, round(im.height * w / W)), Image.LANCZOS)
        r.save(f'{p}-{w}.webp', quality=82); r.save(f'{p}-{w}.avif', quality=60)
        if w == 900: r.save(f'{p}-{w}.jpg', quality=85)

TILES = {
    ('hb', 'camelot-music'): ('hattiesburg/wave2/camelot_v3_bag1974.png', '#f6f1e6', 0.09),
    ('sfv', 'gemco'): ('sfv/wave2/sfv_gemco_membership.png', '#f6f1e6', 0.1),
    ('sfv', 'leons-steak-house'): ('sfv/wave2/sfv_leons.png', '#f6f1e6', 0.07, 900),
    ('sfv', 'zodys'): ('sfv/wave2/sfv_zodys.png', '#101010', 0.1),
    ('sfv', 'white-front'): ('sfv/wave2/sfv_white_front.png', '#f6f1e6', 0.08),
    ('sfv', 'valley-plaza'): ('sfv/wave2/sfv_valley_plaza.png', '#161a20', 0.07, 900),
    ('hb', 'mississippi-britches'): ('hattiesburg/wave2/britches_cloverleaf_cream.png', '#262b45', 0.1),
    ('sfv', 'builders-emporium'): ('sfv/wave2/sfv_builders_emporium.png', '#0f84a6', 0.07, 900),
    ('sfv', 'biffs'): ('sfv/wave2/sfv_biffs.png', '#2b422e', 0.08, 900),
    ('sfv', 'phils-diner'): ('sfv/wave2/sfv_phils_diner.png', '#eeb5bd', 0.09),
}
for (town, name), (rel, bg, pad, *h) in TILES.items():
    save(contain(rel, hex2(bg), pad, *h), town, name); print('built', town, name)
