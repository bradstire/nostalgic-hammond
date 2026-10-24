"""Magnolia Inn sign + locator line (differentiation rule: full name + business type + Hammond).
'1111 W. THOMAS ST. · HAMMOND, LA.' in the sign's black ink, League Spartan Bold tracked, 0.24 in caps, centred under the posts."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W="/home/claude/nh-recovered/print-assets-repo/hammond/wave2"; S="/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad"
DPI=300; INK=(28,27,26,255)
sign=Image.open(f"{W}/magnolia_sign.png").convert("RGBA"); a=np.asarray(sign)
ys,xs=np.where(a[...,3]>0); sign=sign.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
txt="1111 W. THOMAS ST.  ·  HAMMOND, LA."
cap=int(0.24*DPI); f=ImageFont.truetype(f"{S}/fonts/LeagueSpartan[wght].ttf", 400); f.set_variation_by_axes([700])
# render big then scale to cap height
tr=0.12; tmp=Image.new("L",(9000,800),0); d=ImageDraw.Draw(tmp); x=40
for ch in txt:
    d.text((x,600),ch,font=f,fill=255,anchor="ls"); x+=f.getlength(ch)+tr*400
m=np.asarray(tmp)>127; yy,xx=np.where(m); m=m[yy.min():yy.max()+1, xx.min():xx.max()+1]
capH=f.getbbox("H",anchor="ls"); capH=-capH[1]
s=cap/capH; line=Image.fromarray((m*255).astype(np.uint8)).resize((int(m.shape[1]*s),int(m.shape[0]*s)),Image.LANCZOS)
la=(np.asarray(line)>127)
if la.shape[1] > 5.6*DPI: 
    s2=5.6*DPI/la.shape[1]; line=line.resize((int(line.width*s2),int(line.height*s2)),Image.LANCZOS); la=np.asarray(line)>127
gap=int(0.22*DPI); H=sign.height+gap+la.shape[0]; out=Image.new("RGBA",(sign.width,H),(0,0,0,0)); out.alpha_composite(sign,(0,0))
L=np.zeros((la.shape[0],la.shape[1],4),np.uint8); L[la]=INK; out.alpha_composite(Image.fromarray(L,"RGBA"),((sign.width-la.shape[1])//2, sign.height+gap))
# binary alpha
o=np.asarray(out).copy(); o[...,3]=np.where(o[...,3]>127,255,0); out=Image.fromarray(o,"RGBA")
out.save(f"{W}/magnolia_sign_hammond.png",dpi=(DPI,DPI)); print(out.size, round(out.width/DPI,2), round(out.height/DPI,2), 'line w in', round(la.shape[1]/DPI,2))
bg=Image.new("RGBA",out.size,(250,250,248,255)); bg.alpha_composite(out); bg.convert("RGB").resize((out.width//5,out.height//5)).save(f"{S}/hm2/magnolia_view.png")
