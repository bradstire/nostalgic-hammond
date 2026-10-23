import json
from PIL import Image
HERO = '/home/claude/hbsite/hero/out'; OUT = '/home/claude/nh-recovered/pixel-work/public/images/hb'
def save(img, base, widths):
    for w in widths:
        im = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS).convert('RGB')
        im.save(f'{base}-{w}.webp', 'WEBP', quality=80, method=6)
        im.save(f'{base}-{w}.avif', 'AVIF', quality=48)
wide = Image.open(HERO + '/hero_wide.png'); stack = Image.open(HERO + '/hero_stack.png')
save(wide, OUT + '/hero/wide', [800, 1200, 1600, 2400]); save(stack, OUT + '/hero/stack', [600, 750, 900, 1200])
json.dump({'wide': json.load(open(HERO + '/boxes_wide.json')), 'stack': json.load(open(HERO + '/boxes_stack.json'))}, open('/home/claude/nh-recovered/pixel-work/src/v2/hero-boxes.json', 'w'))
from PIL import ImageDraw, ImageFont
og = Image.new('RGB', (1200, 630), (244, 237, 224))
pc = wide.convert('RGB').resize((1036, 561), Image.LANCZOS); og.paste(pc, ((1200 - 1036) // 2, 8))
d = ImageDraw.Draw(og); d.rectangle((0, 576, 1200, 630), fill=(31, 61, 46))
f = ImageFont.truetype('/home/claude/hbsite/fonts/Oswald.ttf', 30)
try: f.set_variation_by_axes([600])
except Exception: pass
t = 'NOSTALGIC HATTIESBURG  ·  TEES, HATS, SOCKS & PRINTS'
w = d.textlength(t, font=f); d.text(((1200 - w) / 2, 586), t, font=f, fill=(246, 239, 225))
og.save(OUT + '/og.jpg', quality=86)
# place-page share images as JPG
import glob, os
for p in glob.glob(OUT + '/places/*-900.webp'):
    Image.open(p).convert('RGB').save(p.replace('.webp', '.jpg'), quality=84)
print('ok')
