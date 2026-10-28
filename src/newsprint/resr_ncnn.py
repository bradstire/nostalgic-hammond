"""Real-ESRGAN via ncnn on CPU, tiled. Usage: python3 resr.py in.png out.png [model] [scale] [tile]"""
import sys, time, numpy as np, cv2, ncnn
MD = "/home/claude/sfv/sr/rs/models"
inp, outp = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "realesrgan-x4plus-anime"
scale = int(sys.argv[4]) if len(sys.argv) > 4 else 4
tile = int(sys.argv[5]) if len(sys.argv) > 5 else 160
pad = 10
net = ncnn.Net()
net.opt.use_vulkan_compute = False
net.opt.num_threads = 2
net.load_param(f"{MD}/{model}.param"); net.load_model(f"{MD}/{model}.bin")
img = cv2.imread(inp, cv2.IMREAD_COLOR)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
H, W, _ = rgb.shape
out = np.zeros((H*scale, W*scale, 3), np.float32)
t0 = time.time(); n = 0
ty = (H + tile - 1)//tile; tx = (W + tile - 1)//tile
for iy in range(ty):
    for ix in range(tx):
        y0, x0 = iy*tile, ix*tile
        y1, x1 = min(y0+tile, H), min(x0+tile, W)
        py0, px0 = max(y0-pad, 0), max(x0-pad, 0)
        py1, px1 = min(y1+pad, H), min(x1+pad, W)
        patch = np.ascontiguousarray(rgb[py0:py1, px0:px1].transpose(2,0,1))
        ex = net.create_extractor()
        ex.input("data", ncnn.Mat(patch))
        _, o = ex.extract("output")
        o = np.array(o).transpose(1,2,0)
        oy0, ox0 = (y0-py0)*scale, (x0-px0)*scale
        out[y0*scale:y1*scale, x0*scale:x1*scale] = o[oy0:oy0+(y1-y0)*scale, ox0:ox0+(x1-x0)*scale]
        n += 1
    print(f"row {iy+1}/{ty} {time.time()-t0:.0f}s", flush=True)
res = cv2.cvtColor((np.clip(out,0,1)*255).round().astype(np.uint8), cv2.COLOR_RGB2BGR)
cv2.imwrite(outp, res)
print("done", res.shape, f"{time.time()-t0:.0f}s")
