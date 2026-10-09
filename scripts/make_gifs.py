#!/usr/bin/env python3
"""Generate cute animated GIFs for the desktop companion (Miso the mushroom)"""
# These replace the placeholder filenames in the plan (idle.gif, dance.gif, angry.gif)

from PIL import Image, ImageDraw
import os

CHAR_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "characters", "miso")
os.makedirs(CHAR_DIR, exist_ok=True)

def draw_miso_frame(size, frame, state, scale=1.0):
    """Draw Miso (mushroom pet) one frame."""
    x, y = size // 2, size // 2
    stem_h = int(60 * scale)
    cap_w = int(90 * scale)
    cap_h = int(38 * scale)

    img = Image.new("RGB", (size, size), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # Stem
    stem_x = int(x - 28 * scale)
    stem_w = int(56 * scale)
    d.rectangle([stem_x, y, stem_x + stem_w, y + stem_h], fill=(255, 200, 180))

    # Cap (mushroom) - rounded
    cap_x = int(x - cap_w // 2)
    d.pieslice([cap_x - 15, y - cap_h, cap_x + cap_w + 15, y], 180, 360, fill=(255, 100, 100))
    d.pieslice([cap_x - 15, y - cap_h // 2, cap_x + cap_w + 15, y + 20], 0, 360, fill=(255, 100, 100))
    # Cap dots
    for dx in [-18, 0, 18]:
        d.ellipse([cap_x + dx - 6, y - cap_h + 8, cap_x + dx + 6, y - cap_h - 4], fill=(255, 180, 180))

    # Face on cap
    eye_x, eye_y = int(x - 24 * scale), int(y - 12 * scale)
    eye_size = int(9 * scale)
    eye_left = (eye_x - eye_size, eye_y, eye_x, eye_y + eye_size)
    eye_right = (eye_x + 9 * scale, eye_y, eye_x + 9 * scale + eye_size, eye_y + eye_size)
    d.ellipse(eye_left, fill=(40, 40, 40))
    d.ellipse(eye_right, fill=(40, 40, 40))

    # Mouth
    mouth_y = int(y - 2 * scale)
    if state == "smile":
        d.arc([int(x - 20 * scale), mouth_y - 10, int(x + 20 * scale), mouth_y + 5], 0, 180, fill=(40, 40, 40), width=4)
    elif state == "ooh":
        d.ellipse([int(x - 10 * scale), mouth_y - 10, int(x + 10 * scale), mouth_y + 10], fill=(40, 40, 40))
    elif state == "angry":
        d.line([int(x - 20 * scale), mouth_y + 8, int(x + 20 * scale), mouth_y - 2], fill=(40, 40, 40), width=4)

    # Eyebrows for angry
    if state == "angry":
        d.line([int(x - 26 * scale), int(y - 28 * scale), int(x - 12 * scale), int(y - 18 * scale)], fill=(40, 40, 40), width=4)
        d.line([int(x + 26 * scale), int(y - 28 * scale), int(x + 12 * scale), int(y - 18 * scale)], fill=(40, 40, 40), width=4)

    # Breathing bob offset
    bob = int(3 * scale) if frame % 30 == 0 else 0

    img = img.crop((0, -3 + bob, size, size - 3 + bob))
    return img

# Idle (breathing)
print("Generating idle.gif...")
idle_frames = []
for i in range(2):
    idle_frames.append(draw_miso_frame(150, i, "smile"))
idle_frames[0].save(os.path.join(CHAR_DIR, "idle.gif"), save_all=True, append_images=idle_frames[1:], duration=200, loop=0)

# Dance (excited)
print("Generating dance.gif...")
dance_frames = []
for i in range(3):
    dance_frames.append(draw_miso_frame(150, i, "ooh", scale=1.05))
dance_frames[0].save(os.path.join(CHAR_DIR, "dance.gif"), save_all=True, append_images=dance_frames[1:], duration=150, loop=0)

# Angry (yelling)
print("Generating angry.gif...")
angry_frames = []
for i in range(2):
    angry_frames.append(draw_miso_frame(150, i, "angry", scale=1.0))
angry_frames[0].save(os.path.join(CHAR_DIR, "angry.gif"), save_all=True, append_images=angry_frames[1:], duration=150, loop=0)

print("All animations generated successfully!")