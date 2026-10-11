#!/usr/bin/env python3
"""Generate detailed 300px GIFs with 6-8 frames each"""
from PIL import Image, ImageDraw
import os

CHAR_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'characters', 'miso')
os.makedirs(CHAR_DIR, exist_ok=True)

def draw_pika_advanced(size=300, frame_idx=0, state="idle", total_frames=8):
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    t = frame_idx / max(1, total_frames - 1)

    # Body
    body_w, body_h = 110, 100
    d.ellipse([cx - body_w//2 - 3, cy - body_h//2 - 3,
               cx + body_w//2 + 3, cy + body_h//2 + 3],
              fill=(255, 200, 50), outline=(220, 150, 30), width=4)
    d.ellipse([cx - body_w//2 + 5, cy - body_h//2 + 8,
               cx + body_w//2 - 5, cy + body_h//2 - 5],
              fill=(255, 230, 100))

    # Ears
    d.polygon([(cx - 55, cy - 30), (cx - 75, cy - 90), (cx - 45, cy - 25)], fill=(255, 215, 0), outline=(200, 160, 20), width=3)
    d.polygon([(cx - 60, cy - 70), (cx - 75, cy - 95), (cx - 50, cy - 60)], fill=(30, 30, 30))
    d.polygon([(cx - 55, cy - 50), (cx - 68, cy - 80), (cx - 48, cy - 55)], fill=(180, 130, 40))
    d.polygon([(cx + 55, cy - 30), (cx + 75, cy - 90), (cx + 45, cy - 25)], fill=(255, 215, 0), outline=(200, 160, 20), width=3)
    d.polygon([(cx + 60, cy - 70), (cx + 75, cy - 95), (cx + 50, cy - 60)], fill=(30, 30, 30))
    d.polygon([(cx + 55, cy - 50), (cx + 68, cy - 80), (cx + 48, cy - 55)], fill=(180, 130, 40))

    # Red cheeks (big, bright)
    d.ellipse([cx - 55, cy + 15, cx - 35, cy + 35], fill=(255, 30, 30), outline=(220, 10, 10), width=3)
    d.ellipse([cx - 48, cy + 18, cx - 40, cy + 26], fill=(255, 80, 80))
    d.ellipse([cx + 35, cy + 15, cx + 55, cy + 35], fill=(255, 30, 30), outline=(220, 10, 10), width=3)
    d.ellipse([cx + 40, cy + 18, cx + 48, cy + 26], fill=(255, 80, 80))

    # Eyes
    if state == "angry":
        d.line([(cx - 35, cy - 10), (cx - 15, cy + 5)], fill=(20, 20, 20), width=6)
        d.line([(cx + 15, cy - 10), (cx + 35, cy + 5)], fill=(20, 20, 20), width=6)
        d.line([(cx - 45, cy - 18), (cx - 25, cy - 2)], fill=(255, 30, 30), width=3)
        d.line([(cx + 45, cy - 18), (cx + 25, cy - 2)], fill=(255, 30, 30), width=3)
        d.ellipse([(cx - 28, cy + 2), (cx - 18, cy + 10)], fill=(20, 20, 20))
        d.ellipse([(cx + 18, cy + 2), (cx + 28, cy + 10)], fill=(20, 20, 20))
    elif state == "dance":
        d.ellipse([(cx - 35, cy - 15), (cx - 15, cy + 5)], fill=(255, 255, 255), outline=(30, 30, 30), width=4)
        d.ellipse([(cx + 15, cy - 15), (cx + 35, cy + 5)], fill=(255, 255, 255), outline=(30, 30, 30), width=4)
        d.ellipse([(cx - 25, cy - 5), (cx - 15, cy + 2)], fill=(25, 25, 25))
        d.ellipse([(cx + 15, cy - 5), (cx + 25, cy + 2)], fill=(25, 25, 25))
        d.ellipse([(cx - 45, cy - 20), (cx - 40, cy - 15)], fill=(255, 255, 200))
        d.ellipse([(cx + 40, cy - 20), (cx + 45, cy - 15)], fill=(255, 255, 200))
    else:
        d.ellipse([(cx - 30, cy - 10), (cx - 12, cy + 8)], fill=(30, 30, 30), outline=(20, 20, 20), width=2)
        d.ellipse([(cx + 12, cy - 10), (cx + 30, cy + 8)], fill=(30, 30, 30), outline=(20, 20, 20), width=2)
        d.ellipse([(cx - 24, cy - 2), (cx - 18, cy + 2)], fill=(255, 255, 255))
        d.ellipse([(cx + 18, cy - 2), (cx + 24, cy + 2)], fill=(255, 255, 255))

    # Mouth
    if state == "angry":
        d.arc([(cx - 30, cy + 15), (cx + 30, cy + 45)], 20, 160, fill=(30, 30, 30), width=6)
        d.line([(cx - 15, cy + 30), (cx - 5, cy + 35)], fill=(30, 30, 30), width=3)
        d.line([(cx + 15, cy + 30), (cx + 5, cy + 35)], fill=(30, 30, 30), width=3)
    elif state == "dance":
        d.arc([(cx - 30, cy + 10), (cx + 30, cy + 45)], 0, 180, fill=(30, 10, 10), width=5)
        d.ellipse([(cx - 12, cy + 28), (cx + 12, cy + 42)], fill=(255, 100, 150))
        d.arc([(cx - 20, cy + 15), (cx - 5, cy + 25)], 180, 360, fill=(240, 240, 240), width=2)
        d.arc([(cx + 5, cy + 15), (cx + 20, cy + 25)], 180, 360, fill=(240, 240, 240), width=2)
    else:
        d.arc([(cx - 18, cy + 15), (cx + 18, cy + 30)], 0, 180, fill=(30, 30, 30), width=4)
        d.ellipse([(cx - 3, cy + 28), (cx + 5, cy + 32)], fill=(255, 100, 100))

    # Tail
    tail_pts = [(cx + 60, cy + 20), (cx + 100, cy - 10), (cx + 85, cy + 25), (cx + 110, cy + 35), (cx + 70, cy + 30)]
    d.polygon(tail_pts, fill=(255, 215, 0), outline=(200, 160, 20), width=4)
    d.polygon([(cx + 75, cy + 15), (cx + 95, cy - 2), (cx + 80, cy + 20)], fill=(255, 180, 30))

    # Body outline for depth
    d.ellipse([cx - body_w//2 - 2, cy - body_h//2 - 2,
               cx + body_w//2 + 2, cy + body_h//2 + 2],
              outline=(200, 140, 20), width=1)

    # Movement
    bob = 0
    tilt = 0
    if state == "idle":
        bob = int(10 * (1 - abs(2 * t - 1)))
    elif state == "dance":
        bob = int(15 * (1 - abs(2 * t - 1)))
        tilt = int(5 * (t * 2 - 1))
    else:
        bob = 0
        tilt = int(3 * (t * 2 - 1))

    crop_top = max(0, -bob - tilt)
    crop_bottom = size - bob - tilt
    img = img.crop((0, crop_top, size, crop_bottom))
    if img.size != (size, size):
        new_img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        offset_x = (size - img.width) // 2
        offset_y = (size - img.height) // 2 if img.height < size else 0
        new_img.paste(img, (offset_x, offset_y))
        img = new_img
    return img

# IDLE: 8 frames
print("Creating improved 300px GIFs...")
frames = [draw_pika_advanced(300, i, "idle", 8) for i in range(8)]
frames[0].save(os.path.join(CHAR_DIR, "idle.gif"), save_all=True, append_images=frames[1:], duration=120, loop=0, disposal=2)
print("idle.gif: 8 frames, 300px, breathing bob, gentle smile")

frames = [draw_pika_advanced(300, i, "dance", 6) for i in range(6)]
frames[0].save(os.path.join(CHAR_DIR, "dance.gif"), save_all=True, append_images=frames[1:], duration=150, loop=0, disposal=2)
print("dance.gif: 6 frames, 300px, open mouth + tongue, big happy eyes")

frames = [draw_pika_advanced(300, i, "angry", 8) for i in range(8)]
frames[0].save(os.path.join(CHAR_DIR, "angry.gif"), save_all=True, append_images=frames[1:], duration=180, loop=0, disposal=2)
print("angry.gif: 8 frames, 300px, furrowed brows, frown, NO bob, red marks")
