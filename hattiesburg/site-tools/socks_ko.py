import glob, os
import numpy as np
from PIL import Image
from rembg import remove, new_session
s = new_session('isnet-general-use'); D = '/home/claude/nh-recovered/pixel-work/public/images/hb/socks'
for f in sorted(glob.glob(D + '/*-1080.webp')):
    h = os.path.basename(f)[:-len('-1080.webp')]
    out = remove(Image.open(f).convert('RGB'), session=s, post_process_mask=True)
    bb = out.split()[3].getbbox(); c = out.crop(bb); side = int(max(c.size) * 1.08)
    sq = Image.new('RGBA', (side, side), (0, 0, 0, 0)); sq.alpha_composite(c, ((side - c.width) // 2, (side - c.height) // 2))
    sq.save(f'master/{h}-front.png')
    for w in (360, 540, 800, 1080): sq.resize((w, w), Image.LANCZOS).save(f'{D}/{h}-{w}.webp', 'WEBP', quality=86, method=6, alpha_quality=90)
    print(h)
