"""Procedural cartoon character drawing: Rex (dog) and Whiskers (cat)."""
import math

from anim_common import (
    DOG_FUR, DOG_FUR_DARK, DOG_EAR, CAT_FUR, CAT_FUR_DARK, CAT_STRIPE,
    TOY_RED, WHITE, BLACK, INK, ellipse_safe, draw_taper,
)


def _paw(draw, hx, hy, phase, color, r):
    """A simple bouncing stubby paw -- reads cleanly at chibi scale."""
    bounce = max(0.0, math.sin(phase)) * (r * 0.8)
    fy = hy - bounce
    draw.ellipse([hx - r, fy - r, hx + r, fy + r], fill=color)


def _lighten(color, amount=18):
    return tuple(min(255, c + amount) for c in color[:3])


def draw_dog(draw, cx, cy, scale=1.0, facing=1, leg_phase=0.0, mouth_open=0.0,
             tilt=0.0, squash=1.0, tail_wag=0.0, dazed=False, panting=False,
             stretch=0.0, fur=None, fur_dark=None, ear_color=None, snout_color=None,
             collar_color=None, closed_eyes=False, chest_color=None):
    """Draw Rex the dog centered near (cx, cy) -- cy is roughly hip height.
    facing: 1 = faces right, -1 = faces left.
    stretch: 0..1 extra horizontal pull (used during tug-of-war), body
    leans away from facing direction while head/mouth stays forward.
    fur/fur_dark/ear_color/snout_color: optional palette overrides (used
    for color variants like the white Rex in the "Best Friends" video).
    collar_color: optional -- draws a simple collar band around the neck.
    """
    fur = fur or DOG_FUR
    fur_dark = fur_dark or DOG_FUR_DARK
    ear_color = ear_color or DOG_EAR
    snout_color = snout_color or (255, 224, 176)
    chest_color = chest_color or (245, 200, 140)

    s = scale
    body_w, body_h = (150 + 70 * stretch) * s, 78 * s * (1.0 / (1 + stretch * 0.3)) * squash
    bx = cx - facing * stretch * 40 * s

    # paws (2, front + back, alternating bounce)
    paw_y = cy + body_h * 0.46
    _paw(draw, bx - body_w * 0.26, paw_y, leg_phase, fur_dark, 15 * s)
    _paw(draw, bx + body_w * 0.24, paw_y, leg_phase + math.pi, fur_dark, 15 * s)

    # tail
    twx = bx - facing * body_w * 0.46
    twy = cy - body_h * 0.1
    wag = math.sin(tail_wag) * 26
    draw_taper(draw, twx, twy, twx - facing * 30 * s, twy - 55 * s + wag, 15 * s, 7 * s, fur)

    # body
    draw.ellipse([bx - body_w / 2, cy - body_h / 2, bx + body_w / 2, cy + body_h / 2], fill=fur)
    # chest shading
    draw.ellipse([bx - body_w * 0.15, cy - body_h * 0.3, bx + body_w * 0.5, cy + body_h * 0.5], fill=chest_color)

    if collar_color:
        cx0 = bx + facing * body_w * 0.1
        cx1 = bx + facing * body_w * 0.62
        draw.arc([min(cx0, cx1), cy - body_h * 0.62, max(cx0, cx1), cy - body_h * 0.02],
                  10, 170, fill=collar_color, width=int(9 * s))

    # head
    hx = bx + facing * body_w * 0.42
    hy = cy - body_h * 0.55 + math.sin(tilt) * 4
    head_r = 58 * s
    draw.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r], fill=fur)

    # ears (floppy, smooth taper)
    ear_flop = 10 + 6 * math.sin(tail_wag * 0.7)
    for side in (-1, 1):
        ex = hx + side * head_r * 0.75
        ey = hy - head_r * 0.15
        draw_taper(draw, ex, ey, ex + side * 14 * s, ey + 58 * s + ear_flop, 20 * s, 9 * s, ear_color)

    # snout
    sx = hx + facing * head_r * 0.75
    sy = hy + head_r * 0.25
    ellipse_safe(draw, sx - 30 * s, sy - 22 * s, sx + facing * 34 * s, sy + 22 * s, fill=snout_color)
    # mouth
    mouth_h = 6 + mouth_open * 26
    mx = sx + facing * 14 * s
    ellipse_safe(draw, mx - 16 * s, sy - 4 * s, mx + facing * 20 * s, sy + mouth_h * s, fill=INK)
    if mouth_open > 0.15:
        draw.polygon([(mx - 4 * s, sy + 2 * s), (mx + facing * 8 * s, sy + 2 * s), (mx + facing * 2 * s, sy + mouth_h * s * 0.5)], fill=(255, 255, 255))
    # nose
    draw.ellipse([sx + facing * 22 * s - 9 * s, sy - 14 * s, sx + facing * 22 * s + 9 * s, sy + 2 * s], fill=BLACK)

    # eyes
    eye_y = hy - head_r * 0.15
    if dazed:
        for sign in (-1, 1):
            ex = hx + sign * head_r * 0.32
            draw.line([(ex - 8 * s, eye_y - 8 * s), (ex + 8 * s, eye_y + 8 * s)], fill=INK, width=int(4 * s))
            draw.line([(ex - 8 * s, eye_y + 8 * s), (ex + 8 * s, eye_y - 8 * s)], fill=INK, width=int(4 * s))
    elif closed_eyes:
        for sign in (-1, 1):
            ex = hx + sign * head_r * 0.32
            draw.arc([ex - 9 * s, eye_y - 4 * s, ex + 9 * s, eye_y + 11 * s], 200, 340, fill=INK, width=int(4 * s))
    else:
        for sign in (-1, 1):
            ex = hx + sign * head_r * 0.32
            draw.ellipse([ex - 9 * s, eye_y - 10 * s, ex + 9 * s, eye_y + 10 * s], fill=WHITE, outline=INK)
            draw.ellipse([ex - 4 * s, eye_y - 4 * s, ex + 4 * s, eye_y + 6 * s], fill=BLACK)
    # eyebrow (happy/determined)
    draw.arc([hx - head_r * 0.55, eye_y - 30 * s, hx + head_r * 0.55, eye_y + 6 * s], 200, 340, fill=fur_dark, width=int(4 * s))

    if panting:
        tongue_y = sy + mouth_h * s + 4
        ellipse_safe(draw, mx - 8 * s, sy + 2 * s, mx + 10 * s, tongue_y + 22 * s, fill=(232, 120, 132))


def draw_cat(draw, cx, cy, scale=1.0, facing=1, leg_phase=0.0, tilt=0.0,
             squash=1.0, tail_flick=0.0, dazed=False, panting=False,
             stretch=0.0, smug=False, fur=None, fur_dark=None, stripe_color=None,
             show_stripes=True, ear_inner=None, bow_color=None, closed_eyes=False):
    """Draw Whiskers the cat centered near (cx, cy) -- chibi proportions
    (oversized head, small body, big sparkly eyes) for extra cuteness.
    fur/fur_dark/stripe_color/ear_inner: optional palette overrides (used
    for color variants like the white Whiskers in the "Best Friends" video).
    show_stripes: set False for a solid-color coat (e.g. a white cat).
    bow_color: optional -- draws a little bow on one ear.
    """
    fur = fur or CAT_FUR
    fur_dark = fur_dark or CAT_FUR_DARK
    stripe_color = stripe_color or CAT_STRIPE
    ear_inner = ear_inner or (245, 200, 210)

    s = scale
    body_w, body_h = (100 + 50 * stretch) * s, 54 * s * (1.0 / (1 + stretch * 0.3)) * squash
    bx = cx - facing * stretch * 30 * s

    # paws (2, front + back, alternating bounce)
    paw_y = cy + body_h * 0.5
    _paw(draw, bx - body_w * 0.22, paw_y, leg_phase, fur_dark, 11 * s)
    _paw(draw, bx + body_w * 0.20, paw_y, leg_phase + math.pi, fur_dark, 11 * s)

    # tail (long, curved, flicking, fluffy tip)
    tbx = bx - facing * body_w * 0.5
    tby = cy
    flick = math.sin(tail_flick) * 34
    tip_x, tip_y = tbx - facing * 34 * s, tby - 70 * s + flick
    draw_taper(draw, tbx, tby, tip_x, tip_y, 12 * s, 6 * s, fur)
    draw.ellipse([tip_x - 10 * s, tip_y - 10 * s, tip_x + 10 * s, tip_y + 10 * s], fill=fur)

    draw.ellipse([bx - body_w / 2, cy - body_h / 2, bx + body_w / 2, cy + body_h / 2], fill=fur)
    if show_stripes:
        for dx in (-0.25, 0.05, 0.32):
            draw.arc([bx + body_w * dx - 12 * s, cy - body_h * 0.4, bx + body_w * dx + 12 * s, cy + body_h * 0.4], 20, 160, fill=stripe_color, width=int(3 * s))

    hx = bx + facing * body_w * 0.42
    hy = cy - body_h * 0.62 + math.sin(tilt) * 4
    head_r = 54 * s  # oversized chibi head

    for side in (-1, 1):
        ex = hx + side * head_r * 0.68
        ey = hy - head_r * 0.8
        draw.polygon([(ex - 17 * s, ey + 15 * s), (ex + 17 * s, ey + 15 * s), (ex, ey - 20 * s)], fill=fur)
        draw.polygon([(ex - 9 * s, ey + 9 * s), (ex + 9 * s, ey + 9 * s), (ex, ey - 8 * s)], fill=ear_inner)
        if bow_color and side == 1:
            draw.polygon([(ex - 12 * s, ey + 2 * s), (ex - 2 * s, ey - 4 * s), (ex - 12 * s, ey - 10 * s)], fill=bow_color)
            draw.polygon([(ex + 12 * s, ey + 2 * s), (ex + 2 * s, ey - 4 * s), (ex + 12 * s, ey - 10 * s)], fill=bow_color)
            draw.ellipse([ex - 4 * s, ey - 8 * s, ex + 4 * s, ey], fill=_lighten(bow_color, 25))

    draw.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r], fill=fur)
    # fluffy cheek tufts
    for sign in (-1, 1):
        cxx = hx + sign * head_r * 0.92
        draw.ellipse([cxx - 12 * s, hy + head_r * 0.15 - 12 * s, cxx + 12 * s, hy + head_r * 0.15 + 12 * s], fill=fur)

    sx = hx + facing * head_r * 0.5
    sy = hy + head_r * 0.4
    for w_ in (-1, 1):
        wy = sy + w_ * 7 * s
        draw.line([(sx, wy), (sx + facing * 32 * s, wy - w_ * 8 * s)], fill=(255, 255, 255, 210), width=2)

    # blush
    for sign in (-1, 1):
        bxx = hx + sign * head_r * 0.62
        byy = hy + head_r * 0.32
        draw.ellipse([bxx - 11 * s, byy - 7 * s, bxx + 11 * s, byy + 7 * s], fill=(255, 150, 160, 110))

    eye_y = hy - head_r * 0.05
    if dazed:
        for sign in (-1, 1):
            ex = hx + sign * head_r * 0.36
            draw.line([(ex - 7 * s, eye_y - 7 * s), (ex + 7 * s, eye_y + 7 * s)], fill=INK, width=int(3 * s))
            draw.line([(ex - 7 * s, eye_y + 7 * s), (ex + 7 * s, eye_y - 7 * s)], fill=INK, width=int(3 * s))
    elif smug or closed_eyes:
        for sign in (-1, 1):
            ex = hx + sign * head_r * 0.36
            draw.arc([ex - 9 * s, eye_y - 6 * s, ex + 9 * s, eye_y + 9 * s], 20, 160, fill=INK, width=int(4 * s))
    else:
        for sign in (-1, 1):
            ex = hx + sign * head_r * 0.36
            draw.ellipse([ex - 11 * s, eye_y - 13 * s, ex + 11 * s, eye_y + 13 * s], fill=WHITE, outline=INK, width=2)
            draw.ellipse([ex - 6.5 * s, eye_y - 8 * s, ex + 6.5 * s, eye_y + 9 * s], fill=(90, 190, 110))
            draw.ellipse([ex - 3.5 * s, eye_y - 5 * s, ex + 3.5 * s, eye_y + 5 * s], fill=BLACK)
            # sparkle highlight
            draw.ellipse([ex - 4 * s, eye_y - 10 * s, ex + 0.5 * s, eye_y - 6 * s], fill=WHITE)

    draw.polygon([(sx + facing * 9 * s, sy - 5 * s), (sx + facing * 9 * s, sy + 5 * s), (sx + facing * 17 * s, sy)], fill=(235, 140, 160))

    if panting:
        ellipse_safe(draw, sx + facing * 4 * s, sy + 4 * s, sx + facing * 14 * s, sy + 20 * s, fill=(232, 140, 150))


def draw_toy(draw, x1, y1, x2, y2, width=14):
    """Squeaky bone toy stretched between two grip points."""
    draw.line([(x1, y1), (x2, y2)], fill=TOY_RED, width=width)
    for (x, y) in [(x1, y1), (x2, y2)]:
        for dx, dy in [(-6, -6), (-6, 6), (6, -6), (6, 6)]:
            draw.ellipse([x + dx - 8, y + dy - 8, x + dx + 8, y + dy + 8], fill=TOY_RED)
