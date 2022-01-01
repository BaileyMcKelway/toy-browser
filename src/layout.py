import font

class Text:
    def __init__(self, text):
        self.text = text
        
class Tag:
    def __init__(self, tag):
        self.tag = tag

class Layout:
    def __init__(self, body):
        self.body = body
      
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
                for word in tok.text.split():
                    w = font.times.measure(word)
                    if cursor_x + w > WIDTH - HSTEP:
                        cursor_y += font.times.metrics("linespace") * 1.25
                        cursor_x = HSTEP
                    display_list.append((cursor_x, cursor_y, word))
                    cursor_x += w + font.times.measure(" ")
            elif tok.tag == "i":
                style = "italic"
            elif tok.tag == "/i":
                style = "roman"
            elif tok.tag == "b":
                weight = "bold"
            elif tok.tag == "/b":
                weight = "normal"
        return display_list
    
    def get_layout(self):
        tokens = self.lex(self.body)
        return self.layout(tokens)
