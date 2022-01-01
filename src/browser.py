import tkinter
import http_req

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.on_mousewheel)
          
    def lex(self, body):
        text = ""
        in_angle = False
        for c in body:
            if c == "<":
                in_angle = True
            elif c == ">":
                in_angle = False
            elif not in_angle:
                text += c
        return text
    
    def layout(self, text):
        display_list = []
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            display_list.append((cursor_x, cursor_y, c))
            cursor_x += HSTEP
            if cursor_x >= WIDTH - HSTEP:
                cursor_y += VSTEP
                cursor_x = HSTEP
        return display_list
    
    def load(self, url):
        headers, body = http_req.Request(url).request()
        self.display_list = self.layout(self.lex(body))
        self.draw()
        
    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)
            
    def scrollup(self, e):
      if self.scroll - SCROLL_STEP >= 0:
        self.scroll -= SCROLL_STEP
        self.draw()
    
    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()
    
    def on_mousewheel(self, e):
        if e.delta < 0:
            self.scrolldown(e)
        else:
            self.scrollup(e)
        



if __name__ == "__main__":
    import sys
    print(sys.argv[1])
    Browser().load(sys.argv[1])
    tkinter.mainloop()
