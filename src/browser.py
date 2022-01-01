import http_req
import layout
import font
import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

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
        
        self.layout = layout.Layout()
    
    def load(self, url):
        headers, body = http_req.Request(url).request()
        display_list = self.Layout(body).get_layout()
        self.draw(display_list)
        
    def draw(self, display_list):
        self.canvas.delete("all")
        for x, y, c in display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=font.times)
 
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
