"""Shared constants, easing helpers, and drawing primitives for the
'Dog & Cat: Funny Fights' procedurally-animated cartoon.

Everything drawn here is original vector-style artwork built from basic
shapes (ellipses, polygons, lines) -- no external images or footage.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
FPS = 24
FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
TITLE_FONT_PATH = f"{FONT_DIR}/BigShoulders-Bold.ttf"
BODY_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Palette
SKY = (255, 226, 176)
WALL = (250, 214, 165)
WALL_TRIM = (223, 175, 116)
FLOOR = (223, 176, 120)
RUG = (233, 122, 97)
RUG_DARK = (201, 92, 68)
COUCH = (94, 129, 138)
COUCH_DARK = (70, 100, 108)
TABLE = (120, 82, 57)
POT = (176, 90, 60)
PLANT = (73, 138, 84)
WINDOW_SKY = (168, 216, 231)
DOG_FUR = (233, 175, 92)
DOG_FUR_DARK = (205, 140, 62)
DOG_EAR = (196, 120, 55)
CAT_FUR = (130, 137, 150)
CAT_FUR_DARK = (98, 105, 120)
CAT_STRIPE = (80, 87, 102)
TOY_RED = (219, 78, 78)
WHITE = (255, 255, 255)
BLACK = (30, 26, 24)
INK = (40, 34, 30)


def lerp(a, b, t):
    return a + (b - a) * t


def clamp01(t):
    return max(0.0, min(1.0, t))


def ease_out_back(t, overshoot=1.7):
    t = clamp01(t)
    t -= 1
    return 1 + (overshoot + 1) * t ** 3 + overshoot * t ** 2


def ease_in_out(t):
    t = clamp01(t)
    return 3 * t ** 2 - 2 * t ** 3


def ease_out_bounce(t):
    t = clamp01(t)
    n1, d1 = 7.5625, 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def scene_t(t, start, end):
    """Normalized local time within [start, end], clamped to [0, 1]."""
    if end <= start:
        return 0.0
    return clamp01((t - start) / (end - start))


def draw_taper(draw, x0, y0, x1, y1, r0, r1, color, steps=10):
    """Smooth tapered capsule (used for floppy ears / tails) made from a
    chain of overlapping circles -- avoids sharp polygon corners."""
    for i in range(steps + 1):
        t = i / steps
        x = lerp(x0, x1, t)
        y = lerp(y0, y1, t)
        r = lerp(r0, r1, t)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)


def ellipse_safe(draw, x0, y0, x1, y1, **kw):
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    draw.ellipse([x0, y0, x1, y1], **kw)


def new_canvas():
    img = Image.new("RGB", (WIDTH, HEIGHT), SKY)
    return img, ImageDraw.Draw(img, "RGBA")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_center(draw, cx, cy, text, f, fill, stroke_fill=None, stroke_width=0):
    bbox = draw.textbbox((0, 0), text, font=f, stroke_width=stroke_width)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = cx - w / 2 - bbox[0]
    y = cy - h / 2 - bbox[1]
    draw.text((x, y), text, font=f, fill=fill, stroke_fill=stroke_fill, stroke_width=stroke_width)


# --- background -------------------------------------------------------

FLOOR_Y = 560


def draw_background(draw, shake=(0, 0)):
    sx, sy = shake
    draw.rectangle([0, 0, WIDTH, HEIGHT], fill=WALL)
    draw.rectangle([0, FLOOR_Y, WIDTH, HEIGHT], fill=FLOOR)
    draw.rectangle([0, FLOOR_Y - 6, WIDTH, FLOOR_Y], fill=WALL_TRIM)

    # window
    wx, wy = 90 + sx, 90 + sy
    draw.rounded_rectangle([wx, wy, wx + 200, wy + 220], radius=14, fill=WINDOW_SKY, outline=WALL_TRIM, width=8)
    draw.line([wx + 100, wy, wx + 100, wy + 220], fill=WALL_TRIM, width=8)
    draw.line([wx, wy + 110, wx + 200, wy + 110], fill=WALL_TRIM, width=8)
    draw.ellipse([wx + 130, wy + 30, wx + 170, wy + 70], fill=(255, 244, 214))

    # rug
    cxr, cyr = WIDTH * 0.52 + sx, FLOOR_Y + 95 + sy
    draw.ellipse([cxr - 330, cyr - 90, cxr + 330, cyr + 90], fill=RUG)
    draw.ellipse([cxr - 330, cyr - 90, cxr + 330, cyr + 90], outline=RUG_DARK, width=6)
    draw.ellipse([cxr - 230, cyr - 55, cxr + 230, cyr + 55], outline=RUG_DARK, width=4)

    # side table + plant (left)
    tx, ty = 150 + sx, FLOOR_Y - 70 + sy
    draw.rectangle([tx, ty, tx + 120, ty + 18], fill=TABLE)
    draw.rectangle([tx + 12, ty + 18, tx + 26, ty + 80], fill=TABLE)
    draw.rectangle([tx + 94, ty + 18, tx + 108, ty + 80], fill=TABLE)

    # couch (right)
    cx0, cy0 = WIDTH - 330 + sx, FLOOR_Y - 150 + sy
    draw.rounded_rectangle([cx0, cy0, cx0 + 320, cy0 + 190], radius=26, fill=COUCH)
    draw.rounded_rectangle([cx0, cy0, cx0 + 320, cy0 + 60], radius=22, fill=COUCH_DARK)
    draw.rounded_rectangle([cx0 - 18, cy0 + 30, cx0 + 30, cy0 + 190], radius=20, fill=COUCH_DARK)
    draw.rounded_rectangle([cx0 + 290, cy0 + 30, cx0 + 338, cy0 + 190], radius=20, fill=COUCH_DARK)
    for i in range(3):
        lx = cx0 + 40 + i * 95
        draw.rounded_rectangle([lx, cy0 + 70, lx + 80, cy0 + 150], radius=18, fill=COUCH, outline=COUCH_DARK, width=3)

    return tx + 60, ty  # returns plant pot anchor point


def draw_plant_pot(draw, x, y, tilt=0.0, on_head=False, scale=1.0):
    """Potted plant. If on_head, drawn upside-down-ish sitting like a hat."""
    w, h = 64 * scale, 46 * scale
    ang = math.radians(tilt)
    cos_a, sin_a = math.cos(ang), math.sin(ang)

    def rot(px, py):
        return (x + (px * cos_a - py * sin_a), y + (px * sin_a + py * cos_a))

    pot_pts = [rot(-w / 2, 0), rot(w / 2, 0), rot(w / 2 - 8, h), rot(-w / 2 + 8, h)]
    draw.polygon(pot_pts, fill=POT, outline=(120, 60, 40))
    if not on_head:
        for dx, dy, r in [(-14, -10, 22), (0, -26, 26), (16, -8, 20)]:
            px, py = rot(dx, dy)
            draw.ellipse([px - r, py - r, px + r, py + r], fill=PLANT)
    else:
        for dx, dy, r in [(-16, -4, 16), (2, -14, 18), (16, -2, 15)]:
            px, py = rot(dx, dy)
            draw.ellipse([px - r, py - r, px + r, py + r], fill=PLANT)


def draw_stars(draw, cx, cy, t, n=3, radius=34):
    for i in range(n):
        a = t * 3.2 + i * (2 * math.pi / n)
        sx = cx + math.cos(a) * radius
        sy = cy - 14 + math.sin(a) * (radius * 0.4)
        draw_star_shape(draw, sx, sy, 9)


def draw_star_shape(draw, cx, cy, r):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        a = math.pi / 2 + i * math.pi / 5
        pts.append((cx + math.cos(a) * rad, cy - math.sin(a) * rad))
    draw.polygon(pts, fill=(255, 221, 74), outline=(200, 150, 20))


def draw_speed_lines(draw, x, y, facing, n=4, length=70, spread=54):
    for i in range(n):
        yy = y - spread / 2 + i * (spread / max(1, n - 1))
        x1 = x - facing * (10)
        x2 = x - facing * (10 + length)
        draw.line([(x1, yy), (x2, yy)], fill=(255, 255, 255, 160), width=4)


def draw_dust_cloud(draw, x, y, t):
    for i in range(5):
        a = i * (2 * math.pi / 5) + t * 4
        r = 18 + 10 * math.sin(t * 6 + i)
        dx = math.cos(a) * (20 + t * 30)
        dy = math.sin(a) * 8
        draw.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(255, 255, 255, 110))


def draw_paw_print(draw, cx, cy, r=14, color=(255, 221, 74)):
    draw.ellipse([cx - r, cy - r * 0.75, cx + r, cy + r * 0.95], fill=color)
    for dx, dy, rr in [(-r * 0.9, -r * 0.9, r * 0.42), (-r * 0.3, -r * 1.25, r * 0.42),
                        (r * 0.3, -r * 1.25, r * 0.42), (r * 0.9, -r * 0.9, r * 0.42)]:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr], fill=color)


def draw_squeak(draw, x, y, t):
    """Little musical squiggle to indicate a toy squeak."""
    pts = []
    for i in range(14):
        px = x + i * 4
        py = y - 24 - 10 * math.sin(i * 0.9 + t * 10)
        pts.append((px, py))
    draw.line(pts, fill=(255, 244, 120, 220), width=4, joint="curve")
    for i, txt in enumerate("!"):
        pass
