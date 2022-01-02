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

def is_open_title(tok):
    return tok.tag.startswith("h1") or tok.tag.startswith("h2") or tok.tag.startswith("h3") or tok.tag.startswith("h4") or tok.tag.startswith("h5") or tok.tag.startswith("h6") or tok.tag.startswith("strong")
    
def is_closing_title(tok):
    return tok.tag == "/h1" or tok.tag == "/h2" or tok.tag == "/h3" or tok.tag == "/h4" or tok.tag == "/h5" or tok.tag == "/h6" or tok.tag == "/strong"

