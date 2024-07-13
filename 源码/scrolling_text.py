import tkinter as tk
from tkinter import simpledialog, colorchooser

class ScrollingText:
    def __init__(self, root, text, speed, fg_color, bg_color, font_name, font_size):
        self.root = root
        self.text = text
        self.speed = speed
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.font_name = font_name
        self.font_size = font_size

        # 设置无标题栏窗口
        self.root.overrideredirect(False)

        # 创建Label
        self.label = tk.Label(root, text=self.text, fg=self.fg_color, bg=self.bg_color, 
                              font=(self.font_name, self.font_size))
        self.label.pack(expand=True, fill=tk.BOTH)

        self.root.geometry("800x100")
        self.root.configure(bg=self.bg_color)

        self.x_pos = self.root.winfo_width()
        self.root.after(0, self.scroll_text)

        # 绑定鼠标事件以便拖动窗口
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # 创建一个隐藏的边框，用于缩放窗口
        self.root.bind("<ButtonPress-3>", self.start_resize)
        self.root.bind("<B3-Motion>", self.do_resize)

    def scroll_text(self):
        self.x_pos -= 2
        if self.x_pos < -self.label.winfo_width():
            self.x_pos = self.root.winfo_width()
        
        self.label.place(x=self.x_pos, y=self.root.winfo_height()//2 - self.label.winfo_height()//2)
        self.root.after(self.speed, self.scroll_text)

    def start_move(self, event):
        self._drag_data = {'x': event.x, 'y': event.y}

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self._drag_data['x']
        y = self.root.winfo_y() + event.y - self._drag_data['y']
        self.root.geometry(f"+{x}+{y}")

    def start_resize(self, event):
        self._resize_data = {'x': event.x, 'y': event.y, 'width': self.root.winfo_width(), 'height': self.root.winfo_height()}

    def do_resize(self, event):
        delta_x = event.x - self._resize_data['x']
        delta_y = event.y - self._resize_data['y']
        new_width = self._resize_data['width'] + delta_x
        new_height = self._resize_data['height'] + delta_y
        self.root.geometry(f"{new_width}x{new_height}")

def start_scrolling_text():
    root = tk.Toplevel()

    text = text_entry.get()
    speed = int(speed_entry.get())
    fg_color = fg_color_entry.get()
    bg_color = bg_color_entry.get()
    font_name = font_name_entry.get()
    font_size = int(font_size_entry.get())

    scrolling_text = ScrollingText(root, text, speed, fg_color, bg_color, font_name, font_size)
    root.mainloop()

def pick_color(entry):
    color_code = colorchooser.askcolor(title="Choose color")[1]
    entry.delete(0, tk.END)
    entry.insert(0, color_code)

app = tk.Tk()
app.title("Scrolling Text Configuration")

tk.Label(app, text="字幕内容:").grid(row=0, column=0)
text_entry = tk.Entry(app)
text_entry.grid(row=0, column=1)

tk.Label(app, text="滚动速度(毫秒):").grid(row=1, column=0)
speed_entry = tk.Entry(app)
speed_entry.grid(row=1, column=1)

tk.Label(app, text="字体颜色:").grid(row=2, column=0)
fg_color_entry = tk.Entry(app)
fg_color_entry.grid(row=2, column=1)
tk.Button(app, text="选择颜色", command=lambda: pick_color(fg_color_entry)).grid(row=2, column=2)

tk.Label(app, text="背景颜色:").grid(row=3, column=0)
bg_color_entry = tk.Entry(app)
bg_color_entry.grid(row=3, column=1)
tk.Button(app, text="选择颜色", command=lambda: pick_color(bg_color_entry)).grid(row=3, column=2)

tk.Label(app, text="字体名称:").grid(row=4, column=0)
font_name_entry = tk.Entry(app)
font_name_entry.grid(row=4, column=1)

tk.Label(app, text="字体大小:").grid(row=5, column=0)
font_size_entry = tk.Entry(app)
font_size_entry.grid(row=5, column=1)

tk.Button(app, text="启动滚动字幕", command=start_scrolling_text).grid(row=6, columnspan=3)

app.mainloop()
