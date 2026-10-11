#!/usr/bin/env python3
"""Generate Pikachu-style animated GIFs for Miso (yellow body, red cheeks, furrowed-brow angry)"""

from PIL import Image, ImageDraw, ImageFont
import os

CHAR_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'characters', 'miso')
os.makedirs(CHAR_DIR, exist_ok=True)

def draw_pika_frame(size=150, frame=0, state="idle", scale=1.0):
    """Draw Pikachu-style Miso: yellow body, red cheeks, pointy ears, furrowed brow when angry."""
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))  # transparent
    d = ImageDraw.Draw(img)

    x, y = size // 2, size // 2

    # Yellow body (oval)
    body_w, body_h = int(70 * scale), int(60 * scale)
    d.ellipse([x - body_w//2, y - body_h//2, x + body_w//2, y + body_h//2], fill=(255, 215, 0))

    # Pointy ears (black tips)
    ear_w, ear_h = int(18 * scale), int(35 * scale)
    # Left ear
    d.polygon([
        (x - body_w//2 - 4, y - body_h//2 + 5),
        (x - body_w//2 - 18, y - body_h//2 - ear_h//2),
        (x - body_w//2 - 4, y - body_h//2 + 15)
    ], fill=(255, 215, 0))
    # Black tip left
    d.polygon([
        (x - body_w//2 - 14, y - body_h//2 - 10),
        (x - body_w//2 - 18, y - body_h//2 - ear_h//2),
        (x - body_w//2 - 6, y - body_h//2 - 2)
    ], fill=(60, 60, 60))
    # Right ear
    d.polygon([
        (x + body_w//2 + 4, y - body_h//2 + 5),
        (x + body_w//2 + 18, y - body_h//2 - ear_h//2),
        (x + body_w//2 + 4, y - body_h//2 + 15)
    ], fill=(255, 215, 0))
    # Black tip right
    d.polygon([
        (x + body_w//2 + 14, y - body_h//2 - 10),
        (x + body_w//2 + 18, y - body_h//2 - ear_h//2),
        (x + body_w//2 + 6, y - body_h//2 - 2)
    ], fill=(60, 60, 60))

    # Red cheeks (small circles)
    cheek_r = int(8 * scale)
    d.ellipse([x - body_w//2 + 8, y - 5, x - body_w//2 + 8 + cheek_r*2, y - 5 + cheek_r*2], fill=(255, 50, 50))
    d.ellipse([x + body_w//2 - 8 - cheek_r*2, y - 5, x + body_w//2 - 8, y - 5 + cheek_r*2], fill=(255, 50, 50))

    # Eyes (small black ovals)
    eye_w, eye_h = int(8 * scale), int(10 * scale)
    d.ellipse([x - 14, y - 8, x - 6, y + 2], fill=(30, 30, 30))
    d.ellipse([x + 6, y - 8, x + 14, y + 2], fill=(30, 30, 30))

    # Mouth / expression based on state
    if state == "angry":
        # Furrowed brow: two downward lines above eyes
        d.line([x - 14, y - 18, x - 6, y - 14], fill=(60, 60, 60), width=3)
        d.line([x + 6, y - 18, x + 14, y - 14], fill=(60, 60, 60), width=3)
        # Small frown mouth
        d.arc([x - 16, y + 4, x + 16, y + 16], 0, 180, fill=(60, 60, 60), width=3)
    elif state == "dance" or state == "ooh":
        # Happy open mouth
        d.arc([x - 14, y + 2, x + 14, y + 14], 0, 180, fill=(60, 60, 60), width=3)
        # Small tongue dot
        d.ellipse([x - 4, y + 8, x + 4, y + 12], fill=(220, 100, 100))
    else:
        # Idle: gentle smile
        d.arc([x - 12, y + 2, x + 12, y + 12], 0, 180, fill=(60, 60, 60), width=2)

    # Small tail (lightning-shaped stub) on right
    tail_points = [
        (x + body_w//2 + 5, y),
        (x + body_w//2 + 20, y - 8),
        (x + body_w//2 + 15, y + 5),
        (x + body_w//2 + 25, y + 8),
        (x + body_w//2 + 10, y + 15)
    ]
    d.polygon(tail_points, fill=(255, 215, 0))
    d.polygon(tail_points, outline=(200, 160, 0), width=2)

    # Tiny breathing bob
    bob = int(3 * scale) if frame % 2 == 0 else 0
    img = img.crop((0, -2 + bob, size, size - 2 + bob))
    return img

# Generate GIFs
print("Generating Pikachu-style Miso animations...")

# Idle (breathing)
print("Creating idle.gif...")
idle_frames = [draw_pika_frame(150, i, "idle") for i in range(2)]
idle_frames[0].save(os.path.join(CHAR_DIR, "idle.gif"), save_all=True, append_images=idle_frames[1:], duration=250, loop=0, disposal=2)

# Dance (excited, open mouth, tongue)
print("Creating dance.gif...")
dance_frames = [draw_pika_frame(150, i, "dance") for i in range(3)]
dance_frames[0].save(os.path.join(CHAR_DIR, "dance.gif"), save_all=True, append_images=dance_frames[1:], duration=180, loop=0, disposal=2)

# Angry (furrowed brow, frown, red cheeks bright)
print("Creating angry.gif...")
angry_frames = [draw_pika_frame(150, i, "angry") for i in range(2)]
angry_frames[0].save(os.path.join(CHAR_DIR, "angry.gif"), save_all=True, append_images=angry_frames[1:], duration=200, loop=0, disposal=2)

print("All animations saved to:", CHAR_DIR)
