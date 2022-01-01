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
        self.weight = "normal"
        self.style = "roman"
        self.size = 16
        
        self.cursor_x = HSTEP
        self.cursor_y = VSTEP
        
        self.tokens = self.lex(body)
        self.display_list = []
        for tok in self.tokens:
            self.token(tok)
            
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
        
    def token(self, tok):
        if isinstance(tok, Text):
            self.text(tok)
        elif tok.tag == "i":
            self.style = "italic"
        elif tok.tag == "/i":
            self.style = "roman"
        elif tok.tag == "b":
            self.weight = "bold"
        elif tok.tag == "/b":
            self.weight = "normal"
    
    def text(self, tok):
        times_font = build_times_font(self.weight, self.style, self.size)
        for word in tok.text.split():
            w = times_font.measure(word)
            if self.cursor_x + w > WIDTH - HSTEP:
                self.cursor_y += times_font.metrics("linespace") * 1.25
                self.cursor_x = HSTEP
            self.display_list.append((self.cursor_x, self.cursor_y, word, times_font))
            self.cursor_x += w + times_font.measure(" ")
