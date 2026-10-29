import numpy as np, json, cv2, sys
from PIL import Image
exec(open('enc_sym.py').read().split('res = {}')[0])
Vh = json.load(open('enc_Vh.json'))
L = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
S = 300.0                                     # px per half-seam in the output
im = np.array(Image.open('encino2_x4.png').convert('RGB'))
Wo, Ho = int(2 * L * S + 200), int(2 * S + 200)
cx, cy = Wo / 2, Ho / 2
outimg = np.zeros((Ho, Wo, 3), np.uint8)
for face in ('L', 'R'):
    H = Himg2plane(face, np.array(Vh[face]))
    # plane (x,y) with x in [-1,1] normalized by tip; output pixel = (cx + x*L*S, cy + y*S)
    A = np.array([[L * S, 0, cx], [0, S, cy], [0, 0, 1]]) @ H
    w = cv2.warpPerspective(im, A, (Wo, Ho), flags=cv2.INTER_CUBIC)
    m = np.zeros((Ho, Wo), bool)
    if face == 'L': m[:, :int(cx)] = True
    else: m[:, int(cx):] = True
    outimg[m] = w[m]
Image.fromarray(outimg).save(f'enc_rect_L{L:.1f}.png')
json.dump(dict(L=L, S=S, Wo=Wo, Ho=Ho), open('enc_rect_meta.json', 'w'))
Image.fromarray(outimg).resize((Wo // 2, Ho // 2)).save('/tmp/claude-0/-home-claude/3ad67d26-ad11-5829-ad96-2a5bc3109ee4/scratchpad/enc_rect.png')
print(Wo, Ho)
