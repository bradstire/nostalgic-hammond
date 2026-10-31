import sys, os, json, numpy as np, cv2
sys.path.insert(0,'/home/claude/print-assets/src/builds/sfv'); sys.path.insert(0,'/home/claude/print-assets/src/newsprint')
from w2lib import print_clean
from PIL import Image
L={n:cv2.imread(f'sep_{n}.png',0)>0 for n in ('cream','yellow','red')}
H,W=L['cream'].shape
# trim paper edges: left 40 px, right 52 px (x4 crop coords)
for n in L: L[n][:, :40]=False; L[n][:, W-52:]=False
xs=[];ys=[]
for m in L.values():
    yy,xx=np.where(m); xs+= [xx.min(),xx.max()]; ys+=[yy.min(),yy.max()]
bx0,bx1,by0,by1=min(xs),max(xs),min(ys),max(ys)
PRINT_W=10.5
ppi_src=(bx1-bx0)/PRINT_W
print('src bbox',bx0,bx1,by0,by1,'ppi',round(ppi_src,1),'height in',round((by1-by0)/ppi_src,2))
sys.path.insert(0,'/home/claude/sfvqa'); from fillholes import fill_small_holes
Lc={n:m[by0:by1+1,bx0:bx1+1] for n,m in L.items()}
Lc,nf=fill_small_holes(Lc, ppi_src, 0.035); print('filled',nf)
out={}
for n,m in Lc.items():
    c=print_clean(m, ppi_src)
    W3=int(round(PRINT_W*300)); H3=int(round(c.shape[0]*300/ppi_src))
    r=cv2.resize(c.astype(np.float32),(W3,H3),interpolation=cv2.INTER_AREA)>0.5
    out[n]=r; print(n,'ink sq in',round(r.sum()/90000,1))
pad=30
Hh,Ww=out['cream'].shape
rgba=np.zeros((Hh+2*pad,Ww+2*pad,4),np.uint8)
cols={'cream':(0xF4,0xEC,0xDD),'yellow':(0xF2,0xC9,0x4C),'red':(0xB3,0x3A,0x2B)}
for n in ('yellow','red','cream'):
    m=np.zeros(rgba.shape[:2],bool); m[pad:pad+Hh,pad:pad+Ww]=out[n]
    rgba[m,:3]=cols[n]; rgba[m,3]=255
Image.fromarray(rgba,'RGBA').save('sfv_biffs_concept.png',dpi=(300,300))
a=rgba[...,3]>0; print('size in',round(rgba.shape[1]/300,2),round(rgba.shape[0]/300,2),'ink',round(a.sum()/90000,1))
bg=Image.new('RGBA',(rgba.shape[1],rgba.shape[0]),(31,58,34,255)); bg.alpha_composite(Image.fromarray(rgba,'RGBA'))
bg.convert('RGB').resize((rgba.shape[1]//4,rgba.shape[0]//4),Image.LANCZOS).save('biffs_preview.png')
