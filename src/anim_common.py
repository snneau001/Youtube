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

# Vertical (9:16) canvas for YouTube Shorts cuts
SHORT_WIDTH, SHORT_HEIGHT = 1080, 1920
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

# "Best Friends" video palette -- white dog/cat + outdoor yard scene
DOG_FUR_WHITE = (252, 249, 244)
DOG_FUR_WHITE_DARK = (222, 214, 202)
DOG_EAR_WHITE = (235, 224, 208)
DOG_SNOUT_WHITE = (255, 240, 232)
DOG_COLLAR = (219, 92, 78)
CAT_FUR_WHITE = (255, 255, 255)
CAT_FUR_WHITE_DARK = (226, 226, 232)
CAT_EAR_INNER_WHITE = (250, 210, 218)
CAT_BOW = (86, 140, 219)

YARD_SKY_TOP = (137, 199, 232)
YARD_SKY_BOTTOM = (206, 233, 245)
GRASS = (140, 197, 104)
GRASS_DARK = (117, 176, 84)
TREE_TRUNK = (140, 96, 61)
TREE_LEAVES = (86, 163, 96)
TREE_LEAVES_DARK = (66, 140, 78)
FENCE = (223, 200, 165)
FENCE_DARK = (196, 170, 135)
SUN = (255, 226, 128)
BOWL_COLOR = (219, 130, 84)
BOWL_DARK = (185, 100, 60)
KIBBLE = (200, 140, 80)


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


FLOOR_Y_V = 1360  # vertical (Shorts) living room floor line


def draw_background_vertical(draw, shake=(0, 0)):
    """Vertical (1080x1920) living room -- same elements as draw_background,
    reflowed for a 9:16 Shorts canvas."""
    sx, sy = shake
    W, H = SHORT_WIDTH, SHORT_HEIGHT
    draw.rectangle([0, 0, W, H], fill=WALL)
    draw.rectangle([0, FLOOR_Y_V, W, H], fill=FLOOR)
    draw.rectangle([0, FLOOR_Y_V - 6, W, FLOOR_Y_V], fill=WALL_TRIM)

    wx, wy = W * 0.5 - 110 + sx, 110 + sy
    draw.rounded_rectangle([wx, wy, wx + 220, wy + 240], radius=16, fill=WINDOW_SKY, outline=WALL_TRIM, width=9)
    draw.line([wx + 110, wy, wx + 110, wy + 240], fill=WALL_TRIM, width=9)
    draw.line([wx, wy + 120, wx + 220, wy + 120], fill=WALL_TRIM, width=9)
    draw.ellipse([wx + 142, wy + 34, wx + 186, wy + 78], fill=(255, 244, 214))

    cxr, cyr = W * 0.5 + sx, FLOOR_Y_V + 220 + sy
    draw.ellipse([cxr - 420, cyr - 190, cxr + 420, cyr + 190], fill=RUG)
    draw.ellipse([cxr - 420, cyr - 190, cxr + 420, cyr + 190], outline=RUG_DARK, width=7)
    draw.ellipse([cxr - 300, cyr - 120, cxr + 300, cyr + 120], outline=RUG_DARK, width=5)

    tx, ty = 40 + sx, FLOOR_Y_V - 80 + sy
    draw.rectangle([tx, ty, tx + 130, ty + 20], fill=TABLE)
    draw.rectangle([tx + 12, ty + 20, tx + 28, ty + 88], fill=TABLE)
    draw.rectangle([tx + 102, ty + 20, tx + 118, ty + 88], fill=TABLE)

    cx0, cy0 = W - 300 + sx, FLOOR_Y_V - 170 + sy
    draw.rounded_rectangle([cx0, cy0, cx0 + 300, cy0 + 210], radius=28, fill=COUCH)
    draw.rounded_rectangle([cx0, cy0, cx0 + 300, cy0 + 66], radius=24, fill=COUCH_DARK)
    draw.rounded_rectangle([cx0 - 18, cy0 + 34, cx0 + 30, cy0 + 210], radius=22, fill=COUCH_DARK)
    draw.rounded_rectangle([cx0 + 268, cy0 + 34, cx0 + 316, cy0 + 210], radius=22, fill=COUCH_DARK)
    for i in range(3):
        lx = cx0 + 34 + i * 90
        draw.rounded_rectangle([lx, cy0 + 78, lx + 76, cy0 + 168], radius=18, fill=COUCH, outline=COUCH_DARK, width=3)

    return tx + 65, ty


def draw_yard_background_vertical(draw, shake=(0, 0)):
    """Vertical (1080x1920) yard scene -- reflowed for a 9:16 Shorts canvas."""
    sx, sy = shake
    W, H = SHORT_WIDTH, SHORT_HEIGHT
    horizon = 620
    for i in range(horizon):
        t = i / horizon
        c = tuple(int(lerp(a, b, t)) for a, b in zip(YARD_SKY_TOP, YARD_SKY_BOTTOM))
        draw.line([(0, i), (W, i)], fill=c)
    draw.ellipse([W - 220 + sx, 70 + sy, W - 100 + sx, 190 + sy], fill=SUN)

    draw.rectangle([0, horizon, W, H], fill=GRASS)
    for gx in range(-20, W + 20, 44):
        gy = horizon + 30 + 20 * math.sin(gx * 0.05)
        draw.line([(gx + sx, gy + sy), (gx + sx - 9, gy - 24 + sy)], fill=GRASS_DARK, width=5)

    for fx in range(-10, W + 40, 68):
        draw.rounded_rectangle([fx + sx, horizon - 76 + sy, fx + 24 + sx, horizon + 22 + sy], radius=7, fill=FENCE, outline=FENCE_DARK, width=3)
    draw.rectangle([0 + sx, horizon - 48 + sy, W + sx, horizon - 32 + sy], fill=FENCE_DARK)

    tx, ty = 190 + sx, horizon + sy
    draw.rectangle([tx - 18, ty - 100, tx + 18, ty + 12], fill=TREE_TRUNK)
    for dx, dy, r in [(-42, -168, 70), (34, -180, 76), (0, -214, 66), (-12, -136, 56)]:
        draw.ellipse([tx + dx - r, ty + dy - r, tx + dx + r, ty + dy + r], fill=TREE_LEAVES)
    draw.ellipse([tx - 22 - 44, ty - 146 - 44, tx - 22 + 44, ty - 146 + 44], fill=TREE_LEAVES_DARK)

    hx, hy = W - 220 + sx, horizon + 340 + sy
    for i in range(5):
        r = 38
        draw.ellipse([hx + i * 34 - r, hy - r, hx + i * 34 + r, hy + r * 0.7], fill=TREE_LEAVES)
    draw.ellipse([hx + 64 - 32, hy - 36, hx + 64 + 32, hy + 22], fill=TREE_LEAVES_DARK)

    return hx + 64, hy - 42


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


def draw_yard_background(draw, shake=(0, 0)):
    """Outdoor yard scene: sky, grassy ground, a tree, and a fence."""
    sx, sy = shake
    horizon = 230
    for i in range(horizon):
        t = i / horizon
        c = tuple(int(lerp(a, b, t)) for a, b in zip(YARD_SKY_TOP, YARD_SKY_BOTTOM))
        draw.line([(0, i), (WIDTH, i)], fill=c)
    draw.ellipse([WIDTH - 190 + sx, 40 + sy, WIDTH - 90 + sx, 140 + sy], fill=SUN)

    draw.rectangle([0, horizon, WIDTH, HEIGHT], fill=GRASS)
    for gx in range(-20, WIDTH + 20, 46):
        gy = horizon + 26 + 18 * math.sin(gx * 0.05)
        draw.line([(gx + sx, gy + sy), (gx + sx - 8, gy - 22 + sy)], fill=GRASS_DARK, width=5)

    # fence along the horizon
    for fx in range(-10, WIDTH + 40, 70):
        draw.rounded_rectangle([fx + sx, horizon - 70 + sy, fx + 22 + sx, horizon + 20 + sy], radius=6, fill=FENCE, outline=FENCE_DARK, width=3)
    draw.rectangle([0 + sx, horizon - 44 + sy, WIDTH + sx, horizon - 30 + sy], fill=FENCE_DARK)

    # a friendly tree, back-left
    tx, ty = 165 + sx, horizon + sy
    draw.rectangle([tx - 16, ty - 90, tx + 16, ty + 10], fill=TREE_TRUNK)
    for dx, dy, r in [(-38, -150, 62), (30, -160, 68), (0, -190, 58), (-10, -120, 50)]:
        draw.ellipse([tx + dx - r, ty + dy - r, tx + dx + r, ty + dy + r], fill=TREE_LEAVES)
    draw.ellipse([tx - 20 - 40, ty - 130 - 40, tx - 20 + 40, ty - 130 + 40], fill=TREE_LEAVES_DARK)

    # low hedge, front-right (fun to hop over)
    hx, hy = WIDTH - 210 + sx, horizon + 170 + sy
    for i in range(5):
        r = 34
        draw.ellipse([hx + i * 32 - r, hy - r, hx + i * 32 + r, hy + r * 0.7], fill=TREE_LEAVES)
    draw.ellipse([hx + 60 - 30, hy - 34, hx + 60 + 30, hy + 20], fill=TREE_LEAVES_DARK)

    return hx + 60, hy - 40  # hedge jump-point anchor


def draw_food_bowl(draw, x, y, scale=1.0, fill_level=1.0):
    """A simple shared pet bowl with kibble; fill_level 0..1 (eaten down)."""
    s = scale
    w, h = 92 * s, 30 * s
    ellipse_safe(draw, x - w / 2, y - h * 0.4, x + w / 2, y + h * 0.7, fill=BOWL_DARK)
    ellipse_safe(draw, x - w / 2 + 6 * s, y - h * 0.55, x + w / 2 - 6 * s, y + h * 0.25, fill=BOWL_COLOR)
    if fill_level > 0.02:
        iw = (w - 22 * s) * min(1.0, fill_level)
        ellipse_safe(draw, x - iw / 2, y - h * 0.45, x + iw / 2, y - h * 0.05, fill=KIBBLE)
        for i in range(int(6 * fill_level) + 1):
            kx = x - iw / 2 + (i * 37 % max(1, iw)) if iw > 0 else x
            ky = y - h * 0.3 + 5 * math.sin(i * 1.7)
            draw.ellipse([kx - 4 * s, ky - 4 * s, kx + 4 * s, ky + 4 * s], fill=_lighten_tuple(KIBBLE, -20))


def _lighten_tuple(color, amount):
    return tuple(max(0, min(255, c + amount)) for c in color)


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


def jump_lift(local_t, height):
    """Parabolic jump arc: 0 at local_t=0/1 (ground), `height` at local_t=0.5 (apex)."""
    lt = clamp01(local_t)
    return height * 4 * lt * (1 - lt)


def draw_swirl_cloud(draw, cx, cy, t, radius=100, n=6, color=(238, 238, 235, 145)):
    """Rotating overlapping puffs -- the classic cartoon scuffle dust ball."""
    for i in range(n):
        a = t * 5.2 + i * (2 * math.pi / n)
        r = radius * 0.45 + radius * 0.4 * math.sin(t * 3.3 + i * 1.7)
        x = cx + math.cos(a) * r
        y = cy + math.sin(a) * r * 0.55
        rr = radius * 0.34
        draw.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color)


def draw_impact_burst(draw, cx, cy, text, f, scale=1.0, color=(255, 221, 74)):
    """Comic-book jagged starburst with punch text ('POW!', 'BAM!', ...)."""
    if scale <= 0.02:
        return
    n = 9
    pts = []
    for i in range(2 * n):
        ang = i * math.pi / n
        r = (46 if i % 2 == 0 else 21) * scale
        pts.append((cx + math.cos(ang) * r, cy + math.sin(ang) * r))
    draw.polygon(pts, fill=color, outline=INK)
    if scale > 0.6:
        text_center(draw, cx, cy, text, f, fill=INK)


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
