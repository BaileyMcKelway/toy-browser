import http_req
import layout
import tkinter
from utils.constants import WIDTH, HEIGHT, HSTEP, VSTEP, SCROLL_STEP

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
          self.window,
          width=WIDTH,
          height=HEIGHT
        )
        self.canvas.pack()
        
        self.scroll = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.on_mousewheel)
    
    def load(self, url):
        headers, body = http_req.Request(url).request()
        display_list = layout.Layout(body).get_layout()
        self.draw(display_list)
        
    def draw(self, display_list):
        self.canvas.delete("all")
        for x, y, word, times_font in display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=word, font=times_font)
 
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
    Browser().load(sys.argv[1])
    tkinter.mainloop()
