#!/usr/bin/env python3
"""Generates the YouTube thumbnail (1280x720) for "Dog & Cat: Best
Friends" from a warm frame of the animation, with bold overlay text.

Usage: python3 thumbnail_bff.py <output_path>
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

from anim_common import WIDTH, HEIGHT, font, text_center, TITLE_FONT_PATH, INK
from render_frames_bff import get_frame


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "assets/thumbnail_bff.png"
    img = get_frame(19.5).convert("RGB")  # happy bowl-sharing moment

    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    vd = ImageDraw.Draw(vignette)
    vd.rectangle([0, 0, WIDTH, 130], fill=100)
    vignette = vignette.filter(ImageFilter.GaussianBlur(40))
    dark = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    img = Image.composite(dark, img, vignette)

    draw = ImageDraw.Draw(img, "RGBA")
    big = font(TITLE_FONT_PATH, 96)
    text_center(draw, WIDTH / 2, 78, "BEST FRIENDS!", big, fill=(255, 255, 255),
                stroke_fill=INK, stroke_width=10)

    img.save(out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
