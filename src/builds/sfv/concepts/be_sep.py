import numpy as np, cv2, sys
sys.path.insert(0,'/home/claude/print-assets/src/builds/sfv'); sys.path.insert(0,'/home/claude/print-assets/src/newsprint')
from w2lib import print_clean
from PIL import Image
im=cv2.imread('be_x4.png'); H,W=im.shape[:2]
lab=cv2.cvtColor(cv2.GaussianBlur(im,(0,0),1.0),cv2.COLOR_BGR2LAB).astype(np.float32)
P=np.array([[224,131,143],[131,106,114],[40,131,133],[193,130,141]],np.float32)  # cream, teal, dark, cream2
d=((lab[:,:,None,:]-P[None,None])**2).sum(-1); cls=np.argmin(d,2)
cream=(cls==0)|(cls==3); dark=(cls==2)
# paper/scan border: keep inside the printed field
cream[:, :24]=False; cream[:, W-24:]=False; cream[:24]=False; cream[H-24:]=False
dark[:, :24]=False; dark[:, W-24:]=False; dark[:24]=False; dark[H-24:]=False
# drop the product copy (GALVANIZED / SPRINKLER / SYSTEMS): cream components inside its box
x0,y0,x1,y1=850,930,1460,1490
n,lab_,st,_=cv2.connectedComponentsWithStats(cream.astype(np.uint8))
for j in range(1,n):
    x,y,w,h,a=st[j]
    if x>=x0 and y>=y0 and x+w<=x1 and y+h<=y1: cream[lab_==j]=False
n,lab_,st,_=cv2.connectedComponentsWithStats(dark.astype(np.uint8))
for j in range(1,n):
    x,y,w,h,a=st[j]
    if x>=x0 and y>=y0 and x+w<=x1 and y+h<=y1: dark[lab_==j]=False
for nme,m in (('cream',cream),('dark',dark)):
    m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))>0
    cv2.imwrite(f'sep_{nme}.png',m.astype(np.uint8)*255)
vis=np.zeros_like(im); vis[:]=(145,134,39)
vis[cv2.imread('sep_cream.png',0)>0]=(191,216,236); vis[cv2.imread('sep_dark.png',0)>0]=(32,37,46)
cv2.imwrite('sep_vis.png',cv2.resize(vis,None,fx=0.3,fy=0.3,interpolation=cv2.INTER_AREA))
