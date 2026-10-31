import numpy as np, cv2, sys, json
sys.path.insert(0,'/home/claude/print-assets/src/builds/sfv'); sys.path.insert(0,'/home/claude/print-assets/src/newsprint')
from w2lib import print_clean, T, move
import vtype
from PIL import Image
from shapely import affinity
cream=cv2.imread('sep_cream.png',0)>0; dark=cv2.imread('sep_dark.png',0)>0
H,W=cream.shape
# printer's date code in the BUILDERS box (P1-1 / 8-17-61): not part of the logo
for m in (dark,):
    n,l,st,_=cv2.connectedComponentsWithStats(m.astype(np.uint8))
    for j in range(1,n):
        x,y,w,h,a=st[j]
        if x>=140 and y>=160 and x+w<=275 and y+h<=300: m[l==j]=False
# split: logo block (oval + tagline) above y_split, mascot below
y_split=820
allm=cream|dark
ys,xs=np.where(allm[:y_split]); lx0,lx1=xs.min(),xs.max()
ys2,xs2=np.where(allm[y_split:]); mx0,mx1=xs2.min(),xs2.max()
shift=int(round(((lx0+lx1)/2)-((mx0+mx1)/2)))
print('logo centre',(lx0+lx1)/2,'mascot centre',(mx0+mx1)/2,'shift',shift)
def sh(m):
    o=m.copy(); low=np.zeros_like(m[y_split:]); 
    if shift>0: low[:,shift:]=m[y_split:,:-shift]
    elif shift<0: low[:,:shift]=m[y_split:,-shift:]
    else: low=m[y_split:]
    o[y_split:]=low; return o
cream=sh(cream); dark=sh(dark)
allm=cream|dark; ys,xs=np.where(allm); bx0,bx1,by0,by1=xs.min(),xs.max(),ys.min(),ys.max()
PRINT_H=12.2
ppi=(by1-by0)/PRINT_H
sys.path.insert(0,'/home/claude/sfvqa'); from fillholes import fill_small_holes
lay,nf=fill_small_holes({'cream':cream[by0:by1+1,bx0:bx1+1],'dark':dark[by0:by1+1,bx0:bx1+1]}, ppi, 0.035); print('filled px',nf)
out={}
for nme in ('cream','dark'):
    m=lay[nme]; c=print_clean(m, ppi)
    W3=int(round(c.shape[1]*300/ppi)); H3=int(round(c.shape[0]*300/ppi))
    out[nme]=cv2.resize(c.astype(np.float32),(W3,H3),interpolation=cv2.INTER_AREA)>0.5
H3,W3=out['cream'].shape
# house line under the mascot (R21 rule 4)
hl,_=T('SEPULVEDA BLVD.  ·  VAN NUYS','Jost[wght].ttf',cap=78,var=[600],track=0.16)
hb=hl.bounds; hw=hb[2]-hb[0]
gap=110; pad=30
Wt=max(W3,int(hw)+2)+2*pad; Ht=H3+gap+int(hb[3]-hb[1])+2*pad+4
rgba=np.zeros((Ht,Wt,4),np.uint8)
ox=(Wt-W3)//2
cols={'cream':(0xF4,0xEC,0xDD),'dark':(0x2A,0x22,0x1D)}
for nme in ('cream','dark'):
    m=np.zeros((Ht,Wt),bool); m[pad:pad+H3,ox:ox+W3]=out[nme]; rgba[m,:3]=cols[nme]; rgba[m,3]=255
hl=move(hl,cx=Wt/2,y=pad+H3+gap)
hm=np.array(vtype.raster([(hl,'#F4ECDD')],Wt,Ht))[...,3]>0
rgba[hm,:3]=cols['cream']; rgba[hm,3]=255
Image.fromarray(rgba,'RGBA').save('sfv_builders_emporium_concept.png',dpi=(300,300))
a=rgba[...,3]>0; print('size in',round(Wt/300,2),round(Ht/300,2),'ink',round(a.sum()/90000,1))
bg=Image.new('RGBA',(Wt,Ht),(39,128,140,255)); bg.alpha_composite(Image.fromarray(rgba,'RGBA'))
bg.convert('RGB').resize((Wt//4,Ht//4),Image.LANCZOS).save('be_preview.png')
json.dump({'shift_px_x4':shift,'y_split_x4':y_split,'ppi_src':ppi},open('be_meta.json','w'))
