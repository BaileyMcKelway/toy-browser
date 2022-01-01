from utils.font import build_times_font
from utils.constants import WIDTH, HEIGHT, HSTEP, VSTEP, SCROLL_STEP

class Text:
    def __init__(self, text):
        self.text = text
        
class Tag:
    def __init__(self, tag):
        self.tag = tag

class Layout:
    def __init__(self, body):
        self.body = body
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
      
    def lex(self, body):
        out = []
        text = ""
        in_tag = False
        for c in body:
            if c == "<":
                in_tag = True
                if text: out.append(Text(text))
                text = ""
            elif c == ">":
                in_tag = False
                out.append(Tag(text))
                text = ""
            else:
                text += c
        if not in_tag and text:
            out.append(Text(text))
        return out
        
    def layout(self, tokens):
        display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP
        for tok in tokens:
            if isinstance(tok, Text):
                times_font = build_times_font(self.weight, self.style, self.size)
                for word in tok.text.split():
                    w = times_font.measure(word)
                    if cursor_x + w > WIDTH - HSTEP:
                        cursor_y += times_font.metrics("linespace") * 1.25
                        cursor_x = HSTEP
                    display_list.append((cursor_x, cursor_y, word, times_font))
                    cursor_x += w + times_font.measure(" ")
            elif tok.tag == "i":
                self.style = "italic"
            elif tok.tag == "/i":
                self.style = "roman"
            elif tok.tag == "b":
                self.weight = "bold"
            elif tok.tag == "/b":
                self.weight = "normal"
        return display_list
    
    def get_layout(self):
        tokens = self.lex(self.body)
        return self.layout(tokens)
