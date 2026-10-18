from PIL import Image, ImageDraw, ImageFont
import os

out = "public/images"
os.makedirs(out, exist_ok=True)

def product_img(name, bg, text_col, label, size=(800, 800)):
    img = Image.new('RGB', size, bg)
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        sf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        f = sf = ImageFont.load_default()
    
    bb = d.textbbox((0,0), label, font=f)
    d.text(((size[0]-(bb[2]-bb[0]))//2, (size[1]-(bb[3]-bb[1]))//2), label, fill=text_col, font=f)
    
    wm = "NOSTALGIC HAMMOND"
    bb2 = d.textbbox((0,0), wm, font=sf)
    wm_col = "#555555" if bg in ['#1A1A1A','#2D4A2D','#6B6B6B'] else "#BBBBBB"
    d.text(((size[0]-(bb2[2]-bb2[0]))//2, size[1]-50), wm, fill=wm_col, font=sf)
    
    img.save(f"{out}/{name}", "JPEG", quality=90)

def framed_img(name, size=(800, 800)):
    img = Image.new('RGB', size, '#2A2A2A')
    d = ImageDraw.Draw(img)
    d.rectangle([50, 50, 750, 750], fill='#F5F0E6')
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        sf = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        f = sf = ImageFont.load_default()
    
    bb = d.textbbox((0,0), "FRAMED PRINT", font=f)
    d.text(((800-(bb[2]-bb[0]))//2, (800-(bb[3]-bb[1]))//2), "FRAMED PRINT", fill='#8B7D6B', font=f)
    
    wm = "NOSTALGIC HAMMOND"
    bb2 = d.textbbox((0,0), wm, font=sf)
    d.text(((800-(bb2[2]-bb2[0]))//2, 700), wm, fill='#BBAA99', font=sf)
    
    img.save(f"{out}/{name}", "JPEG", quality=90)

# Generate all product images
product_img("tee-white.jpg", "#E8E8E8", "#333333", "T-SHIRT")
product_img("tee-cream.jpg", "#F5F0E6", "#555555", "T-SHIRT")
product_img("tee-black.jpg", "#1A1A1A", "#FFFFFF", "T-SHIRT")
product_img("hat-black.jpg", "#1A1A1A", "#FFFFFF", "DAD HAT")
product_img("hat-forest.jpg", "#2D4A2D", "#FFFFFF", "DAD HAT")
product_img("hat-khaki.jpg", "#C4B59D", "#333333", "DAD HAT")
product_img("ringer-tee.jpg", "#F5F0E6", "#555555", "RINGER TEE")
product_img("sweatshirt.jpg", "#6B6B6B", "#FFFFFF", "CREW NECK")
framed_img("poster-framed.jpg")

print("✅ Generated 9 product images in public/images/")
