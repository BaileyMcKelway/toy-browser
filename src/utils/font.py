import tkinter.font

def build_times_font(weight, style, size):
    return tkinter.font.Font(
            family="Times",
            size=size,
            weight=weight,
            slant=style,
    )
  