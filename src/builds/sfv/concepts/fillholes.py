import numpy as np, cv2
def fill_small_holes(layers, ppi, max_in=0.03):
    """layers: dict name->bool mask (same shape). Fill garment holes smaller than max_in x max_in
    (enclosed by ink) with the layer that touches them most (nearest-layer by distance)."""
    names=list(layers); U=np.zeros_like(layers[names[0]])
    for n in names: U|=layers[n]
    inv=(~U).astype(np.uint8)
    n,lab,st,_=cv2.connectedComponentsWithStats(inv,connectivity=4)
    amax=(max_in*ppi)**2
    small=np.zeros_like(U)
    for j in range(1,n):
        x,y,w,h,a=st[j]
        if a<=amax and x>0 and y>0 and x+w<U.shape[1] and y+h<U.shape[0]: small[lab==j]=True
    # nearest layer
    dists=[cv2.distanceTransform((~layers[nm]).astype(np.uint8),cv2.DIST_L2,3) for nm in names]
    best=np.argmin(np.stack(dists,0),0)
    out={nm:layers[nm].copy() for nm in names}
    for i,nm in enumerate(names): out[nm]|= small&(best==i)
    return out, int(small.sum())
