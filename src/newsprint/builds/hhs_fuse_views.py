import cv2, numpy as np
ims = []
for i in range(7):
    g = cv2.imread(f'h{i}_x4.png', 0).astype(np.float32) / 255.0
    ink = (g < 0.45).astype(np.float32)
    # keep the largest dark component cluster near center (the letter), drop collar/folds
    n, lab, st, cen = cv2.connectedComponentsWithStats((ink > 0).astype(np.uint8), 8)
    H, W = ink.shape
    keep = np.zeros_like(ink)
    for j in range(1, n):
        x, y, w, h, a = st[j]
        cx, cy = cen[j]
        if a > 150 and abs(cx - W / 2) < W * 0.35 and abs(cy - H / 2) < H * 0.42:
            keep[lab == j] = 1
    ims.append(keep)
ref = ims[5]  # most frontal/clean
fused = [ref]
warp_mode = cv2.MOTION_AFFINE
for i, im in enumerate(ims):
    if i == 5: continue
    M = np.eye(2, 3, dtype=np.float32)
    try:
        _, M = cv2.findTransformECC(cv2.GaussianBlur(ref, (0, 0), 4), cv2.GaussianBlur(im, (0, 0), 4), M, warp_mode,
                                    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-6), None, 5)
        al = cv2.warpAffine(im, M, (ref.shape[1], ref.shape[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        score = (al * ref).sum() / max(1, np.sqrt((al ** 2).sum() * (ref ** 2).sum()))
        print(i, "aligned, overlap", round(float(score), 3))
        if score > 0.55: fused.append(al)
    except cv2.error as e:
        print(i, "fail")
avg = np.mean(fused, axis=0)
print("fused from", len(fused))
cv2.imwrite('h_fused_avg.png', ((1 - avg) * 255).astype(np.uint8))
cv2.imwrite('h_fused_bw.png', np.where(avg > 0.5, 0, 255).astype(np.uint8))
