import http_req
import layout
import tkinter
from utils.font import build_times_font
from utils.constants import WIDTH, HEIGHT, HSTEP, VSTEP, SCROLL_STEP

class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
          self.window,
          bg='white',
          width=WIDTH,
          height=HEIGHT
        )
        self.canvas.pack()
        
        self.scroll = 0
        self.focus = None
        self.address_bar = ""
        self.address_bar_font = build_times_font("normal", "roman", 16)
        
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.on_mousewheel)
        self.window.bind("<Button-1>", self.handle_click)
        self.window.bind("<Key>", self.handle_key)
        self.window.bind("<BackSpace>", self.handle_delete)
        self.window.bind("<Delete>", self.handle_delete)
        self.window.bind("<Return>", self.handle_return)
        
    def is_in_address_bar(self, e):
        return e.y < 100 and 50 <= e.x < WIDTH - 10 and 40 <= e.y < 90
    
    def handle_return(self, e):
        if self.focus == "address bar":
            print(self.address_bar)
            self.load(self.address_bar)
            self.focus = None
            self.draw()
    def handle_delete(self, e):
        if len(self.address_bar) > 0:
            self.address_bar = self.address_bar[:-1]
            self.draw()
            
    def handle_click(self, e):
        self.focus = None
        if self.is_in_address_bar(e):
            self.focus = "address bar"
            self.address_bar = ""
        self.draw()
        
    def handle_key(self, e):
        if len(e.char) == 0: return
        if not (0x20 <= ord(e.char) < 0x7f): return

        if self.focus == "address bar":
            self.address_bar += e.char
            self.draw()
    
    def load(self, url):
        headers, body = http_req.Request(url).request()
        self.display_list = layout.Layout(body).display_list
        self.draw()
        
    def build_browser_template(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, 100, fill="white", outline="black")
        self.canvas.create_rectangle(40, 50, WIDTH - 10, 90, outline="black", width=1)
    
    def draw(self):
        self.build_browser_template()
        if self.focus == "address bar":
            self.canvas.create_text(55, 55, anchor='nw', text=self.address_bar,font=self.address_bar_font, fill="black")
            w = self.address_bar_font.measure(self.address_bar)
            self.canvas.create_line(55 + w, 55, 55 + w, 85, fill="black")
        else:
            for x, y, word, times_font in self.display_list:
                if y > self.scroll + HEIGHT: continue
                if y + VSTEP < self.scroll: continue
                self.canvas.create_text(x, y - self.scroll + 115, text=word, font=times_font, anchor="nw")
            
            
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
