#!/usr/bin/env python3
"""Generates the end-card still image for the real-footage edit. Uses a
soft-shadow caption style (not the animated videos' thick comic
outline) since that reads as cartoonish over real photography -- and
composites over a blurred/darkened frame from the source footage so the
end card feels like part of the same video rather than a flat slide.

Usage: python3 realfootage_cards.py <end_card_output.png> [background_frame.png]
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

from anim_common import font, text_center_soft, draw_paw_print, TITLE_FONT_PATH, BODY_FONT_PATH

W, H = 1080, 1920
WARM_BG = (60, 66, 54)
BLUE = (150, 210, 255)


def make_end_card(path, bg_frame=None):
    if bg_frame:
        img = Image.open(bg_frame).convert("RGB").resize((W, H))
        img = img.filter(ImageFilter.GaussianBlur(18))
        dark = Image.new("RGB", (W, H), (10, 12, 8))
        img = Image.blend(img, dark, 0.55)
    else:
        img = Image.new("RGB", (W, H), WARM_BG)

    draw = ImageDraw.Draw(img, "RGBA")
    title_font = font(TITLE_FONT_PATH, 80)
    sub_font = font(TITLE_FONT_PATH, 40)

    text_center_soft(draw, W / 2, H / 2 - 90, "Best Friends", title_font, fill=(255, 255, 255))
    text_center_soft(draw, W / 2, H / 2 + 60, "Subscribe for more!", sub_font, fill=BLUE)
    for side in (-1, 1):
        draw_paw_print(draw, W / 2 + side * 200, H / 2 + 60, r=16, color=BLUE)

    img.save(path)
    print(f"wrote {path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "build/realfootage/end_card.png"
    bg = sys.argv[2] if len(sys.argv) > 2 else None
    make_end_card(out, bg)
