"""Build public/images/sfv/* (hero, story, place tiles, og) from the SFV print + art masters in print-assets."""
import os
from PIL import Image
PA = '/home/claude/print-assets/sfv'
OUT = os.path.join(os.path.dirname(__file__), '..', 'public', 'images', 'sfv')
MAT = (242, 235, 220)

def unmat(path):
    im = Image.open(path).convert('RGB')
    from PIL import ImageChops
    bg = Image.new('RGB', im.size, MAT)
    d = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 18 else 0)
    return im.crop(d.getbbox())

def cover(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((r.width - w) * fx); y = round((r.height - h) * fy)
    return r.crop((x, y, x + w, y + h))

def contain(im, w, h, bg, pad=0.08):
    c = Image.new('RGB', (w, h), bg)
    s = min(w * (1 - 2 * pad) / im.width, h * (1 - 2 * pad) / im.height)
    r = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    if r.mode == 'RGBA': c.paste(r, ((w - r.width) // 2, (h - r.height) // 2), r)
    else: c.paste(r, ((w - r.width) // 2, (h - r.height) // 2))
    return c

def save(im, rel, sizes, jpg=None):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    for w in sizes:
        h = round(im.height * w / im.width); r = im.resize((w, h), Image.LANCZOS)
        r.save(f'{p}-{w}.webp', quality=82); r.save(f'{p}-{w}.avif', quality=60)
        if jpg and w == jpg: r.save(f'{p}-{w}.jpg', quality=85)

def hex2(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

ranchos = unmat(f'{PA}/prints/sfv_ranchos_1908_16x12.jpg')
little = unmat(f'{PA}/prints/sfv_littlefarms_1919_16x12.jpg')
burbank = unmat(f'{PA}/prints/sfv_burbank_label_1922_16x12.jpg')
print('cards', ranchos.size, little.size, burbank.size)

# hero: wide 2:1, tall 3:4 (both crop the painted valley, not the sky)
save(cover(ranchos, 2400, 1200, fy=0.6), 'hero/ranchos-wide', [2400, 1600, 1200, 800])
save(cover(ranchos, 1200, 1600, fx=0.5, fy=0.5), 'hero/ranchos-tall', [1200, 900, 600])
# story: whole artifact on cream, 4:3
for n, im in (('ranchos', ranchos), ('littlefarms', little), ('burbank', burbank)):
    save(contain(im, 900, 675, MAT, 0.05), f'story/{n}', [900, 600])
# place tiles 900x675 (+600) and a 900 jpg for og/meta
art = lambda n: Image.open(f'{PA}/{n}.png').convert('RGBA')
tiles = {
    'orchard-valley': cover(ranchos, 900, 675, fy=0.55),
    'greetings': contain(art('sfv_greetings_red'), 900, 675, hex2('#f6f1e6'), 0.1),
    'cruise-night': contain(art('sfv_cruise_gold'), 900, 675, hex2('#14171c'), 0.1),
    'valley-music-theatre': contain(art('sfv_vmt_cream'), 900, 675, hex2('#14171c'), 0.1),
    'phys-ed': contain(art('sfv_pe_vannuys_crimson'), 900, 675, hex2('#f3ecdd'), 0.1),
}
for n, im in tiles.items(): save(im, f'places/{n}', [900, 600], jpg=900)
cover(ranchos, 1200, 630, fy=0.55).save(os.path.join(OUT, 'og.jpg'), quality=85)
print('done')
