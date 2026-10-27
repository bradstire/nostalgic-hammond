"""SFV framed-print files v1 (HQ 2026-10-27).
Sources (CSUN Oviatt San Fernando Valley History Digital Library):
  SFVH 2320  Postcard, Lankershim and Van Nuys Ranchos, c.1908 (West Valley Museum)  rights: "Public domain."
  SFVH 2354  Postcard, small farm ("A Little Land and a Living"), c.1919           rights: "Public domain."
  SFVH 1721  Burbank Brand peach can label, McKeon Canning Co., c.1922 (Burbank Historical Society);
             no copyright notice on the label (litho credit + "Reg. U.S. Pat. Off." only) -> PD for lack of notice.
Pipeline: Real-ESRGAN x4 (resr_ncnn) -> remove the scanner's burned-in "West Valley Museum" credit (inpaint,
only inside its box) -> light despeckle -> fit on a cream mat, 16x12 in landscape @300 dpi. No repainting.
Usage: python3 prints_v1_build.py SRDIR OUTDIR
"""
import sys, os, numpy as np, cv2
from PIL import Image, ImageFilter
SR, OUT = sys.argv[1], sys.argv[2]
MAT = (242, 235, 220)
W, H = 4800, 3600   # 16 x 12 in @ 300

def remove_stamp(img, box):
    """Inpaint bright stamp lettering inside box (x0,y0,x1,y1 as fractions of the image)."""
    a = np.array(img.convert('RGB'))
    h, w = a.shape[:2]
    x0, y0, x1, y1 = int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h)
    roi = a[y0:y1, x0:x1]
    bright = (roi.min(axis=2) > 185).astype(np.uint8) * 255
    bright = cv2.dilate(bright, np.ones((9, 9), np.uint8))
    mask = np.zeros(a.shape[:2], np.uint8); mask[y0:y1, x0:x1] = bright
    out = cv2.inpaint(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), mask, 9, cv2.INPAINT_TELEA)
    return Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB)), int(mask.sum() / 255)

def despeckle(img):
    a = np.array(img); med = cv2.medianBlur(a, 3)
    diff = np.abs(a.astype(int) - med.astype(int)).max(axis=2)
    a[diff > 70] = med[diff > 70]          # isolated hot pixels only
    return Image.fromarray(a)

def mat(img, name, maxw=4200, maxh=3000):
    s = min(maxw / img.width, maxh / img.height)
    card = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
    canvas = Image.new('RGB', (W, H), MAT)
    x = (W - card.width) // 2; y = (H - card.height) // 2 - 60     # optical centre, a touch high
    canvas.paste(card, (x, y))
    p = os.path.join(OUT, name + '_16x12.jpg'); canvas.save(p, quality=95, dpi=(300, 300))
    print(name, 'card', card.size, f'effective {img.width / (card.width / 300):.0f} ppi native-SR', p)

r = Image.open(os.path.join(SR, 'ranchos_x4.png')).convert('RGB')
r, n = remove_stamp(r, (0.60, 0.90, 1.0, 1.0)); print('ranchos stamp px', n)
mat(despeckle(r), 'sfv_ranchos_1908')

lf = Image.open(os.path.join(SR, 'littlefarms_x4.png')).convert('RGB')
lf, n = remove_stamp(lf, (0.0, 0.90, 0.35, 1.0)); print('littlefarms stamp px', n)
mat(despeckle(lf), 'sfv_littlefarms_1919')

b = Image.open(os.path.join(SR, 'burbank_x4.png')).convert('RGB')
b = b.crop((0, 0, 2600, b.height))      # left panel: bowl, BURBANK, Yellow Cling Peaches
mat(despeckle(b), 'sfv_burbank_label_1922')
