"""Hattiesburg social kit: avatar, Facebook cover, 6 launch posts (1080x1350)."""
import os, json, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
H = '/home/claude/hbsite'; PUB = '/home/claude/nh-recovered/pixel-work/public/images/hb'; PNG = H + '/png/master'
OUT = 'out'; os.makedirs(OUT, exist_ok=True)
PAPER = (244, 237, 224); INK = (30, 26, 22); BRICK = (168, 51, 31); PINE = (31, 61, 46); TILE = (233, 224, 204)
def fr(size, w=700):
    f = ImageFont.truetype(H + '/fonts/Fraunces.ttf', size)
    try: f.set_variation_by_axes([min(144, size), w, 50, 0])
    except Exception: pass
    return f
def it(size, w=600):
    f = ImageFont.truetype('Inter.ttf', size)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def ko(prefix):
    return Image.open(sorted(glob.glob(f'{PNG}/{prefix}*.png'))[0]).convert('RGBA')
def shadowed(img):
    a = img.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * .28))
    sh = Image.new('RGBA', img.size, (40, 30, 15, 0)); sh.putalpha(a)
    c = Image.new('RGBA', (img.width, img.height + 24), (0, 0, 0, 0)); c.alpha_composite(sh, (0, 18)); c.alpha_composite(img, (0, 0)); return c
def text_c(d, y, s, f, fill, W=1080, tracking=0):
    if tracking:
        w = sum(d.textlength(ch, font=f) for ch in s) + tracking * (len(s) - 1); x = (W - w) / 2
        for ch in s: d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + tracking
    else:
        w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill)
def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    if len(lines) == 2:   # balance two lines (no orphans)
        best = None
        for i in range(1, len(words)):
            a, b = ' '.join(words[:i]), ' '.join(words[i:])
            m = max(d.textlength(a, font=f), d.textlength(b, font=f))
            if m <= maxw and (best is None or m < best[0]): best = (m, [a, b])
        if best: lines = best[1]
    return lines
def base(eyebrow, headline):
    im = Image.new('RGBA', (1080, 1350), PAPER + (255,)); d = ImageDraw.Draw(im)
    text_c(d, 62, eyebrow.upper(), it(24, 650), BRICK, tracking=4)
    y = 104
    for ln in wrap(d, headline, fr(64), 920): text_c(d, y, ln, fr(64), INK); y += 74
    return im, d, y
def footer(d, line='NOSTALGIC HATTIESBURG  ·  NOSTALGICHATTIESBURG.COM'):
    d.rectangle((0, 1278, 1080, 1350), fill=PINE); text_c(d, 1300, line, it(24, 650), (246, 239, 225), tracking=2)
def tile(im, img, box, bg=TILE, r=26):
    x0, y0, x1, y1 = box; m = Image.new('L', (x1 - x0, y1 - y0), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, x1 - x0, y1 - y0), r, fill=255)
    t = Image.new('RGBA', (x1 - x0, y1 - y0), bg + (255,))
    if img is not None:
        i2 = img.copy(); i2.thumbnail((int((x1 - x0) * .9), int((y1 - y0) * .9)), Image.LANCZOS); i2 = shadowed(i2)
        t.alpha_composite(i2, ((t.width - i2.width) // 2, (t.height - i2.height) // 2))
    im.paste(t, (x0, y0), m)
def cover_img(im, img, box, r=26):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0; s = max(w / img.width, h / img.height)
    i2 = img.convert('RGBA').resize((int(img.width * s) + 1, int(img.height * s) + 1), Image.LANCZOS)
    i2 = i2.crop(((i2.width - w) // 2, (i2.height - h) // 2, (i2.width - w) // 2 + w, (i2.height - h) // 2 + h))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), r, fill=255); im.paste(i2, (x0, y0), m)
def caption_line(d, y, s, size=30, fill=INK, w=500):
    text_c(d, y, s, it(size, w), fill)

hero_s = Image.open(H + '/hero/out/hero_stack.png'); hero_w = Image.open(H + '/hero/out/hero_wide.png')
# avatar (circle-safe) + FB cover
av = Image.new('RGB', (1080, 1080), PAPER); hs = hero_s.resize((1080, 1080), Image.LANCZOS); av.paste(hs.crop((90, 200, 1170, 1280)).resize((1080, 1080)) if False else hs)
av.save(f'{OUT}/avatar_1080.jpg', quality=92)
cv = Image.new('RGB', (1640, 624), PAPER); hw = hero_w.resize((1152, 624), Image.LANCZOS); cv.paste(hw, ((1640 - 1152) // 2, 0)); cv.save(f'{OUT}/fb_cover_1640x624.jpg', quality=92)

# 1 teaser: the postcard
im, d, y = base('Opening Monday, Oct. 26', 'Every letter is a piece of old Hattiesburg')
pc = hero_s.convert('RGB').resize((880, 880), Image.LANCZOS); im.paste(pc, (100, y + 30))
caption_line(d, y + 950, 'How many can you name?', 34, BRICK, 650)
footer(d); im.convert('RGB').save(f'{OUT}/post1_postcard.jpg', quality=90)

P = {
 'bev': 'mens-premium-short-sleeve-tee-black-front-6adb01d960eab', 'bevnat': 'mens-premium-short-sleeve-tee-vintage-white-front-6adb01b32d332',
 'bag': 'mens-premium-short-sleeve-tee-white-front-6adafc899e79a', 'camhat': 'classic-dad-hat-white-front-6adb047babf6a',
 'hubtee': 'mens-premium-short-sleeve-tee-white-front-6adb018a655d7', 'hubhat': 'classic-dad-hat-stone-front-6adb04564aa66',
 'spdtee': 'mens-premium-short-sleeve-tee-vintage-white-front-6adb00aa87c0f', 'spdhat': 'classic-dad-hat-stone-front-6adb04e24c52d',
 'culp': 'mens-premium-short-sleeve-tee-white-front-6adb00f66ba1a', 'ringer': 'unisex-ringer-t-shirt-natural-black-front-6adaffa43c637',
 'main': 'enhanced-matte-paper-framed-poster-_in_-black-12x18-front-6ad6de2a59731', 'hubprint': 'enhanced-matte-paper-framed-poster-_in_-black-12x12-front-6adb0628a7a06',
}
K = lambda k: Image.open(f'{PNG}/{P[k]}.png').convert('RGBA')
def label(d, x, y, w, t1, t2):
    f1, f2 = it(26, 600), it(26, 700)
    lw = d.textlength(t1, font=f1); d.text((x + (w - lw) / 2, y), t1, font=f1, fill=INK)
    lw = d.textlength(t2, font=f2); d.text((x + (w - lw) / 2, y + 34), t2, font=f2, fill=INK)

# 2 Beverly
im, d, y = base('Beverly Drive-In Theatre · 1948–2005', 'Double features under the pines on Highway 49')
cover_img(im, Image.open(f'{PUB}/places/beverly-drive-in-900.webp'), (80, y + 24, 1000, y + 420))
tile(im, K('bev'), (80, y + 448, 530, y + 898)); tile(im, K('bevnat'), (550, y + 448, 1000, y + 898))
d = ImageDraw.Draw(im); label(d, 80, y + 912, 920, 'The Beverly Drive-In Theatre Tee, black or vintage white', '$34')
footer(d); im.convert('RGB').save(f'{OUT}/post2_beverly.jpg', quality=90)

# 3 Camelot
im, d, y = base('Cloverleaf Mall · Opened 1974', 'Records at Camelot, Saturday at Cloverleaf')
cover_img(im, Image.open(f'{PUB}/story/camelot-900.webp'), (80, y + 24, 1000, y + 420))
tile(im, K('bag'), (80, y + 448, 530, y + 898)); tile(im, K('camhat'), (550, y + 448, 1000, y + 898))
d = ImageDraw.Draw(im); label(d, 80, y + 912, 920, 'Camelot Music Rainbow Bag Tee $34 · Camelot Music Hat $32', 'Not affiliated with any current owner of the Camelot Music name.')
footer(d); im.convert('RGB').save(f'{OUT}/post3_camelot.jpg', quality=90)

# 4 Hub City
im, d, y = base('Hub City Drag Raceway · 1966', '"FORD vs. CHEVY!" Three miles north on I-59')
ad = Image.open(f'{PUB}/story/hubcity-900.webp').convert('RGBA'); ad.thumbnail((900, 392), Image.LANCZOS)
d.rounded_rectangle((80, y + 24, 1000, y + 420), 26, fill=(236, 226, 203)); im.alpha_composite(ad, ((1080 - ad.width) // 2, y + 24 + (396 - ad.height) // 2))
tile(im, K('hubtee'), (80, y + 448, 530, y + 898)); tile(im, K('hubhat'), (550, y + 448, 1000, y + 898))
d = ImageDraw.Draw(im); label(d, 80, y + 912, 920, 'Restored from the 1966 newspaper ad, newsprint grain and all', 'Tee $34 · Hat $32')
footer(d); im.convert('RGB').save(f'{OUT}/post4_hubcity.jpg', quality=90)

# 5 Launch: we're open
im, d, y = base('Now open', 'Lost Hattiesburg, ready to wear')
keys = ['bev', 'bag', 'camhat', 'hubtee', 'ringer', 'main']; gw = 290; gap = 25; x0 = (1080 - 3 * gw - 2 * gap) // 2
for i, k in enumerate(keys):
    x = x0 + (i % 3) * (gw + gap); yy = y + 30 + (i // 3) * (gw + gap); tile(im, K(k), (x, yy, x + gw, yy + gw), r=20)
d = ImageDraw.Draw(im)
yy = y + 30 + 2 * (gw + gap) + 10
for ln in ['Tees, hats, socks and framed prints redrawn and restored', 'from old Hattiesburg signs, ads and postcards.', 'Free US shipping on $60+ · Order by Dec 11 for Christmas']:
    caption_line(d, yy, ln, 28, INK, 500); yy += 42
footer(d); im.convert('RGB').save(f'{OUT}/post5_open.jpg', quality=90)

# 6 Gift pairs
im, d, y = base('Gift pairs · $66 · ships free', 'A tee and a hat for anyone who called it home')
rows = [('The Weekend', 'bev', 'hubhat'), ('The Mall Rat', 'bag', 'camhat'), ('The Supper Club', 'spdtee', 'spdhat')]
rh = 270
for i, (t, a, b) in enumerate(rows):
    yy = y + 30 + i * (rh + 22)
    tile(im, K(a), (80, yy, 80 + rh, yy + rh), r=20); tile(im, K(b), (80 + rh + 16, yy, 80 + 2 * rh + 16, yy + rh), r=20)
    d = ImageDraw.Draw(im); d.text((80 + 2 * rh + 50, yy + rh / 2 - 46), t, font=fr(46), fill=INK); d.text((80 + 2 * rh + 50, yy + rh / 2 + 12), '$66 · ships free', font=it(28, 600), fill=PINE)
footer(d, 'ORDER BY DEC 11 FOR CHRISTMAS  ·  NOSTALGICHATTIESBURG.COM'); im.convert('RGB').save(f'{OUT}/post6_pairs.jpg', quality=90)
print('ok')
