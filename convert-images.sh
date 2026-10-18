#!/bin/bash

# Convert PNG product images to JPG with cream background (#FAF8F3)
# Target directory: public/images/

SOURCE_DIR="tmp_product_images"
TARGET_DIR="public/images"
BACKGROUND="#FAF8F3"  # warm-white/cream color

echo "Converting product images with cream background..."

# Hat images
convert "$SOURCE_DIR/hats/hats/nostalgic_Hammond_hat_black_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/hat-black.jpg"
convert "$SOURCE_DIR/hats/hats/nostalgic_Hammond_hat_green_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/hat-forest.jpg"
convert "$SOURCE_DIR/hats/hats/nostalgic_Hammond_hat_khaki_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/hat-khaki.jpg"

# Tee images
convert "$SOURCE_DIR/tops/tops/cave_tangi_tee_white_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/tee-white.jpg"
convert "$SOURCE_DIR/tops/tops/cave_tangi_tee_black_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/tee-black.jpg"
convert "$SOURCE_DIR/tops/tops/cave_tangi_tee_cream_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/tee-cream.jpg"

# Ringer tee
convert "$SOURCE_DIR/tops/tops/nostalgic_Hammond_pe_tee_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/ringer-tee.jpg"

# Sweatshirt
convert "$SOURCE_DIR/tops/tops/tornadoes_crewneck_white_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/sweatshirt.jpg"

# Posters - using the individual folder versions
convert "$SOURCE_DIR/individual/greetings-8x10.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/poster-greetings-8x10.jpg"
convert "$SOURCE_DIR/individual/greetings-11x14.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/poster-greetings-11x14.jpg"

# Check for 16x20 poster
if [ -f "$SOURCE_DIR/individual/greetings-16x20.png" ]; then
    convert "$SOURCE_DIR/individual/greetings-16x20.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/poster-greetings-16x20.jpg"
elif [ -f "$SOURCE_DIR/artwork/artwork/greetings_poster_16x20_01_main.png" ]; then
    convert "$SOURCE_DIR/artwork/artwork/greetings_poster_16x20_01_main.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/poster-greetings-16x20.jpg"
fi

# Stadium poster
convert "$SOURCE_DIR/individual/stadium.png" -background "$BACKGROUND" -flatten "$TARGET_DIR/poster-stadium.jpg"

echo "✅ Image conversion complete!"
