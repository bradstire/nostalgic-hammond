"""Beverly natural/navy front v2 (Brad 10-22: too much negative space under 'Beverly').
The y-descender forced the subline 1in below the script baseline. v2 tucks the subline block up under 'Bever',
ending left of the descender — classic script + tucked subline. Same art, same navy; just re-composed."""
import numpy as np, cv2
from PIL import Image
SRC = "/home/claude/nh-recovered/print-assets-repo/hattiesburg/beverly_front_navy.png"
a = np.array(Image.open(SRC)); al = a[..., 3] > 127
bands = [(42, 1231), (1529, 1796), (1846, 1928), (2064, 2264)]
script = al[:bands[0][1] + 1]
lines = [al[y0:y1 + 1] for y0, y1 in bands[1:]]
gaps = [bands[2][0] - bands[1][1], bands[3][0] - bands[2][1]]
# descender: script ink below the baseline region; find the left-most x of ink in the bottom 30% of the script
H = script.shape[0]
cols = np.where(script.any(0))[0]
colbot = np.array([np.where(script[:, c])[0].max() for c in cols])
med = np.median(colbot)
desc_cols = cols[colbot > med + 150]                                         # columns where ink drops well below the letters
desc_cols = desc_cols[desc_cols > cols.min() + (cols.max() - cols.min()) * 0.5]   # the y-descender is in the right half
desc_left = desc_cols.min()
body_bottom = int(np.percentile(colbot[cols < desc_left - 40], 95))           # letter bottoms left of the descender
xs = np.where(script.any(0))[0]; left = xs.min()
print("script h", H, "descender starts x", desc_left, "body bottom y", body_bottom)
def crop_x(m): c = np.where(m.any(0))[0]; return m[:, c.min():c.max() + 1]
lines = [crop_x(l) for l in lines]
blk_w0 = max(l.shape[1] for l in lines); blk_h0 = sum(l.shape[0] for l in lines) + sum(gaps)
avail = (desc_left - 90) - left
s = min(1.0, avail / blk_w0)
L = [cv2.resize(l.astype(np.float32), (int(l.shape[1] * s), max(1, int(l.shape[0] * s))), interpolation=cv2.INTER_AREA) > 0.5 for l in lines]
g = [int(x * s) for x in gaps]
top = body_bottom + int(0.16 * 300)
out_h = max(H, top + sum(l.shape[0] for l in L) + sum(g)) + 20
out = np.zeros((out_h, al.shape[1]), bool); out[:H] |= script
cx = left + avail / 2; y = top
for i, l in enumerate(L):
    x0 = int(cx - l.shape[1] / 2); out[y:y + l.shape[0], x0:x0 + l.shape[1]] |= l; y += l.shape[0] + (g[i] if i < len(g) else 0)
ys, xs = np.where(out); out = out[max(0, ys.min() - 20):ys.max() + 21, max(0, xs.min() - 20):xs.max() + 21]
rgba = np.zeros((*out.shape, 4), np.uint8); col = a[al][0, :3]; rgba[out, :3] = col; rgba[out, 3] = 255
Image.fromarray(rgba, "RGBA").save("beverly_front_navy_v2.png", dpi=(300, 300))
print("v2", out.shape, round(out.shape[1] / 300, 2), "x", round(out.shape[0] / 300, 2), "in; subline scale", round(s, 2), "colour", col)
b = Image.new("RGB", (out.shape[1], out.shape[0]), (236, 228, 210)); b.paste(Image.fromarray(rgba, "RGBA"), (0, 0), Image.fromarray(rgba, "RGBA"))
b.resize((out.shape[1] // 4, out.shape[0] // 4)).save("bev_navy_v2_view.png")
