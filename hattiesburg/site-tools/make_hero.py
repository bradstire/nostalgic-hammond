"""Large-letter 'Greetings from Hattiesburg' postcard hero.
Each letter is filled with a lost place: public-domain MDAH postcards (Cooper Collection,
'no known copyright restrictions') and Nostalgic Hattiesburg's own restored artwork.
No generative imagery. Usage: python3 make_hero.py [layout] -> out/hero_<layout>.png
layout: wide (one line, desktop) | stack (two lines, mobile)
"""
import sys, os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps

random.seed(7); np.random.seed(7)
H = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(H, '..', 'fonts')
SP = '/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hb'
PA = '/home/claude/nh-recovered/print-assets-repo/hattiesburg'
OUT = os.path.join(H, 'out'); os.makedirs(OUT, exist_ok=True)

layout = sys.argv[1] if len(sys.argv) > 1 else 'wide'

def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)

def on_bg(path, bg, pad=0.0, scale=1.0):
    """Transparent print art composited on a garment/paper colour."""
    a = Image.open(path).convert('RGBA')
    if scale != 1.0:
        a = a.resize((int(a.width*scale), int(a.height*scale)), Image.LANCZOS)
    w, h = a.size; P = int(max(w, h)*pad)
    c = Image.new('RGBA', (w+2*P, h+2*P), bg)
    c.alpha_composite(a, (P, P))
    return c.convert('RGB')

def newsprint(img):
    """Restored ad art printed on aged newsprint."""
    a = np.asarray(img.convert('L')).astype(np.float32)/255.0
    base = np.array([236, 226, 203], np.float32)
    ink = np.array([38, 34, 30], np.float32)
    n = (np.random.rand(*a.shape)*0.06 - 0.03)[..., None]
    out = base*(a[..., None]) + ink*(1-a[..., None]) + n*255
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

# ---------- letter fills ----------
# Rule: no lettering inside a letter. Each fill is a photo (archive postcard / restored ad photo)
# or a bold pattern drawn from that place's own artwork, so nothing reads as a cropped word.
def _px(w, h, rgb):
    return np.ones((h, w, 3), np.float32) * np.array(rgb, np.float32)

def night(w, h, m=None):
    """Beverly Drive-In: a night sky over the screen, the theatre's teal glowing at the horizon."""
    yy = np.linspace(0, 1, h)[:, None, None]
    top = np.array([14, 20, 36], np.float32); bot = np.array([22, 52, 66], np.float32)
    a = top + (bot - top) * yy ** 1.6
    glow = np.clip((yy - 0.70) / 0.30, 0, 1) ** 1.3
    a = a * (1 - glow * 0.85) + np.array([92, 204, 198], np.float32) * glow * 0.85
    img = Image.fromarray(np.repeat(a, w, axis=1).clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img); rnd = random.Random(48)
    for _ in range(int(w * h / 2600)):
        x, y = rnd.randrange(w), rnd.randrange(int(h * 0.8)); r = rnd.choice([1, 1, 2, 2, 3])
        c = rnd.choice([(250, 244, 226), (220, 238, 240), (255, 236, 200)])
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    # the big outdoor screen, glowing, on its posts
    sw, sh_ = int(w * 0.62), int(h * 0.15); sx = (w - sw) // 2; sy = int(h * 0.60)
    d.rectangle((sx, sy, sx + sw, sy + sh_), fill=(236, 246, 240))
    d.rectangle((sx + int(sw * .18), sy + sh_, sx + int(sw * .18) + 6, int(h * .86)), fill=(20, 30, 40))
    d.rectangle((sx + int(sw * .82) - 6, sy + sh_, sx + int(sw * .82), int(h * .86)), fill=(20, 30, 40))
    for _ in range(6):
        x, y = rnd.randrange(int(w * .1), int(w * .9)), rnd.randrange(int(h * .05), int(h * .5)); L = rnd.randrange(9, 15)
        d.line((x - L, y, x + L, y), fill=(255, 250, 235), width=3); d.line((x, y - L, x, y + L), fill=(255, 250, 235), width=3)
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(255, 252, 240))
    return img

def tristripe(w, h, m=None):
    """Camelot Music: the 1970s bag's royal-blue rainbow arch over the tri-stripes."""
    a = _px(w, h, (246, 240, 226)); P = 132; band = 22; gap = 9
    cols = [(232, 178, 58), (200, 50, 43), (39, 71, 184)]
    for y0 in range(int(h * 0.36), h, P):
        for k, c in enumerate(cols):
            y = y0 + k * (band + gap); a[max(0, y):max(0, min(h, y + band))] = c
    img = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(img)
    cx, cy = w / 2, h * 0.31; R = w * 0.50; t = w * 0.055; g = w * 0.032
    for k in range(4):
        r = R - k * (t + g)
        d.pieslice((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(39, 71, 184))
        d.pieslice((cx - (r - t), cy - (r - t), cx + (r - t), cy + (r - t)), 180, 360, fill=(246, 240, 226))
    return img

def checker(w, h, m=None):
    """Hub City Drag Raceway: the checkered band from our drag-strip art."""
    s = max(28, int(w * 0.16)); a = _px(w, h, (240, 233, 216))
    for y in range(0, h, s):
        for x in range(0, w, s):
            if ((x // s) + (y // s)) % 2 == 0: a[y:y + s, x:x + s] = (28, 26, 24)
    return Image.fromarray(a.astype(np.uint8))

def speeds_sign(w, h, m=None):
    """Albert Speed's: the sign's brick-red panel, cream keyline and green-white-green band."""
    img = Image.fromarray(_px(w, h, (179, 48, 31)).astype(np.uint8)); d = ImageDraw.Draw(img)
    k = max(10, int(w * 0.07)); t = max(5, int(w * 0.035))
    d.rectangle((k, k, w - k - 1, h - k - 1), outline=(244, 232, 205), width=t)   # the panel's cream keyline
    k2 = k + t + max(6, int(w * 0.04))
    d.rectangle((k2, k2, w - k2 - 1, h - k2 - 1), outline=(244, 232, 205), width=max(2, t // 3))   # inner pinline, like the neon tube
    return img

def duck(w, h, m=None):
    """Culpepper Body & Paint: the 1968 ad's spray-gun duck, on newsprint."""
    base = Image.fromarray(_px(w, h, (236, 226, 203)).astype(np.uint8))
    dk = Image.open(f'{PA}/wave2/culpepper_duck_hat_embroidery.png').convert('RGBA')
    s = (h * 0.60) / dk.height; dk = dk.resize((int(dk.width * s), int(dk.height * s)), Image.LANCZOS)
    a = np.asarray(dk).astype(np.float32); a[..., :3] = np.array([34, 30, 27], np.float32)
    dk = Image.fromarray(a.astype(np.uint8))
    base.paste(dk, ((w - dk.width) // 2 + int(w * 0.04), int(h * 0.10)), dk)
    return newsprint(base)

def gym(w, h, m=None):
    """Phys. Ed.: natural ringer cloth, purple gym-sock stripes and our Old English H, whole."""
    a = _px(w, h, (78, 44, 128)); gold = (226, 172, 62)
    for yc in (0.08, 0.50):
        y = int(h * yc)
        for k in range(3): a[y + k * 24: y + k * 24 + 13] = gold
    img = Image.fromarray(a.astype(np.uint8))
    H = Image.open(f'{PA}/wave2/hhs_v5_H_only_leftchest_gold.png').convert('RGBA')
    if m is not None:
        mk = np.asarray(m) > 200
        # largest H that sits entirely inside the letter, searched from the bottom bowl up
        from scipy.ndimage import binary_erosion
        mk = binary_erosion(mk, iterations=6)   # keep a margin inside the keyline
        for hh in range(int(h * 0.40), 30, -4):
            ww = int(H.width * hh / H.height)
            if ww >= w: continue
            Hs = H.resize((ww, hh), Image.LANCZOS); ha = np.asarray(Hs)[..., 3] > 30
            for yy in range(h - hh - 2, int(h * 0.25), -3):
                for xx in range(max(0, (w - ww) // 2 - 12), min(w - ww, (w - ww) // 2 + 12) + 1, 3):
                    if mk[yy:yy + hh, xx:xx + ww][ha].all():
                        img.paste(Hs, (xx, yy), Hs); return img
    return img

def fills():
    f = {}
    m = Image.open(f'{SP}/main_90199_full.jpg').convert('RGB'); f['main99'] = m.crop((0, 0, m.width, int(m.height * .90)))   # drop printed caption
    m = Image.open(f'{SP}/main_90198_half.jpg').convert('RGB'); f['main98'] = m.crop((0, int(m.height * .12), m.width, m.height))  # drop caption + rooftop sign
    m = Image.open(f'{SP}/main_89943_half.jpg').convert('RGB'); f['main43'] = m.crop((330, 270, 1530, 800))  # photo only: no handwriting, no script
    pz = Image.open(f'{SP}/hb_pansy_full.jpg').convert('RGB'); W_, H_ = pz.size
    f['pansy'] = pz.crop((int(W_*.71), int(H_*.47), int(W_*.95), int(H_*.79)))        # lower petal, no captions
    bf = Image.open(f'{SP}/hb_butterfly_full.jpg').convert('RGB'); W_, H_ = bf.size
    f['butterfly'] = bf.crop((int(W_*.865), int(H_*.06), int(W_*.975), int(H_*.50)))  # outer wing, no captions
    ad = Image.open(f'{PA}/hubcity_ad_front_v3.png').convert('RGBA')
    bgw = Image.new('RGBA', ad.size, (255, 255, 255, 255)); bgw.alpha_composite(ad)
    f['mainR'] = f['main99']; f['mainG'] = f['main98']
    carsrc = newsprint(bgw.convert('RGB').crop((112, 1000, 1360, 1880)))   # the 999 Mustang, whole, with its road
    def hubcar(w, h, m=None, src=carsrc):
        # whole car across the T's top bar; the road continues down the stem
        car = src.resize((w, int(src.height * w / src.width)), Image.LANCZOS)
        out = Image.new('RGB', (w, h), (236, 226, 203))
        road = src.crop((0, int(src.height * .78), src.width, src.height)).resize((w, max(1, int(src.height * .22 * w / src.width))), Image.LANCZOS)
        y = car.height
        while y < h: out.paste(road, (0, y)); y += road.height
        out.paste(car, (0, 0))
        return out
    f['hubcar'] = hubcar
    f['beverly'] = night; f['camelot'] = tristripe; f['speeds'] = speeds_sign; f['culpepper'] = duck; f['physed'] = gym; f['checker'] = checker
    bf = Image.open(f'{SP}/hb_butterfly_full.jpg').convert('RGB'); W_, H_ = bf.size
    f['wing'] = bf.crop((int(W_*.362), int(H_*.27), int(W_*.408), int(H_*.62)))  # yellow + blue wing veins only
    return f

def cover(img, w, h, focus=(0.5, 0.5), zoom=1.0):
    iw, ih = img.size
    s = max(w/iw, h/ih)*zoom
    nw, nh = int(iw*s)+1, int(ih*s)+1
    im = img.resize((nw, nh), Image.LANCZOS)
    x = int((nw-w)*focus[0]); y = int((nh-h)*focus[1])
    return im.crop((x, y, x+w, y+h))

# ---------- textures ----------
def linen(w, h, strength=0.10):
    """Linen-finish crosshatch like 1930s-50s 'linen' postcards."""
    y = np.arange(h)[:, None]; x = np.arange(w)[None, :]
    jx = np.random.rand(1, w)*2; jy = np.random.rand(h, 1)*2
    hz = (np.sin((y+jy)*2*math.pi/3.1) > 0.55).astype(np.float32)*(0.6+0.4*np.random.rand(h, 1))
    vt = (np.sin((x+jx)*2*math.pi/3.3) > 0.55).astype(np.float32)*(0.6+0.4*np.random.rand(1, w))
    t = np.clip(hz*0.6 + vt*0.5 + np.random.rand(h, w)*0.35, 0, 1.5)
    t = 1.0 - strength*t
    return t.astype(np.float32)

def sky(w, h):
    top = np.array([47, 96, 156], np.float32); mid = np.array([126, 172, 205], np.float32)
    hor = np.array([246, 228, 189], np.float32)
    yy = np.linspace(0, 1, h)[:, None, None]
    g = np.where(yy < 0.55, top + (mid-top)*(yy/0.55), mid + (hor-mid)*((yy-0.55)/0.45))
    img = np.repeat(g, w, axis=1)
    # soft clouds
    cl = np.zeros((h, w), np.float32)
    small = Image.fromarray((np.random.rand(h//40+1, w//40+1)*255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    cl = np.asarray(small.filter(ImageFilter.GaussianBlur(60))).astype(np.float32)/255.0
    cl = np.clip((cl-0.55)*3.0, 0, 1)*np.clip(1.2-yy[..., 0]*1.4, 0, 1)
    img = img*(1-cl[..., None]*0.55) + np.array([250, 246, 236], np.float32)*cl[..., None]*0.55
    return img

# ---------- compose ----------
WORD = 'HATTIESBURG'
STRETCH = 1.5
ASSIGN = ['main99', 'beverly', 'hubcar', 'camelot', 'speeds', 'main98', 'culpepper', 'checker', 'physed', 'mainR', 'mainG']
FOCUS = {'checker': (0.5,0.5,1), 'wing': (0.5, 0.5, 1.0), 'mainR': (0.56, 0.72, 1.3), 'mainG': (0.80, 0.55, 1.15), 'hubcar': (0.14, 0.62, 1.0), 'physed': (0.5,0.5,1), 'beverly': (0.5,0.5,1), 'camelot': (0.5,0.5,1), 'speeds': (0.5,0.5,1), 'culpepper': (0.5,0.5,1),
         'main99': (0.10, 0.55, 1.2), 'beverly': (0.22, 0.42, 1.05), 'hubcity': (0.25, 0.45, 2.8), 'camelot': (0.5, 0.20, 1.05),
         'speeds': (0.20, 0.36, 2.6), 'pansy': (0.5, 0.5, 1.0), 'culpepper': (0.52, 0.42, 1.7), 'main98': (0.18, 0.62, 1.25),
         'britches': (0.5, 0.5, 1.0), 'butterfly': (0.5, 0.5, 1.0), 'main43': (0.45, 0.55, 1.1), 'mainB': (0.85, 0.55, 1.6)}

def render(layout):
    global STRETCH
    if layout == 'wide':
        W, Hh = 2400, 1300
        lines = [WORD]; lsize = 470; top_y = 430; STRETCH = 1.55
    else:
        W, Hh = 1500, 1500
        lines = ['HATTIES', 'BURG']; lsize = 362; top_y = 330; STRETCH = 1.45
    bd = int(W*0.028)                       # white postcard border
    iw, ih = W-2*bd, Hh-2*bd
    card = sky(iw, ih)
    lf = font('AlfaSlabOne.ttf', lsize)
    fl = fills()
    canvas = Image.fromarray(np.clip(card, 0, 255).astype(np.uint8)).convert('RGBA')
    depth = int(lsize*0.085)
    idx = 0
    y = top_y
    global BOXES
    BOXES = []
    for li, line in enumerate(lines):
        # measure with tight tracking
        track = -int(lsize*0.035)
        boxes = [lf.getbbox(ch) for ch in line]
        widths = [b[2]-b[0] for b in boxes]
        total = sum(widths) + track*(len(line)-1)
        scale = min(1.0, (iw*0.94)/total)
        if scale < 1.0:
            lf2 = font('AlfaSlabOne.ttf', int(lsize*scale)); boxes = [lf2.getbbox(ch) for ch in line]
            widths = [b[2]-b[0] for b in boxes]; track = int(track*scale); total = sum(widths)+track*(len(line)-1)
        else:
            lf2 = lf
        x = (iw-total)//2
        ascent = max(b[3] for b in boxes)
        for ci, ch in enumerate(line):
            b = boxes[ci]; w = widths[ci]
            m = Image.new('L', (w+4, ascent+4), 0)
            ImageDraw.Draw(m).text((-b[0]+2, 2), ch, font=lf2, fill=255)
            m = m.crop((0, b[1], m.width, m.height))
            m = m.resize((m.width, int(m.height*STRETCH)), Image.LANCZOS)
            mh = m.height
            # extrusion (deep navy), stepping down-right
            ext = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
            for k in range(depth, 0, -1):
                col = (22+k//3, 34+k//4, 64+k//3, 255)
                ext.paste(Image.new('RGBA', m.size, col), (x+int(k*0.55), y+k), m)
            # drop shadow
            sh = Image.new('L', canvas.size, 0); sh.paste(m, (x+depth+10, y+depth+16))
            sh = sh.filter(ImageFilter.GaussianBlur(7))
            canvas = Image.composite(Image.new('RGBA', canvas.size, (30, 30, 50, 255)), canvas, sh.point(lambda v: int(v*0.28)))
            canvas.alpha_composite(ext)
            # cream outline ring
            ring = m.filter(ImageFilter.MaxFilter(9))
            canvas.paste(Image.new('RGBA', m.size, (250, 243, 226, 255)), (x-0, y-0), ring) if False else None
            big = Image.new('L', (m.width+28, m.height+28), 0); big.paste(m, (14, 14)); big = big.filter(ImageFilter.MaxFilter(17))
            canvas.paste(Image.new('RGBA', big.size, (251, 245, 230, 255)), (x-14, y-14), big)
            # fill
            key = ASSIGN[idx % len(ASSIGN)]; fx, fy, z = FOCUS[key]
            fimg = fl[key](m.width, m.height, m) if callable(fl[key]) else cover(fl[key], m.width, m.height, (fx, fy), z)
            # unify: warm tint + slight desat + inner shadow from top
            arr = np.asarray(fimg).astype(np.float32)
            gray = arr.mean(axis=2, keepdims=True)
            arr = arr*0.85 + gray*0.15
            arr = arr*np.array([1.03, 1.0, 0.94])
            grad = np.linspace(0.86, 1.04, m.height)[:, None, None]
            arr = np.clip(arr*grad, 0, 255)
            fimg = Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
            inner = m.filter(ImageFilter.MinFilter(3))
            canvas.paste(fimg, (x, y), inner)
            BOXES.append({'key': key, 'ch': ch, 'x': (x+bd)/W, 'y': (y+bd)/Hh, 'w': m.width/W, 'h': m.height/Hh})
            # thin dark keyline just inside
            edge = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(5)))
            canvas.paste(Image.new('RGBA', m.size, (28, 36, 62, 255)), (x, y), edge.point(lambda v: int(v*0.55)))
            x += w + track
            idx += 1
        y += int((ascent-min(bb[1] for bb in boxes))*STRETCH) + (int(lsize*0.10) if layout == 'stack' else 0)
    # 'Greetings from' script
    sf = font('Yellowtail.ttf', int((260 if layout == 'wide' else 210)))
    txt = 'Greetings from'
    tb = sf.getbbox(txt)
    tx = int(iw*0.06) if layout == 'wide' else int(iw*0.07)
    ty = top_y - (tb[3]-tb[1]) - (95 if layout == 'wide' else 70)
    tl = Image.new('L', canvas.size, 0); ImageDraw.Draw(tl).text((tx, ty), txt, font=sf, fill=255)
    sh = tl.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(3))
    canvas.paste(Image.new('RGBA', canvas.size, (24, 30, 54, 255)), (8, 10), sh)
    canvas.paste(Image.new('RGBA', canvas.size, (252, 247, 236, 255)), (0, 0), tl.filter(ImageFilter.MaxFilter(13)))
    canvas.paste(Image.new('RGBA', canvas.size, (196, 46, 38, 255)), (0, 0), tl)
    # bottom banner
    of = ImageFont.truetype(os.path.join(F, 'Oswald.ttf'), 104 if layout == 'wide' else 84)
    try:
        of.set_variation_by_axes([700])
    except Exception:
        pass
    btxt = 'THE HUB CITY  ·  MISSISSIPPI'
    bb = of.getbbox(btxt); bw = bb[2]-bb[0]; bh = bb[3]-bb[1]
    by = y + depth + (40 if layout == 'wide' else 30)
    bx = (iw-bw)//2
    rib = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); rd = ImageDraw.Draw(rib)
    padx, pady = 60, 34
    rd.polygon([(bx-padx-40, by-pady+bh//2+20), (bx-padx, by-pady), (bx+bw+padx, by-pady), (bx+bw+padx+40, by-pady+bh//2+20),
                (bx+bw+padx, by+bh+pady+30), (bx-padx, by+bh+pady+30)], fill=(178, 44, 36, 255))
    canvas.alpha_composite(rib)
    ImageDraw.Draw(canvas).text((bx-bb[0], by-bb[1]+12), btxt, font=of, fill=(251, 245, 230, 255))
    # linen texture over everything + warm age + vignette
    arr = np.asarray(canvas.convert('RGB')).astype(np.float32)
    arr *= linen(iw, ih, 0.11)[..., None]
    yy, xx = np.mgrid[0:ih, 0:iw]
    v = ((xx-iw/2)/(iw/2))**2 + ((yy-ih/2)/(ih/2))**2
    arr *= (1 - 0.10*np.clip(v-0.3, 0, 1))[..., None]
    arr = arr*np.array([1.0, 0.985, 0.95]) + np.array([4, 2, -2])
    inner = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    # white border with paper texture
    card = Image.new('RGB', (W, Hh), (247, 242, 230))
    ca = np.asarray(card).astype(np.float32)*linen(W, Hh, 0.05)[..., None]
    card = Image.fromarray(np.clip(ca, 0, 255).astype(np.uint8))
    card.paste(inner, (bd, bd))
    return card

if __name__ == '__main__':
    img = render(layout)
    p = os.path.join(OUT, f'hero_{layout}.png'); img.save(p)
    img.resize((img.width//2, img.height//2), Image.LANCZOS).save(os.path.join(OUT, f'hero_{layout}_half.jpg'), quality=88)
    import json; json.dump(BOXES, open(os.path.join(OUT, f'boxes_{layout}.json'), 'w'), indent=1)
    print(p, img.size, len(BOXES))
