"""Nostalgic San Fernando Valley — typeset tee/hat masters, v1 (HQ, 2026-10-27).

Every line here is rendered straight from an OFL font (no tracing, no roughen, L31); masters are
300 dpi, binary alpha, one bank colour per print (white/cream on dark garments). Each master gets a
.prov.json sidecar declaring its typeset boxes for the S9 gate (toolkit/art_qa.py).

Usage: python3 typeset_v1_build.py OUTDIR FONTDIR
"""
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont

OUT, FD = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
DPI = 300

# Drive colour bank (NT_TOOLKIT R16) + white/cream for dark garments
RED = (139, 0, 0, 255)       # #8B0000
GOLD = (184, 134, 11, 255)   # #B8860B
NAVY = (0, 51, 102, 255)     # #003366
CREAM = (244, 236, 221, 255) # light ink on dark garments
WHITE = (255, 255, 255, 255)


def font(name, size, var=None):
    f = ImageFont.truetype(os.path.join(FD, name), size)
    if var:
        try:
            f.set_variation_by_name(var)
        except Exception:
            pass
    return f


class Canvas:
    """Lays lines top-to-bottom, centred; records every typeset box for the prov sidecar."""

    def __init__(self, W, H):
        self.W, self.H = W, H
        self.im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.typeset = []

    def text_width(self, txt, f, track):
        return sum(f.getlength(c) for c in txt) + track * (len(txt) - 1)

    def line(self, txt, fname, size, y, ink, track=0, var=None, fit=None, x=None, align='c'):
        """Draw a tracked line. fit=width shrinks/grows the size so the line spans exactly that width."""
        f = font(fname, size, var)
        if fit:
            w = self.text_width(txt, f, track * size / 100)
            size = max(8, int(size * fit / w))
            f = font(fname, size, var)
        tr = track * size / 100
        w = self.text_width(txt, f, tr)
        if x is None:
            x = (self.W - w) / 2
        elif align == 'r':
            x = x - w
        x0 = x
        top = bot = left = right = None
        for c in txt:
            bb = self.d.textbbox((x, y), c, font=f)
            if c.strip():
                top = bb[1] if top is None else min(top, bb[1])
                bot = bb[3] if bot is None else max(bot, bb[3])
                left = bb[0] if left is None else min(left, bb[0])
                right = bb[2] if right is None else max(right, bb[2])
            self.d.text((x, y), c, font=f, fill=ink)
            x += f.getlength(c) + tr
        box = [int(min(x0, left)) - 6, int(top) - 6, int(max(x, right)) + 6, int(bot) + 6]
        self.typeset.append([box, f"{fname} {size}px"])
        return box

    def save(self, name, pad=40):
        a = self.im.split()[3].point(lambda v: 255 if v >= 128 else 0)   # binary alpha (DTG rule)
        self.im.putalpha(a)
        bb = self.im.getbbox()
        crop = (bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad)
        im = self.im.crop(crop)
        rgb = Image.new('RGBA', im.size, (0, 0, 0, 0))
        # flatten colour under binary alpha so no fringe colours survive
        px = im.load(); po = rgb.load()
        ink = None
        for yy in range(0, im.size[1], 7):
            for xx in range(0, im.size[0], 7):
                if px[xx, yy][3]:
                    ink = px[xx, yy][:3]
                    break
            if ink:
                break
        solid = Image.new('RGBA', im.size, ink + (255,))
        solid.putalpha(im.split()[3])
        path = os.path.join(OUT, name + '.png')
        solid.save(path, dpi=(DPI, DPI))
        ts = [[[b[0] - crop[0], b[1] - crop[1], b[2] - crop[0], b[3] - crop[1]], f] for b, f in self.typeset]
        json.dump({'typeset': ts, 'exempt': self.exempt if hasattr(self, 'exempt') else [], 'redrawn': []},
                  open(os.path.join(OUT, name + '.prov.json'), 'w'), indent=1)
        print(name, solid.size, f"{solid.size[0]/DPI:.2f} x {solid.size[1]/DPI:.2f} in")
        return path


def star(d, cx, cy, r, ink):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=ink)


# ---------------------------------------------------------------- Greetings from San Fernando Valley
def greetings(ink, name):
    """After the 1950s 'Greetings from San Fernando Valley, Calif.' photo card (CSUN SFVH 2478/2920):
    our own setting of its banner copy. Condensed display caps = League Gothic; small copy = Oswald."""
    c = Canvas(3600, 2200)
    W = 3200
    b = c.line('GREETINGS FROM', 'Oswald[wght].ttf', 170, 80, ink, track=22, var='SemiBold')
    b = c.line('SAN FERNANDO VALLEY', 'LeagueGothic[wdth].ttf', 700, b[3] + 10, ink, track=1, fit=W)
    b2 = c.line('CALIF.', 'Oswald[wght].ttf', 150, b[3] + 26, ink, track=18, var='SemiBold', x=(3600 + W) / 2 - 6, align='r')
    # rule, then the card's tagline
    y = b2[3] + 30
    c.d.rectangle([(3600 - W) / 2, y, (3600 + W) / 2, y + 16], fill=ink)
    c.typeset.append([[int((3600 - W) / 2) - 6, int(y) - 6, int((3600 + W) / 2) + 6, int(y) + 22], 'rule'])
    c.line('THE FASTEST GROWING AREA OF LOS ANGELES', 'Oswald[wght].ttf', 140, y + 52, ink, track=10, var='Medium', fit=W)
    return c.save(name)


# ---------------------------------------------------------------- Valley Music Theatre
def vmt(ink, name):
    """Valley Music Theatre, Woodland Hills (opened July 6, 1964; theatre in the round under a dome).
    The dome is our own simple drawing (half-ellipse with ribs on a drum), not a trace of any photo."""
    c = Canvas(3600, 2700)
    d = c.d
    cx, base_y, rx, ry = 1800, 1050, 1050, 720
    # dome
    d.pieslice([cx - rx, base_y - ry, cx + rx, base_y + ry], 180, 360, fill=ink)
    # meridian ribs knocked out: half-ellipse arcs from the crown to the drum, like a ribbed dome
    # (each 22 px = 0.07 in, well above the 0.03 in gap floor)
    rib = 22
    for k in (-3, -2, -1, 1, 2, 3):
        rxk = abs(rx * math.sin(k * math.pi / 8))
        box = [cx - rxk, base_y - ry, cx + rxk, base_y + ry]
        d.arc(box, 270 if k > 0 else 180, 360 if k > 0 else 270, fill=(0, 0, 0, 0), width=rib)
    d.line([(cx, base_y - ry), (cx, base_y)], fill=(0, 0, 0, 0), width=rib)
    # one latitude ring
    d.arc([cx - rx * 0.62, base_y - ry * 0.62 - 260, cx + rx * 0.62, base_y + ry * 0.62 - 260], 200, 340, fill=(0, 0, 0, 0), width=rib)
    # crown ring
    # crown cap: covers the slivers where the meridian ribs converge
    d.ellipse([cx - 230, base_y - ry - 60, cx + 230, base_y - ry + 150], fill=ink)
    d.ellipse([cx - 120, base_y - ry - 5, cx + 120, base_y - ry + 85], fill=(0, 0, 0, 0))
    # drum (base band) with knocked-out window slots
    d.rectangle([cx - rx - 40, base_y, cx + rx + 40, base_y + 170], fill=ink)
    n = 17
    slot_w = (2 * rx + 80 - 60) / n
    for i in range(n):
        x0 = cx - rx - 40 + 30 + i * slot_w + 16
        d.rectangle([x0, base_y + 40, x0 + slot_w - 32, base_y + 130], fill=(0, 0, 0, 0))
    c.exempt = [[[cx - rx - 80, base_y - ry - 80, cx + rx + 80, base_y + 210], 'illustration: our own drawn dome, not lettering']]
    b = c.line('VALLEY MUSIC THEATRE', 'Graduate-Regular.ttf', 260, base_y + 260, ink, track=4, fit=2900)
    b = c.line('WOODLAND HILLS · CALIFORNIA', 'Oswald[wght].ttf', 150, b[3] + 40, ink, track=24, var='Medium')
    c.line('THEATRE IN THE ROUND · OPENED 1964', 'Oswald[wght].ttf', 120, b[3] + 30, ink, track=30, var='Regular')
    # crop offsets are applied in save(); exempt boxes are canvas coords, so shift them there too
    return save_with_exempt(c, name)


def save_with_exempt(c, name):
    ex = c.exempt
    c.exempt = []
    path = c.save(name)
    # recompute crop to shift exempt boxes into master coords
    a = c.im.split()[3]
    bb = a.getbbox()
    ox, oy = bb[0] - 40, bb[1] - 40
    prov = json.load(open(path[:-4] + '.prov.json'))
    prov['exempt'] = [[[b[0] - ox, b[1] - oy, b[2] - ox, b[3] - oy], r] for b, r in ex]
    json.dump(prov, open(path[:-4] + '.prov.json', 'w'), indent=1)
    return path


# ---------------------------------------------------------------- Cruise Night
def cruise(ink, name):
    """Van Nuys Boulevard's Wednesday cruise night (late 1950s until the city banned cruising there).
    Our own badge: Pacifico script (same script as the hat; Yellowtail read as a 0.76 deg tilt at the gate) + Oswald."""
    c = Canvas(3600, 2400)
    b = c.line('Cruise Night', 'Pacifico-Regular.ttf', 600, 60, ink, track=1.5, fit=2700)
    y = b[3] + 40
    c.d.rectangle([450, y, 3150, y + 14], fill=ink)
    c.typeset.append([[444, int(y) - 6, 3156, int(y) + 20], 'rule'])
    b = c.line('VAN NUYS BLVD.', 'Oswald[wght].ttf', 330, y + 50, ink, track=12, var='Bold', fit=2700)
    y = b[3] + 50
    c.d.rectangle([450, y, 3150, y + 14], fill=ink)
    c.typeset.append([[444, int(y) - 6, 3156, int(y) + 20], 'rule'])
    b = c.line('EVERY WEDNESDAY NIGHT', 'Oswald[wght].ttf', 150, y + 50, ink, track=26, var='Medium')
    cy = (b[1] + b[3]) / 2
    star(c.d, b[0] - 110, cy, 62, ink)
    star(c.d, b[2] + 110, cy, 62, ink)
    c.typeset.append([[int(b[0]) - 180, int(cy) - 70, int(b[0]) - 40, int(cy) + 70], 'star (drawn polygon)'])
    c.typeset.append([[int(b[2]) + 40, int(cy) - 70, int(b[2]) + 180, int(cy) + 70], 'star (drawn polygon)'])
    c.line('SAN FERNANDO VALLEY · CALIF.', 'Oswald[wght].ttf', 120, b[3] + 36, ink, track=30, var='Regular')
    return c.save(name)


# ---------------------------------------------------------------- San Fernando Drag Strip
def dragstrip(ink, name):
    """San Fernando Raceway, "the Pond" (1955 to late 1969; NHRA 2008). Our own lockup: slab caps + a checkered band."""
    c = Canvas(3600, 2400)
    b = c.line('SAN FERNANDO', 'AlfaSlabOne-Regular.ttf', 330, 60, ink, track=6, fit=2600)
    y = b[3] + 50
    # checkered band: 2 rows x 26 squares, 100 px squares (0.33 in)
    sq = 100; n = 26
    x0 = (3600 - n * sq) / 2
    for r in range(2):
        for i in range(n):
            if (i + r) % 2 == 0:
                c.d.rectangle([x0 + i * sq + 6, y + r * sq + 6, x0 + (i + 1) * sq - 7, y + (r + 1) * sq - 7], fill=ink)  # 12 px inset: squares never touch corner-to-corner
    c.d.rectangle([x0, y - 34, x0 + n * sq, y - 20], fill=ink)
    c.d.rectangle([x0, y + 2 * sq + 20, x0 + n * sq, y + 2 * sq + 34], fill=ink)
    c.typeset.append([[int(x0) - 6, int(y) - 28, int(x0 + n * sq) + 6, int(y + 2 * sq) + 28], 'checker (drawn squares)'])
    b = c.line('RACEWAY', 'AlfaSlabOne-Regular.ttf', 470, y + 2 * sq + 70, ink, track=6, fit=2600)
    c.line('SAN FERNANDO, CALIF. · 1955–1969', 'Oswald[wght].ttf', 150, b[3] + 50, ink, track=22, var='Medium', fit=2500)
    return c.save(name)


# ---------------------------------------------------------------- Phys. Ed. (R16 lockup, after hattiesburg_pe.py)
def arched(c, text, f, radius, ls, ink, top):
    adv = [f.getlength(ch) for ch in text]
    total = sum(adv) + ls * (len(text) - 1)
    a = -total / radius / 2
    cx = c.W / 2; cy = radius + top
    for ch, ad in zip(text, adv):
        mid = a + (ad / 2) / radius
        gw, gh = int(ad) + 40, int(f.size * 1.4)
        g = Image.new('RGBA', (gw, gh), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((20, 0), ch, font=f, fill=ink, stroke_width=11, stroke_fill=ink)
        g = g.rotate(-math.degrees(mid), resample=Image.BICUBIC, expand=True)
        x = cx + radius * math.sin(mid); y = cy - radius * math.cos(mid)
        c.im.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
        a += (ad + ls) / radius


def phys_ed(town, ink, name, size=430, radius=4300):
    """Generic gym-class lockup per R16: town name arched over a blank name plate + PHYSICAL ED.,
    one verified school colour. No school name, mascot or crest."""
    c = Canvas(3800, 2300)
    big = font('Graduate-Regular.ttf', size)
    arched(c, town, big, radius, 26, ink, 260)
    bb = c.im.getbbox()
    c.exempt = [[[bb[0] - 10, bb[1] - 10, bb[2] + 10, bb[3] + 10], 'LEVEL only: deliberate arch (Graduate set on a circle; house PE lockup)']]
    y0 = bb[3] + 70; pw, ph, st = 1500, 215, 24; x0 = (c.W - pw) // 2
    d = c.d
    tail, drop = 120, 62
    d.polygon([(x0 - tail, y0 + drop), (x0 + 40, y0 + drop), (x0 + 40, y0 + ph * .8 + drop), (x0 - tail, y0 + ph * .8 + drop), (x0 - tail + 48, y0 + ph * .4 + drop)], fill=ink)
    xa = x0 + pw - 40; xb = x0 + pw + tail
    d.polygon([(xa, y0 + drop), (xb, y0 + drop), (xb - 48, y0 + ph * .4 + drop), (xb, y0 + ph * .8 + drop), (xa, y0 + ph * .8 + drop)], fill=ink)
    d.rectangle([x0, y0, x0 + pw, y0 + ph], fill=ink)
    d.rectangle([x0 + st, y0 + st, x0 + pw - st, y0 + ph - st], fill=(0, 0, 0, 0))
    c.typeset.append([[x0 - tail - 6, y0 - 6, xb + 6, int(y0 + ph * .8 + drop) + 6], 'plate (drawn polygons)'])
    c.line('PHYSICAL ED.', 'Oswald[wght].ttf', 240, y0 + ph + 20, ink, track=6, var='SemiBold')
    return save_with_exempt(c, name)


# ---------------------------------------------------------------- Cruise Night hat (embroidery)
def cruise_hat(ink, name):
    """Dad-hat front, 5.0 x ~1.7 in at stitch size. Pacifico (heavier script than Yellowtail) so every
    stroke clears the 0.05 in floor and the lettering clears 0.25 in."""
    c = Canvas(1900, 800)
    b = c.line('Cruise Night', 'Pacifico-Regular.ttf', 300, 60, ink, track=5, fit=1560)
    c.line('VAN NUYS BLVD.', 'Oswald[wght].ttf', 110, b[3] + 8, ink, track=18, var='SemiBold', fit=1150)
    return c.save(name, pad=30)


if __name__ == '__main__':
    greetings(RED, 'sfv_greetings_red')
    greetings(CREAM, 'sfv_greetings_cream')
    vmt(CREAM, 'sfv_vmt_cream')
    cruise(GOLD, 'sfv_cruise_gold')
    dragstrip(RED, 'sfv_raceway_red')
    phys_ed('VAN NUYS', RED, 'sfv_pe_vannuys_crimson')
    phys_ed('SAN FERNANDO', GOLD, 'sfv_pe_sanfernando_gold', size=340, radius=7600)
    cruise_hat((255, 204, 0, 255), 'sfv_cruise_hat_gold')   # thread Gold #FFCC00
