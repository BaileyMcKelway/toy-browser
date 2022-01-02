import tkinter.font

FONTS_CACHE = {}

def build_times_font(weight, style, size):
    key = (weight, style, size)
    if key not in FONTS_CACHE:
        font = tkinter.font.Font(
            family="Times",
            size=size,
            weight=weight,
            slant=style,
        )
        FONTS_CACHE[key] = font
    return FONTS_CACHE[key]
  