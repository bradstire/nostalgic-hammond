"""Magnolia Inn (motel & 24-hour restaurant, 1111 W. Thomas St., Hammond) — the roadside sign from the 1970s postcard
(IMG_7167/7168). Pipeline B: Real-ESRGAN x4 -> perspective rectified on the RESTAURANT board (a true rectangle) ->
'Magnolia' script, 'INN' and 'RESTAURANT' traced (the sign's own letters). Boards, frames and posts redrawn as clean
polygons at the rectified proportions. The magnolia emblem box is too small in the postcard to trace: redrawn as a
six-petal magnolia in the same white-on-black, petal outlines in the box's aqua."""
import sys, numpy as np, cv2
sys.path.insert(0, "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/lib")
from hmlib import remove_small, fill_small_holes, build_multi, disk
D = "/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/hm/magnolia"
RED, BLACK, WHITE, AQUA = (222, 66, 40), (28, 27, 26), (255, 255, 255), (205, 236, 228)
im = cv2.imread(f"{D}/sign_rect.png").astype(np.float32)
B, G, R = im[..., 0], im[..., 1], im[..., 2]; gray = im.mean(2)
H0, W0 = gray.shape
K = 4
def poly(pts): m = np.zeros((H0, W0), np.uint8); cv2.fillPoly(m, [np.int32(np.array(pts) * K)], 1); return m > 0
main = poly([(38, 58), (752, 180), (688, 450), (98, 452)])
rest = poly([(66, 530), (728, 538), (724, 688), (70, 682)])
FR = 13 * K
main_face = cv2.erode(main.astype(np.uint8), disk(FR)) > 0
rest_face = cv2.erode(rest.astype(np.uint8), disk(16 * K)) > 0
# traced letters
hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV); Hh_, Ss_, Vv_ = cv2.split(hsv)
redm = ((Hh_ < 16) | (Hh_ > 168)) & (Ss_ > 95) & (Vv_ > 80)          # red-orange paint incl. the sunlit letters
redm &= cv2.erode(main_face.astype(np.uint8), disk(6)) > 0
redm = fill_small_holes(remove_small(cv2.morphologyEx(redm.astype(np.uint8), cv2.MORPH_OPEN, disk(3)) > 0, 700), 2500)   # keeps the i-dot
n_, lab_, st_, _ = cv2.connectedComponentsWithStats(redm.astype(np.uint8), 8)
for i in range(1, n_):
    if st_[i, 4] < 15000:                                # the i-dot: photo glint cut a notch -> its convex hull
        cnt = cv2.findContours((lab_ == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0][0]
        tmp = redm.astype(np.uint8); cv2.fillPoly(tmp, [cv2.convexHull(cnt)], 1); redm = tmp > 0
redm = cv2.GaussianBlur(redm.astype(np.float32), (0, 0), 3.0) > 0.5
blk = Vv_ < 105
blk &= cv2.erode(rest_face.astype(np.uint8), disk(10)) > 0
blk = fill_small_holes(remove_small(cv2.morphologyEx(blk.astype(np.uint8), cv2.MORPH_OPEN, disk(3)) > 0, 4000), 3000)
blk = cv2.morphologyEx(blk.astype(np.uint8), cv2.MORPH_CLOSE, disk(8))
blk = cv2.morphologyEx(blk, cv2.MORPH_OPEN, disk(6)) > 0
blk = cv2.GaussianBlur(blk.astype(np.float32), (0, 0), 4.0) > 0.5
# posts
posts = poly([(182, 448), (207, 448), (207, 532), (182, 532)]) | poly([(578, 448), (605, 448), (605, 534), (578, 534)]) \
      | poly([(182, 684), (207, 684), (207, 790), (182, 790)]) | poly([(578, 686), (605, 686), (605, 790), (578, 790)])
# magnolia emblem box on top of the main board (front face square + mount)
bx0, by0, bs = 468, -52, 186                          # view px; box sits just above the board's top edge (short stem)
yy, xx = np.mgrid[:H0, :W0]
canvas_top = 160 * K                                   # extra room above for the box
def shift(m): return np.pad(m, ((canvas_top, 0), (0, 0)))
main, main_face, rest, rest_face, redm, blk, posts = map(shift, (main, main_face, rest, rest_face, redm, blk, posts))
H, W = main.shape
box = np.zeros((H, W), np.uint8)
X0, Y0, S = bx0 * K, (by0 + 160) * K, bs * K
cv2.rectangle(box, (X0, Y0), (X0 + S, Y0 + S), 1, -1)
mount = np.zeros((H, W), np.uint8)
top_y_at = lambda x: (58 + (180 - 58) * (x - 38) / (752 - 38) + 160) * K
mx = X0 + S // 2
cv2.rectangle(mount, (mx - 9 * K, Y0 + S), (mx + 9 * K, int(top_y_at(mx / K)) + 6 * K), 1, -1)
# six-petal magnolia (top view), white petals with aqua outline on the black box
petal = np.zeros((H, W), np.uint8); outline = np.zeros((H, W), np.uint8)
cxf, cyf = X0 + S / 2, Y0 + S / 2; rr = S * 0.30
for k in range(6):
    a = np.radians(90 + k * 60 + (12 if k % 2 else 0))
    c = (int(cxf + np.cos(a) * rr * 0.92), int(cyf - np.sin(a) * rr * 0.92))
    ax = (int(rr * 0.70), int(rr * 0.50)); ang = -np.degrees(a)
    cv2.ellipse(outline, c, (ax[0] + 3 * K, ax[1] + 3 * K), ang, 0, 360, 1, -1)
    cv2.ellipse(petal, c, ax, ang, 0, 360, 1, -1)
cv2.circle(outline, (int(cxf), int(cyf)), int(rr * 0.30) + 3 * K, 1, -1)
cv2.circle(petal, (int(cxf), int(cyf)), int(rr * 0.30), 1, -1)
# petal separations: redraw each petal over the others with its outline so they read as overlapping petals
petals_w = np.zeros((H, W), bool); petals_a = np.zeros((H, W), bool)
for k in [1, 3, 5, 0, 2, 4]:
    a = np.radians(90 + k * 60 + (12 if k % 2 else 0)); m1 = np.zeros((H, W), np.uint8); m2 = np.zeros((H, W), np.uint8)
    c = (int(cxf + np.cos(a) * rr * 0.92), int(cyf - np.sin(a) * rr * 0.92)); ax = (int(rr * 0.70), int(rr * 0.50)); ang = -np.degrees(a)
    cv2.ellipse(m2, c, (ax[0] + 3 * K, ax[1] + 3 * K), ang, 0, 360, 1, -1); cv2.ellipse(m1, c, ax, ang, 0, 360, 1, -1)
    petals_a |= m2 > 0; petals_w = (petals_w & ~(m2 > 0)) | (m1 > 0); petals_a &= ~petals_w
cc = np.zeros((H, W), np.uint8); cv2.circle(cc, (int(cxf), int(cyf)), int(rr * 0.30) + 3 * K, 1, -1)
cw = np.zeros((H, W), np.uint8); cv2.circle(cw, (int(cxf), int(cyf)), int(rr * 0.30), 1, -1)
petals_a = (petals_a | (cc > 0)) & ~(cw > 0); petals_w = (petals_w & ~(cc > 0)) | (cw > 0)
box = box > 0; mount = mount > 0
# layers (paint order): black (frames, posts, box, RESTAURANT letters), white face, aqua face, red, flower
black = (main & ~main_face) | (rest & ~rest_face) | posts | box | mount | blk
white = main_face & ~redm
aqua = (rest_face & ~blk) | (petals_a & box)
red = redm
flower_w = petals_w & box
layers = [(black & ~white & ~aqua & ~red & ~flower_w, BLACK), (white, WHITE), (aqua, AQUA), (red, RED), (flower_w, WHITE)]
ys, xs = np.where(black | white | aqua); y0, y1, x0, x1 = ys.min() - 30, ys.max() + 31, xs.min() - 30, xs.max() + 31
layers = [(m[y0:y1, x0:x1], c) for m, c in layers]
Hh, Ww = layers[0][0].shape
build_multi(layers, Ww, Hh, 2700, f"{D}/magnolia_sign")          # 9 in wide
np.save(f"{D}/script_red.npy", red[y0:y1, x0:x1])
print(Ww, Hh)
