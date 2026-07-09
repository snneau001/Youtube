#!/usr/bin/env python3
"""Renders "Dog & Cat: Best Friends" as a vertical (1080x1920) YouTube
Short: same characters/story as render_frames_bff.py, but reformatted
for 9:16 and re-paced for Shorts -- action starts at frame 0 (no static
title beat), tighter scene durations, ~27s total.

Usage: python3 render_frames_shorts.py <output_dir>
"""
import math
import os
import sys

from anim_common import (
    SHORT_WIDTH, SHORT_HEIGHT, FPS, draw_background_vertical, draw_yard_background_vertical,
    draw_food_bowl, draw_paw_print, draw_dust_cloud,
    text_center, font, TITLE_FONT_PATH, BODY_FONT_PATH,
    ease_out_back, ease_in_out, ease_out_bounce, scene_t, lerp, clamp01,
    jump_lift, INK, WHITE, BLACK,
    DOG_FUR_WHITE, DOG_FUR_WHITE_DARK, DOG_EAR_WHITE, DOG_SNOUT_WHITE, DOG_COLLAR,
    CAT_FUR_WHITE, CAT_FUR_WHITE_DARK, CAT_EAR_INNER_WHITE, CAT_BOW,
    SKY,
)
from characters import draw_dog, draw_cat
from PIL import Image, ImageDraw

# --- timeline (seconds) -- hook-first, tight pacing for Shorts --------
T_CHASE = (0.0, 9.0)
T_HEADIN = (9.0, 10.5)
T_ENTER = (10.5, 11.5)
T_FEED = (11.5, 18.0)
T_NUZZLE = (18.0, 21.5)
T_END = (21.5, 26.5)
TOTAL_DURATION = 26.5

# yard scene geometry (vertical)
YARD_STAND_Y = 820
HEDGE_X = 924

# living room scene geometry (vertical)
RUG_CX = SHORT_WIDTH // 2
STAND_Y = 1400
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
        TITLE_FONT = font(TITLE_FONT_PATH, 104)
        SUB_FONT = font(TITLE_FONT_PATH, 44)
        BODY_FONT = font(BODY_FONT_PATH, 34)
    return TITLE_FONT, SUB_FONT, BODY_FONT


def new_canvas_v():
    img = Image.new("RGB", (SHORT_WIDTH, SHORT_HEIGHT), SKY)
    return img, ImageDraw.Draw(img, "RGBA")


def get_frame(t):
    title_font, sub_font, body_font = _fonts()
    img, draw = new_canvas_v()

    indoor = t >= T_ENTER[0]
    if indoor:
        draw_background_vertical(draw)
    else:
        draw_yard_background_vertical(draw)

    dog = dict(cx=380, cy=YARD_STAND_Y, scale=1.3, facing=1, leg_phase=0, mouth_open=0.35,
               tilt=0, tail_wag=0, dazed=False, panting=False, stretch=0, squash=1.0,
               closed_eyes=False)
    cat = dict(cx=560, cy=YARD_STAND_Y, scale=1.0, facing=1, leg_phase=0, tilt=0,
               tail_flick=0, dazed=False, panting=False, stretch=0, smug=False, squash=1.0,
               closed_eyes=False)
    bowl_fill = 1.0
    title_alpha = 0.0
    end_alpha = 0.0
    fade_warm = 0.0
    show_bowl = False

    if t < T_CHASE[1]:
        lt = scene_t(t, *T_CHASE)
        lane_lo, lane_hi = 150, 900
        n_laps = 2.3
        phase = lt * 2 * math.pi * n_laps
        pos = (math.sin(phase - math.pi / 2) + 1) / 2
        lead_x = lerp(lane_lo, lane_hi, pos)
        vel = math.cos(phase - math.pi / 2)
        facing = 1 if vel >= 0 else -1

        dog['cx'] = lead_x
        dog['facing'] = facing
        cat['cx'] = lead_x - facing * 170
        cat['facing'] = facing
        dog['leg_phase'] = t * 22
        cat['leg_phase'] = t * 22
        dog['tail_wag'] = t * 16
        cat['tail_flick'] = t * 14
        dog['mouth_open'] = 0.45
        dog['panting'] = True

        bounce = abs(math.sin(t * 10)) * 11
        dog['cy'] = YARD_STAND_Y - bounce
        cat['cy'] = YARD_STAND_Y - bounce * 0.9

        for who in (dog, cat):
            dist = abs(who['cx'] - HEDGE_X)
            hop = max(0.0, 1 - dist / 130) ** 2
            who['cy'] -= hop * 95 * who['scale']
            who['squash'] = lerp(1.0, 1.2, hop)
            if hop > 0.05:
                draw_dust_cloud(draw, who['cx'], YARD_STAND_Y + 20, t)

        title_alpha = ease_out_back(clamp01((t - 0.1) / 0.7))

    elif t < T_HEADIN[1]:
        lt = scene_t(t, *T_HEADIN)
        e = ease_in_out(lt)
        dog['cx'] = lerp(dog.get('cx', 700), SHORT_WIDTH + 200, e)
        cat['cx'] = lerp(cat.get('cx', 600), SHORT_WIDTH + 260, e)
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
        dog['cx'] = lerp(-150, RUG_CX - 60, e)
        cat['cx'] = lerp(-260, RUG_CX + 140, e)
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
        base_dog_x, base_cat_x = RUG_CX - 60, RUG_CX + 140

        if lt < 0.3:
            e = ease_in_out(clamp01(lt / 0.3))
            dog['cx'] = lerp(base_dog_x, RUG_CX - 30, e)
            cat['cx'] = base_cat_x
            cat['facing'] = -1
            dog['leg_phase'] = t * 16
            dog['tail_wag'] = t * 12
            dog['mouth_open'] = 0.2 + 0.1 * math.sin(t * 6)
            bowl_fill = 1.0
        elif lt < 0.62:
            e = clamp01((lt - 0.3) / 0.32)
            dog['cx'] = RUG_CX - 30
            cat['cx'] = lerp(base_cat_x, RUG_CX + 65, ease_in_out(e))
            cat['facing'] = -1
            cat['leg_phase'] = t * 10
            cat['tail_flick'] = t * 14
            bowl_fill = lerp(1.0, 0.55, e)
            dog['tail_wag'] = t * 14
        else:
            e = clamp01((lt - 0.62) / 0.38)
            cat['cx'] = lerp(RUG_CX + 65, RUG_CX + 140, ease_in_out(e))
            dog['cx'] = lerp(RUG_CX - 30, RUG_CX - 60, ease_in_out(e))
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
        e = ease_in_out(min(1, lt * 2.2))
        dog['cx'] = lerp(RUG_CX - 60, RUG_CX - 95, e)
        cat['cx'] = lerp(RUG_CX + 140, RUG_CX + 155, e)
        dog['facing'] = 1
        cat['facing'] = -1
        dog['cy'] = STAND_Y
        cat['cy'] = STAND_Y
        dog['tilt'] = lerp(0, 10, e)
        cat['tilt'] = lerp(0, -10, e)
        dog['closed_eyes'] = lt > 0.3
        cat['closed_eyes'] = lt > 0.3
        dog['tail_wag'] = t * 8
        cat['tail_flick'] = t * 6

    else:
        lt = scene_t(t, *T_END)
        show_bowl = True
        bowl_fill = 0.28
        dog['cx'] = RUG_CX - 95
        cat['cx'] = RUG_CX + 155
        dog['facing'] = 1
        cat['facing'] = -1
        dog['cy'] = STAND_Y
        cat['cy'] = STAND_Y
        dog['tail_wag'] = t * 10
        cat['tail_flick'] = t * 8
        fade_warm = ease_in_out(clamp01((lt - 0.35) / 0.35))
        end_alpha = ease_out_back(clamp01((lt - 0.45) / 0.35))

    # --- compose ------------------------------------------------------
    draw_dog(draw, dog['cx'], dog['cy'], scale=dog['scale'], facing=dog['facing'],
              leg_phase=dog['leg_phase'], mouth_open=dog['mouth_open'], tilt=dog['tilt'],
              tail_wag=dog['tail_wag'], dazed=dog['dazed'], panting=dog['panting'],
              stretch=dog['stretch'], squash=dog['squash'], closed_eyes=dog['closed_eyes'], **DOG_KW)

    draw_cat(draw, cat['cx'], cat['cy'], scale=cat['scale'], facing=cat['facing'],
              leg_phase=cat['leg_phase'], tilt=cat['tilt'], tail_flick=cat['tail_flick'],
              dazed=cat['dazed'], panting=cat['panting'], stretch=cat['stretch'],
              smug=cat['smug'], squash=cat['squash'], closed_eyes=cat['closed_eyes'], **CAT_KW)

    if show_bowl:
        draw_food_bowl(draw, BOWL_X, BOWL_Y, scale=1.3, fill_level=bowl_fill)

    # --- text overlays --------------------------------------------------
    if title_alpha > 0.02:
        bounce_y = 240 - 24 * math.sin(t * 4)
        text_center(draw, SHORT_WIDTH / 2, bounce_y, "DOG & CAT", title_font, fill=(255, 255, 255),
                    stroke_fill=INK, stroke_width=7)
        text_center(draw, SHORT_WIDTH / 2, bounce_y + 84, "BEST FRIENDS", sub_font, fill=(120, 200, 255),
                    stroke_fill=INK, stroke_width=6)

    if fade_warm > 0.01:
        warm = Image.new("RGB", (SHORT_WIDTH, SHORT_HEIGHT), (255, 241, 214))
        img = Image.blend(img, warm, clamp01(fade_warm))

    if end_alpha > 0.02:
        end_font = font(TITLE_FONT_PATH, 78)
        draw2 = ImageDraw.Draw(img, "RGBA")
        text_center(draw2, SHORT_WIDTH / 2, SHORT_HEIGHT / 2 - 100, "BEST FRIENDS", end_font, fill=(255, 255, 255),
                    stroke_fill=INK, stroke_width=7)
        text_center(draw2, SHORT_WIDTH / 2, SHORT_HEIGHT / 2 - 10, "FOREVER", end_font, fill=(255, 255, 255),
                    stroke_fill=INK, stroke_width=7)
        text_center(draw2, SHORT_WIDTH / 2, SHORT_HEIGHT / 2 + 90, "Subscribe for more!", sub_font, fill=(120, 200, 255),
                    stroke_fill=INK, stroke_width=6)
        for side in (-1, 1):
            draw_paw_print(draw2, SHORT_WIDTH / 2 + side * 210, SHORT_HEIGHT / 2 + 90, r=18)

    return img


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/frames_shorts"
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
