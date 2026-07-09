#!/usr/bin/env python3
"""Renders the full 'Dog & Cat: Funny Fights' cartoon as a PNG sequence.

Usage: python3 render_frames.py <output_dir>
"""
import math
import os
import sys

from anim_common import (
    WIDTH, HEIGHT, FPS, new_canvas, draw_background, draw_plant_pot,
    draw_stars, draw_speed_lines, draw_dust_cloud, draw_squeak, draw_paw_print,
    text_center, font, TITLE_FONT_PATH, BODY_FONT_PATH,
    ease_out_back, ease_in_out, ease_out_bounce, scene_t, lerp, clamp01,
    INK, WHITE, BLACK,
)
from characters import draw_dog, draw_cat, draw_toy

# --- timeline (seconds) ------------------------------------------------
T_TITLE = (0.0, 3.0)
T_STANDOFF = (3.0, 6.0)
T_DASH = (6.0, 11.0)
T_TUG = (11.0, 17.0)
T_SNAP = (17.0, 20.0)
T_DAZE = (20.0, 24.0)
T_CHASE = (24.0, 30.0)
T_DRAW = (30.0, 35.0)
T_PUNCH = (35.0, 40.0)
TOTAL_DURATION = 40.0

RUG_CX, RUG_CY = 666, 630
STAND_Y = 630
COUCH_X, COUCH_Y = 1030, 630
TABLE_X, TABLE_Y = 230, 630

TITLE_FONT = None
SUB_FONT = None
BODY_FONT = None


def _fonts():
    global TITLE_FONT, SUB_FONT, BODY_FONT
    if TITLE_FONT is None:
        TITLE_FONT = font(TITLE_FONT_PATH, 92)
        SUB_FONT = font(TITLE_FONT_PATH, 40)
        BODY_FONT = font(BODY_FONT_PATH, 30)
    return TITLE_FONT, SUB_FONT, BODY_FONT


def get_frame(t):
    title_font, sub_font, body_font = _fonts()
    img, draw = new_canvas()

    shake = (0, 0)
    if T_SNAP[0] <= t < T_SNAP[0] + 0.5 or T_SNAP[0] + 1.7 <= t < T_SNAP[0] + 2.2:
        shake = (math.sin(t * 90) * 6, math.cos(t * 70) * 4)

    tx, ty = draw_background(draw, shake=shake)  # plant pot anchor near table

    dog = dict(cx=-200, cy=STAND_Y, scale=1.3, facing=1, leg_phase=0, mouth_open=0,
               tilt=0, tail_wag=0, dazed=False, panting=False, stretch=0)
    cat = dict(cx=RUG_CX + 70, cy=STAND_Y, scale=1.0, facing=-1, leg_phase=0, tilt=0,
               tail_flick=0, dazed=False, panting=False, stretch=0, smug=True)
    toy = None  # (x1,y1,x2,y2) or None
    plant_on_table = True
    plant_tilt = 0.0
    plant_on_dog_head = False
    plant_on_cat_head = False
    extra_fx = []
    title_alpha = 0.0
    end_alpha = 0.0
    fade_black = 0.0

    if t < T_TITLE[1]:
        lt = scene_t(t, *T_TITLE)
        # Rex & Whiskers peek in from the corners while the title bounces.
        dog['cx'] = lerp(-150, 250, ease_in_out(min(1, lt * 1.6)))
        dog['leg_phase'] = t * 6
        cat['cx'] = lerp(RUG_CX + 320, RUG_CX + 40, ease_in_out(min(1, lt * 1.6)))
        cat['tail_flick'] = t * 3
        title_alpha = ease_out_back(clamp01((t - 0.2) / 1.0))

    elif t < T_STANDOFF[1]:
        lt = scene_t(t, *T_STANDOFF)
        dog['cx'] = lerp(250, 470, ease_out_bounce(lt))
        dog['leg_phase'] = t * 9 if lt < 0.7 else 0
        dog['mouth_open'] = 0.25 + 0.15 * math.sin(t * 6)
        cat['cx'] = RUG_CX + 40
        cat['tail_flick'] = t * 4
        cat['smug'] = True
        toy = (RUG_CX - 10, STAND_Y + 10, RUG_CX + 30, STAND_Y + 10)

    elif t < T_DASH[1]:
        lt = scene_t(t, *T_DASH)
        e = ease_in_out(lt)
        dog['cx'] = lerp(470, 560, e)
        dog['leg_phase'] = t * 24
        dog['mouth_open'] = 0.5
        cat['cx'] = lerp(RUG_CX + 40, 780, e)
        cat['leg_phase'] = t * 22
        cat['smug'] = False
        if lt < 0.85:
            draw_dust_cloud(draw, dog['cx'] - 60, STAND_Y + 40, t)
            draw_speed_lines(draw, dog['cx'] - 70, STAND_Y - 10, 1)
            draw_dust_cloud(draw, cat['cx'] + 60, STAND_Y + 40, t)
            draw_speed_lines(draw, cat['cx'] + 70, STAND_Y - 10, -1)
        toy = (dog['cx'] + 60, STAND_Y - 30, cat['cx'] - 60, STAND_Y - 30)

    elif t < T_TUG[1]:
        lt = scene_t(t, *T_TUG)
        wobble = math.sin(lt * 2 * math.pi * 3.2) * 25
        dog['cx'] = 560 + wobble
        cat['cx'] = 780 - wobble
        dog['leg_phase'] = t * 30
        cat['leg_phase'] = t * 28
        dog['mouth_open'] = 0.7
        dog['stretch'] = 0.55
        cat['stretch'] = 0.55
        dog['tail_wag'] = t * 10
        cat['tail_flick'] = t * 2
        toy = (dog['cx'] + 60, STAND_Y - 30, cat['cx'] - 60, STAND_Y - 30)
        if int(t * 4) % 2 == 0:
            mx = (toy[0] + toy[2]) / 2
            my = min(toy[1], toy[3])
            draw_squeak(draw, mx - 28, my, t)

    elif t < T_SNAP[1]:
        lt = scene_t(t, *T_SNAP)
        e = ease_out_back(min(1, lt * 1.6))
        dog['cx'] = lerp(560, COUCH_X - 60, e)
        dog['cy'] = lerp(STAND_Y, STAND_Y - 40, math.sin(min(1, lt * 2) * math.pi))
        dog['tilt'] = lerp(0, 8, e)
        dog['leg_phase'] = 0
        cat['cx'] = lerp(780, TABLE_X + 60, e)
        cat['cy'] = lerp(STAND_Y, STAND_Y - 30, math.sin(min(1, lt * 2) * math.pi))
        cat['tilt'] = lerp(0, -8, e)
        cat['leg_phase'] = 0
        if lt < 0.15:
            toy = (620, STAND_Y - 30, 720, STAND_Y - 30)
        else:
            toy = None
        plant_tilt = lerp(0, -35, ease_in_out(clamp01((lt - 0.4) / 0.5)))

    elif t < T_DAZE[1]:
        lt = scene_t(t, *T_DAZE)
        dog['cx'] = COUCH_X - 60
        dog['tail_wag'] = t * 8
        dog['dazed'] = True
        cat['cx'] = TABLE_X + 60
        cat['dazed'] = True
        plant_on_cat_head = True
        plant_on_table = False
        extra_fx.append(('stars_dog', dog['cx'], STAND_Y - 90, t))
        extra_fx.append(('stars_cat', cat['cx'], STAND_Y - 80, t))

    elif t < T_CHASE[1]:
        lt = scene_t(t, *T_CHASE)
        lane_lo, lane_hi = 300, 980
        phase = lt * 2 * math.pi * 3
        pos = (math.sin(phase - math.pi / 2) + 1) / 2  # 0..1..0 sweeps
        lead_x = lerp(lane_lo, lane_hi, pos)
        vel = math.cos(phase - math.pi / 2)
        facing = 1 if vel >= 0 else -1
        dog['cx'] = lead_x
        dog['facing'] = facing
        dog['leg_phase'] = t * 26
        dog['tail_wag'] = t * 14
        cat['cx'] = lead_x - facing * 100
        cat['facing'] = facing
        cat['leg_phase'] = t * 26
        cat['tail_flick'] = t * 10
        cat['smug'] = False
        draw_dust_cloud(draw, dog['cx'] - facing * 50, STAND_Y + 40, t)
        draw_speed_lines(draw, dog['cx'] - facing * 55, STAND_Y - 10, facing)
        draw_speed_lines(draw, cat['cx'] - facing * 55, STAND_Y - 10, facing)

    elif t < T_DRAW[1]:
        lt = scene_t(t, *T_DRAW)
        e = ease_out_bounce(min(1, lt * 2.2))
        dog['cx'] = lerp(dog.get('cx', 560), 560, 1) if lt > 0 else 560
        dog['cx'] = 560
        cat['cx'] = 780
        pant = 0.4 + 0.35 * abs(math.sin(t * 5))
        dog['mouth_open'] = pant
        cat_mouth = pant
        dog['panting'] = True
        cat['panting'] = True
        dog['leg_phase'] = 0
        cat['leg_phase'] = 0
        toy = (640, STAND_Y + 20, 700, STAND_Y + 20)

    else:
        lt = scene_t(t, *T_PUNCH)
        dog['cx'] = 560
        cat['cx'] = 780
        dog['panting'] = True
        cat['panting'] = True
        dog['tilt'] = lerp(0, 14, ease_in_out(min(1, lt * 3)))
        cat['tilt'] = lerp(0, -14, ease_in_out(min(1, lt * 3)))
        toy = (640, STAND_Y + 20, 700, STAND_Y + 20)
        fade_black = ease_in_out(clamp01((lt - 0.55) / 0.35))
        end_alpha = ease_out_back(clamp01((lt - 0.65) / 0.35))

    # --- compose: table/plant (back), characters, toy + pot on top ------
    if plant_on_table:
        draw_plant_pot(draw, tx + shake[0], ty + shake[1], tilt=plant_tilt)

    dog_cy = dog['cy'] if 'cy' in dog else STAND_Y
    cat_cy = cat['cy'] if 'cy' in cat else STAND_Y

    draw_dog(draw, dog['cx'] + shake[0], dog_cy + shake[1],
             scale=dog.get('scale', 1.0), facing=dog['facing'], leg_phase=dog['leg_phase'],
             mouth_open=dog['mouth_open'], tilt=dog['tilt'], tail_wag=dog['tail_wag'],
             dazed=dog['dazed'], panting=dog['panting'], stretch=dog['stretch'])

    draw_cat(draw, cat['cx'] + shake[0], cat_cy + shake[1],
             scale=cat.get('scale', 1.0), facing=cat['facing'], leg_phase=cat['leg_phase'],
             tilt=cat['tilt'], tail_flick=cat['tail_flick'], dazed=cat['dazed'],
             panting=cat['panting'], stretch=cat['stretch'], smug=cat['smug'])

    if toy is not None:
        x1, y1, x2, y2 = toy
        draw_toy(draw, x1 + shake[0], y1 + shake[1], x2 + shake[0], y2 + shake[1])

    if plant_on_dog_head:
        head_x = dog['cx'] + dog['facing'] * 63 * dog.get('scale', 1.0)
        draw_plant_pot(draw, head_x + shake[0], dog_cy - 108 + shake[1], tilt=8, on_head=True, scale=0.85)

    if plant_on_cat_head:
        head_x = cat['cx'] + cat['facing'] * 55 * cat.get('scale', 1.0)
        draw_plant_pot(draw, head_x + shake[0], cat_cy - 90 + shake[1], tilt=6, on_head=True, scale=0.75)

    for fx in extra_fx:
        if fx[0] == 'stars_dog':
            draw_stars(draw, fx[1], fx[2], fx[3])
        elif fx[0] == 'stars_cat':
            draw_stars(draw, fx[1], fx[2], fx[3])

    # --- text overlays ----------------------------------------------------
    if title_alpha > 0.02:
        scale = clamp01(title_alpha)
        bounce_y = 150 - 20 * math.sin(t * 4)
        text_center(draw, WIDTH / 2, bounce_y, "DOG & CAT", title_font, fill=(255, 255, 255),
                    stroke_fill=INK, stroke_width=6)
        text_center(draw, WIDTH / 2, bounce_y + 74, "FUNNY FIGHTS", sub_font, fill=(255, 221, 74),
                    stroke_fill=INK, stroke_width=5)

    if fade_black > 0.01:
        from PIL import Image
        black = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        img = _blend(img, black, fade_black)
        draw = None

    if end_alpha > 0.02:
        draw2 = __import__('PIL.ImageDraw', fromlist=['ImageDraw']).Draw(img, "RGBA")
        text_center(draw2, WIDTH / 2, HEIGHT / 2 - 40, "SUBSCRIBE FOR MORE", title_font, fill=(255, 255, 255),
                    stroke_fill=INK, stroke_width=6)
        text_center(draw2, WIDTH / 2, HEIGHT / 2 + 40, "FUNNY FIGHTS!", sub_font, fill=(255, 221, 74),
                    stroke_fill=INK, stroke_width=5)
        for side in (-1, 1):
            draw_paw_print(draw2, WIDTH / 2 + side * 210, HEIGHT / 2 + 40, r=16)

    return img


def _blend(img_a, img_b, t):
    from PIL import Image
    return Image.blend(img_a, img_b, clamp01(t))


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "build/frames"
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
