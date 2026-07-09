#!/usr/bin/env python3
"""Generates title/end-card still images for the real-footage edit, in
the same visual language (fonts, colors, paw-print icon) as the
animated videos, so the channel look stays consistent across both.

Usage: python3 realfootage_cards.py <end_card_output.png>
"""
import sys

from PIL import Image

from anim_common import (
    font, text_center, draw_paw_print, TITLE_FONT_PATH, BODY_FONT_PATH, INK,
)

W, H = 1080, 1920
WARM_BG = (255, 241, 214)
BLUE = (120, 200, 255)


def make_end_card(path):
    img = Image.new("RGB", (W, H), WARM_BG)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img, "RGBA")

    title_font = font(TITLE_FONT_PATH, 92)
    sub_font = font(TITLE_FONT_PATH, 44)

    text_center(draw, W / 2, H / 2 - 140, "BEST FRIENDS", title_font, fill=(255, 255, 255),
                stroke_fill=INK, stroke_width=8)
    text_center(draw, W / 2, H / 2 - 40, "ON A WALK", title_font, fill=(255, 255, 255),
                stroke_fill=INK, stroke_width=8)
    text_center(draw, W / 2, H / 2 + 60, "Subscribe for more!", sub_font, fill=BLUE,
                stroke_fill=INK, stroke_width=6)
    for side in (-1, 1):
        draw_paw_print(draw, W / 2 + side * 210, H / 2 + 60, r=18)

    img.save(path)
    print(f"wrote {path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "build/realfootage/end_card.png"
    make_end_card(out)
