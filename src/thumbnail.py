#!/usr/bin/env python3
"""Generates a YouTube thumbnail (1280x720) from a dramatic frame of the
animation, with bold overlay text for click-through appeal.

Usage: python3 thumbnail.py <output_path>
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

from anim_common import WIDTH, HEIGHT, font, text_center, TITLE_FONT_PATH, INK
from render_frames import get_frame


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "assets/thumbnail.png"
    img = get_frame(13.0).convert("RGB")  # peak tug-of-war moment

    # subtle vignette for contrast
    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    vd = ImageDraw.Draw(vignette)
    vd.rectangle([0, 0, WIDTH, 130], fill=110)
    vignette = vignette.filter(ImageFilter.GaussianBlur(40))
    dark = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    img = Image.composite(dark, img, vignette)

    draw = ImageDraw.Draw(img, "RGBA")
    big = font(TITLE_FONT_PATH, 108)
    text_center(draw, WIDTH / 2, 78, "FUNNY FIGHTS!", big, fill=(255, 221, 74),
                stroke_fill=INK, stroke_width=10)

    img.save(out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
