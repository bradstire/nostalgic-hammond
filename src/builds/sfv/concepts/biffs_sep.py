import numpy as np, cv2, sys, json
im=cv2.imread('biffs_x4.png')
H,W=im.shape[:2]
x0,x1,y0,y1=64,3268,0,3400
im=im[y0:y1,x0:x1]
lab=cv2.cvtColor(cv2.GaussianBlur(im,(0,0),0.8),cv2.COLOR_BGR2LAB).astype(np.float32)
pal={'green':(53,112,142),'cream':(235,127,137),'yellow':(227,123,202),'red':(104,169,165),'dark':(25,136,137)}
names=list(pal); P=np.array([pal[n] for n in names],np.float32)
d=((lab[:,:,None,:]-P[None,None,:,:])**2).sum(-1)
cls=np.argmin(d,axis=2)
out={}
for i,n in enumerate(names): out[n]=(cls==i)
# remove the collection credit (x4 coords of the crop)
cx0,cy0=2040-x0,3260; out['cream'][cy0:cy0+80, cx0-20:cx0+760]=False
for n in ('cream','yellow','red'):
    m=out[n].astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    cv2.imwrite(f'sep_{n}.png',m*255)
    print(n, m.mean().round(3))
vis=np.zeros_like(im); vis[:]=(30,56,29)
for n,c in (('cream',(214,231,237)),('yellow',(72,223,250)),('red',(36,63,163))):
    vis[cv2.imread(f'sep_{n}.png',0)>0]=c
cv2.imwrite('sep_vis.png',cv2.resize(vis,None,fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA))
