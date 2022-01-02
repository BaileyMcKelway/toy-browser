from utils.font import build_times_font, is_open_title, is_closing_title
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
        
        self.line = []
        self.flush()
        
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
                if text.startswith('body'):
                    is_body = True
                    out = []
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
        elif tok.tag == "br":
            self.flush()
        elif tok.tag == "/p":
            self.flush()
            self.cursor_y += VSTEP
        elif is_open_title(tok):
            self.flush()
            self.size += 4
        elif is_closing_title(tok):
            self.flush()
            self.size -= 4
        
    def text(self, tok):
        self.times_font = build_times_font(self.weight, self.style, self.size)
        for word in tok.text.split():
            w = self.times_font.measure(word)
            if self.cursor_x + w > WIDTH - HSTEP:
                self.flush()
            self.line.append((self.cursor_x, word, self.times_font))
            self.cursor_x += w + self.times_font.measure(" ")
            
    def flush(self):
        if not self.line: return
        metrics = [self.times_font.metrics() for x, word, font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, times_font in self.line:
            y = baseline - times_font.metrics("ascent")
            self.display_list.append((x, y, word, times_font))
        self.cursor_x = HSTEP
        self.line = []
        max_descent = max([metric["descent"] for metric in metrics])
        self.cursor_y = baseline + 1.25 * max_descent
        
