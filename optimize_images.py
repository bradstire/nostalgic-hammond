from PIL import Image
import os

images_dir = "public/images"

# Images to process
images_to_process = [
    ("sweatshirt-temp.png", "sweatshirt.jpg"),
    ("hat-black-temp.png", "hat-black.jpg"),
    ("hat-forest-temp.png", "hat-forest.jpg"),
    ("hat-khaki-temp.png", "hat-khaki.jpg"),
    ("ringer-tee-temp.png", "ringer-tee.jpg"),
]

for source, dest in images_to_process:
    source_path = os.path.join(images_dir, source)
    dest_path = os.path.join(images_dir, dest)
    
    if os.path.exists(source_path):
        img = Image.open(source_path)
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg
        
        # Resize to max width 800px, maintaining aspect ratio
        if img.width > 800:
            ratio = 800 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((800, new_height), Image.Resampling.LANCZOS)
        
        # Save as optimized JPEG
        img.save(dest_path, "JPEG", quality=85, optimize=True)
        print(f"✓ {dest}")
        
        # Remove temp file
        os.remove(source_path)
    else:
        print(f"✗ {source} not found")

print("\nDone optimizing images!")
