import math, sys
from PIL import Image, ImageDraw, ImageFont
FD='/tmp/claude-0/-home-claude/2883d029-23a6-5e8e-ac19-37b93b8bd372/scratchpad/fonts/'
INK=(31,42,74,255)  # navy
STROKE=11
W,H=3600,2100
def arched(text, font, radius, letter_spacing, ink):
    # measure advances
    adv=[font.getlength(ch) for ch in text]
    total=sum(adv)+letter_spacing*(len(text)-1)
    theta_total=total/radius
    size=int(radius*2+400)
    canvas=Image.new('RGBA',(W,H),(0,0,0,0))
    cx=W/2; cy=radius+260   # circle centre below the text
    a=-theta_total/2
    for ch,ad in zip(text,adv):
        mid=a+(ad/2)/radius
        # glyph image
        bbox=font.getbbox(ch)
        gw,gh=int(ad)+40,int(font.size*1.4)
        g=Image.new('RGBA',(gw,gh),(0,0,0,0))
        ImageDraw.Draw(g).text((20,0),ch,font=font,fill=ink,stroke_width=STROKE,stroke_fill=ink)
        g=g.rotate(-math.degrees(mid),resample=Image.BICUBIC,expand=True)
        x=cx+radius*math.sin(mid); y=cy-radius*math.cos(mid)
        canvas.alpha_composite(g,(int(x-g.width/2),int(y-g.height/2)))
        a+=(ad+letter_spacing)/radius
    return canvas
big=ImageFont.truetype(FD+'Graduate-Regular.ttf',430)
img=arched('HATTIESBURG',big,radius=4300,letter_spacing=26,ink=INK)
d=ImageDraw.Draw(img)
# crop check of arch bottom to place plate
bb=img.getbbox(); print('arch bbox',bb)
top_plate=bb[3]+70
pw,ph=1500,215; x0=(W-pw)//2; y0=top_plate; st=24
# ribbon tails (behind the plate): small folded banners at each end
tail=120; drop=62
for side in (-1,1):
    if side<0:
        xa=x0-tail; xb=x0+40
        poly=[(xa,y0+drop),(xb,y0+drop),(xb,y0+ph*0.8+drop),(xa,y0+ph*0.8+drop),(xa+48,y0+ph*0.4+drop)]
    else:
        xa=x0+pw-40; xb=x0+pw+tail
        poly=[(xa,y0+drop),(xb,y0+drop),(xb-48,y0+ph*0.4+drop),(xb,y0+ph*0.8+drop),(xa,y0+ph*0.8+drop)]
    d.polygon(poly,fill=INK)
# plate: knock out interior so it reads as an outlined plate over the tails
d.rectangle([x0,y0,x0+pw,y0+ph],fill=INK)
d.rectangle([x0+st,y0+st,x0+pw-st,y0+ph-st],fill=(0,0,0,0))
# small fold triangles linking plate to tails
small=ImageFont.truetype(FD+'Oswald[wght].ttf',240)
try: small.set_variation_by_name('SemiBold')
except Exception as e: print('var',e)
txt='PHYSICAL ED.'
# letterspaced
ls=14; widths=[small.getlength(c) for c in txt]; tw=sum(widths)+ls*(len(txt)-1)
x=(W-tw)/2; y=y0+ph+20
for c,wc in zip(txt,widths):
    d.text((x,y),c,font=small,fill=INK); x+=wc+ls
bb=img.getbbox(); print('final bbox',bb)
img=img.crop((bb[0]-40,bb[1]-40,bb[2]+40,bb[3]+40))
img.save(sys.argv[1],dpi=(300,300)); print(img.size)
prev=Image.new('RGB',img.size,(246,239,214)); prev.paste(img,(0,0),img); prev.thumbnail((900,900)); prev.save(sys.argv[2])
