#!/bin/bash

# Image optimization script for Nostalgic Hammond
# Resize to max 800px width, compress to under 300KB while preserving transparency

TARGET_DIR="public/images"
BACKUP_DIR="public/images/originals"
MAX_WIDTH=800
TARGET_SIZE_KB=300

echo "🖼️  Starting image optimization..."
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Count images
TOTAL=$(ls -1 "$TARGET_DIR"/*.png 2>/dev/null | wc -l)
CURRENT=0

if [ $TOTAL -eq 0 ]; then
    echo "❌ No PNG images found in $TARGET_DIR"
    exit 1
fi

echo "📊 Found $TOTAL PNG images to optimize"
echo ""

# Process each PNG
for img in "$TARGET_DIR"/*.png; do
    CURRENT=$((CURRENT + 1))
    filename=$(basename "$img")
    
    # Skip if already in backup directory
    if [[ "$img" == *"/originals/"* ]]; then
        continue
    fi
    
    # Get original size
    ORIGINAL_SIZE=$(du -k "$img" | cut -f1)
    ORIGINAL_SIZE_MB=$(echo "scale=2; $ORIGINAL_SIZE / 1024" | bc)
    
    printf "[%2d/%2d] %s (%.2f MB) ... " "$CURRENT" "$TOTAL" "$filename" "$ORIGINAL_SIZE_MB"
    
    # Backup original
    if [ ! -f "$BACKUP_DIR/$filename" ]; then
        cp "$img" "$BACKUP_DIR/$filename"
    fi
    
    # Create temp file
    TEMP_FILE="${img}.tmp.png"
    
    # Step 1: Resize to max width 800px (preserve aspect ratio)
    convert "$img" -resize "${MAX_WIDTH}x>" -strip "$TEMP_FILE"
    
    # Step 2: Compress with pngquant (quality 80-95, preserve transparency)
    pngquant --quality=80-95 --speed=1 --force --output "$TEMP_FILE.quant" "$TEMP_FILE" 2>/dev/null
    
    if [ -f "$TEMP_FILE.quant" ]; then
        mv "$TEMP_FILE.quant" "$TEMP_FILE"
    fi
    
    # Step 3: Further optimize with optipng (lossless)
    optipng -quiet -o2 "$TEMP_FILE" 2>/dev/null
    
    # Get new size
    NEW_SIZE=$(du -k "$TEMP_FILE" | cut -f1)
    NEW_SIZE_MB=$(echo "scale=2; $NEW_SIZE / 1024" | bc)
    SAVINGS=$(echo "scale=1; ($ORIGINAL_SIZE - $NEW_SIZE) * 100 / $ORIGINAL_SIZE" | bc)
    
    # Replace original
    mv "$TEMP_FILE" "$img"
    
    printf "%.2f MB (-%s%%)\n" "$NEW_SIZE_MB" "$SAVINGS"
done

echo ""
echo "✅ Optimization complete!"
echo ""

# Summary
ORIGINAL_TOTAL=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
NEW_TOTAL=$(du -sh "$TARGET_DIR" --exclude=originals 2>/dev/null | cut -f1)

echo "📊 Summary:"
echo "   Original: $ORIGINAL_TOTAL"
echo "   Optimized: $NEW_TOTAL"
echo ""
echo "💾 Originals backed up to: $BACKUP_DIR"
