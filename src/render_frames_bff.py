#!/usr/bin/env python3
"""Renders the "Dog & Cat: Best Friends" video as a PNG sequence.
Companion to render_frames.py -- same character rigs, recolored white,
happy chase in a yard then sharing a bowl indoors. No fighting.

Usage: python3 render_frames_bff.py <output_dir>
"""
import math
import os
import sys

from anim_common import (
    WIDTH, HEIGHT, FPS, new_canvas, draw_background, draw_yard_background,
    draw_food_bowl, draw_paw_print, draw_dust_cloud,
    text_center, font, TITLE_FONT_PATH, BODY_FONT_PATH,
    ease_out_back, ease_in_out, ease_out_bounce, scene_t, lerp, clamp01,
    jump_lift, INK, WHITE, BLACK,
    DOG_FUR_WHITE, DOG_FUR_WHITE_DARK, DOG_EAR_WHITE, DOG_SNOUT_WHITE, DOG_COLLAR,
    CAT_FUR_WHITE, CAT_FUR_WHITE_DARK, CAT_EAR_INNER_WHITE, CAT_BOW,
)
from characters import draw_dog, draw_cat

# --- timeline (seconds) ------------------------------------------------
T_TITLE = (0.0, 3.0)
T_CHASE = (3.0, 13.5)
T_HEADIN = (13.5, 15.5)
T_ENTER = (15.5, 17.0)
T_FEED = (17.0, 23.0)
T_NUZZLE = (23.0, 27.5)
T_END = (27.5, 32.0)
TOTAL_DURATION = 32.0

# yard scene geometry
YARD_STAND_Y = 480
HEDGE_X = WIDTH - 150

# living room scene geometry (matches render_frames.py's living room)
RUG_CX = 666
STAND_Y = 630
BOWL_X, BOWL_Y = RUG_CX, STAND_Y + 58

DOG_KW = dict(fur=DOG_FUR_WHITE, fur_dark=DOG_FUR_WHITE_DARK, ear_color=DOG_EAR_WHITE,
              snout_color=DOG_SNOUT_WHITE, collar_color=DOG_COLLAR, chest_color=(255, 249, 240))
CAT_KW = dict(fur=CAT_FUR_WHITE, fur_dark=CAT_FUR_WHITE_DARK, ear_inner=CAT_EAR_INNER_WHITE,
              show_stripes=False, bow_color=CAT_BOW)

TITLE_FONT = None
SUB_FONT = None
BODY_FONT = None


def _fonts():
    global TITLE_FONT, SUB_FONT, BODY_FONT
    if TITLE_FONT is None:
        TITLE_FONT = font(TITLE_FONT_PATH, 92)
        SUB_FONT = font(TITLE_FONT_PATH, 38)
        BODY_FONT = font(BODY_FONT_PATH, 30)
    return TITLE_FONT, SUB_FONT, BODY_FONT


def get_frame(t):
    title_font, sub_font, body_font = _fonts()
    img, draw = new_canvas()

    indoor = t >= T_ENTER[0]
    if indoor:
        draw_background(draw)
    else:
        draw_yard_background(draw)

    dog = dict(cx=250, cy=YARD_STAND_Y, scale=1.3, facing=1, leg_phase=0, mouth_open=0.3,
               tilt=0, tail_wag=0, dazed=False, panting=False, stretch=0, squash=1.0,
               closed_eyes=False)
    cat = dict(cx=420, cy=YARD_STAND_Y, scale=1.0, facing=1, leg_phase=0, tilt=0,
               tail_flick=0, dazed=False, panting=False, stretch=0, smug=False, squash=1.0,
               closed_eyes=False)
    bowl_fill = 1.0
    title_alpha = 0.0
    end_alpha = 0.0
    fade_warm = 0.0
    show_bowl = False

    if t < T_TITLE[1]:
        lt = scene_t(t, *T_TITLE)
        dog['cx'] = lerp(-150, 300, ease_in_out(min(1, lt * 1.6)))
        dog['cy'] = YARD_STAND_Y - abs(math.sin(t * 8)) * 14
        dog['leg_phase'] = t * 9
        dog['tail_wag'] = t * 10
        cat['cx'] = lerp(WIDTH + 150, 900, ease_in_out(min(1, lt * 1.6)))
        cat['facing'] = -1
        cat['cy'] = YARD_STAND_Y - abs(math.sin(t * 9)) * 12
        cat['leg_phase'] = t * 9
        cat['tail_flick'] = t * 6
        title_alpha = ease_out_back(clamp01((t - 0.2) / 1.0))

    elif t < T_CHASE[1]:
        lt = scene_t(t, *T_CHASE)
        lane_lo, lane_hi = 260, 1080
        n_laps = 2.5
        phase = lt * 2 * math.pi * n_laps
        pos = (math.sin(phase - math.pi / 2) + 1) / 2
        lead_x = lerp(lane_lo, lane_hi, pos)
        vel = math.cos(phase - math.pi / 2)
        facing = 1 if vel >= 0 else -1

        dog['cx'] = lead_x
        dog['facing'] = facing
        cat['cx'] = lead_x - facing * 210
        cat['facing'] = facing
        dog['leg_phase'] = t * 22
        cat['leg_phase'] = t * 22
        dog['tail_wag'] = t * 16
        cat['tail_flick'] = t * 14
        dog['mouth_open'] = 0.45
        dog['panting'] = True

        bounce = abs(math.sin(t * 10)) * 10
        dog['cy'] = YARD_STAND_Y - bounce
        cat['cy'] = YARD_STAND_Y - bounce * 0.9

        for who in (dog, cat):
            dist = abs(who['cx'] - HEDGE_X)
            hop = max(0.0, 1 - dist / 130) ** 2
            who['cy'] -= hop * 90 * who['scale']
            who['squash'] = lerp(1.0, 1.2, hop)
            if hop > 0.05:
                draw_dust_cloud(draw, who['cx'], YARD_STAND_Y + 20, t)

    elif t < T_HEADIN[1]:
        lt = scene_t(t, *T_HEADIN)
        e = ease_in_out(lt)
        dog['cx'] = lerp(dog.get('cx', 900), WIDTH + 200, e)
        cat['cx'] = lerp(cat.get('cx', 780), WIDTH + 260, e)
        dog['facing'] = 1
        cat['facing'] = 1
        dog['leg_phase'] = t * 24
        cat['leg_phase'] = t * 24
        dog['tail_wag'] = t * 18
        cat['tail_flick'] = t * 16
        dog['cy'] = YARD_STAND_Y - abs(math.sin(t * 11)) * 10
        cat['cy'] = YARD_STAND_Y - abs(math.sin(t * 11)) * 9
        dog['mouth_open'] = 0.4
        dog['panting'] = True

    elif t < T_ENTER[1]:
        lt = scene_t(t, *T_ENTER)
        e = ease_out_bounce(lt)
        dog['cx'] = lerp(-150, 560, e)
        cat['cx'] = lerp(-260, 760, e)
        cat['facing'] = -1
        dog['leg_phase'] = t * 20
        cat['leg_phase'] = t * 20
        dog['tail_wag'] = t * 14
        cat['tail_flick'] = t * 12
        dog['cy'] = STAND_Y
        cat['cy'] = STAND_Y
        show_bowl = True
        bowl_fill = 1.0

    elif t < T_FEED[1]:
        lt = scene_t(t, *T_FEED)
        show_bowl = True
        dog['cy'] = STAND_Y
        cat['cy'] = STAND_Y

        if lt < 0.35:
            # Rex trots up and noses the bowl toward Whiskers
            e = ease_in_out(clamp01(lt / 0.35))
            dog['cx'] = lerp(560, 610, e)
            cat['cx'] = 760
            cat['facing'] = -1
            dog['leg_phase'] = t * 16
            dog['tail_wag'] = t * 12
            dog['mouth_open'] = 0.2 + 0.1 * math.sin(t * 6)
            bowl_fill = 1.0
        elif lt < 0.65:
            # Whiskers happily eats -- bowl empties a little
            e = clamp01((lt - 0.35) / 0.3)
            dog['cx'] = 610
            cat['cx'] = lerp(760, 705, ease_in_out(e))
            cat['facing'] = -1
            cat['leg_phase'] = t * 10
            cat['tail_flick'] = t * 14
            bowl_fill = lerp(1.0, 0.55, e)
            dog['tail_wag'] = t * 14
        else:
            # Whiskers noses it back, Rex takes a turn
            e = clamp01((lt - 0.65) / 0.35)
            cat['cx'] = lerp(705, 750, ease_in_out(e))
            dog['cx'] = lerp(610, 640, ease_in_out(e))
            dog['facing'] = 1
            dog['leg_phase'] = t * 10
            dog['mouth_open'] = 0.2 + 0.15 * math.sin(t * 7)
            bowl_fill = lerp(0.55, 0.3, e)
            cat['tail_flick'] = t * 12
            dog['tail_wag'] = t * 16

    elif t < T_NUZZLE[1]:
        lt = scene_t(t, *T_NUZZLE)
        show_bowl = True
        bowl_fill = 0.28
        e = ease_in_out(min(1, lt * 2.0))
        dog['cx'] = lerp(640, 610, e)
        cat['cx'] = lerp(750, 715, e)
        dog['facing'] = 1
        cat['facing'] = -1
        dog['cy'] = STAND_Y
        cat['cy'] = STAND_Y
        dog['tilt'] = lerp(0, 10, e)
        cat['tilt'] = lerp(0, -10, e)
        dog['closed_eyes'] = lt > 0.35
        cat['closed_eyes'] = lt > 0.35
        dog['tail_wag'] = t * 8
        cat['tail_flick'] = t * 6

    else:
        lt = scene_t(t, *T_END)
        show_bowl = True
        bowl_fill = 0.28
        dog['cx'] = 610
        cat['cx'] = 715
        dog['facing'] = 1
        cat['facing'] = -1
        dog['cy'] = STAND_Y
        cat['cy'] = STAND_Y
        dog['tail_wag'] = t * 10
        cat['tail_flick'] = t * 8
        fade_warm = ease_in_out(clamp01((lt - 0.5) / 0.35))
        end_alpha = ease_out_back(clamp01((lt - 0.6) / 0.35))

    # --- compose ----------------------------------------------------------
    draw_dog(draw, dog['cx'], dog['cy'], scale=dog['scale'], facing=dog['facing'],
              leg_phase=dog['leg_phase'], mouth_open=dog['mouth_open'], tilt=dog['tilt'],
              tail_wag=dog['tail_wag'], dazed=dog['dazed'], panting=dog['panting'],
              stretch=dog['stretch'], squash=dog['squash'], closed_eyes=dog['closed_eyes'], **DOG_KW)

    draw_cat(draw, cat['cx'], cat['cy'], scale=cat['scale'], facing=cat['facing'],
              leg_phase=cat['leg_phase'], tilt=cat['tilt'], tail_flick=cat['tail_flick'],
              dazed=cat['dazed'], panting=cat['panting'], stretch=cat['stretch'],
              smug=cat['smug'], squash=cat['squash'], closed_eyes=cat['closed_eyes'], **CAT_KW)

    if show_bowl:
        draw_food_bowl(draw, BOWL_X, BOWL_Y, scale=1.2, fill_level=bowl_fill)

    # --- text overlays ------------------------------------------------------
    if title_alpha > 0.02:
        bounce_y = 150 - 20 * math.sin(t * 4)
        text_center(draw, WIDTH / 2, bounce_y, "DOG & CAT", title_font, fill=(255, 255, 255),
                    stroke_fill=INK, stroke_width=6)
        text_center(draw, WIDTH / 2, bounce_y + 74, "BEST FRIENDS", sub_font, fill=(120, 200, 255),
                    stroke_fill=INK, stroke_width=5)

    if fade_warm > 0.01:
        from PIL import Image
        warm = Image.new("RGB", (WIDTH, HEIGHT), (255, 241, 214))
        img = Image.blend(img, warm, clamp01(fade_warm))

    if end_alpha > 0.02:
        draw2 = __import__('PIL.ImageDraw', fromlist=['ImageDraw']).Draw(img, "RGBA")
        text_center(draw2, WIDTH / 2, HEIGHT / 2 - 40, "BEST FRIENDS FOREVER", title_font, fill=(255, 255, 255),
                    stroke_fill=INK, stroke_width=6)
        text_center(draw2, WIDTH / 2, HEIGHT / 2 + 40, "Subscribe for more!", sub_font, fill=(120, 200, 255),
                    stroke_fill=INK, stroke_width=5)
        for side in (-1, 1):
            draw_paw_print(draw2, WIDTH / 2 + side * 230, HEIGHT / 2 + 40, r=16)

    return img


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/frames_bff"
    os.makedirs(out_dir, exist_ok=True)
    n_frames = int(round(TOTAL_DURATION * FPS))
    for i in range(n_frames):
        t = i / FPS
        img = get_frame(t)
        img.save(os.path.join(out_dir, f"frame_{i:05d}.png"))
        if i % 48 == 0:
            print(f"rendered frame {i}/{n_frames} (t={t:.2f}s)")
    print(f"done: {n_frames} frames -> {out_dir}")


if __name__ == "__main__":
    main()
