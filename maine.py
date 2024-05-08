import tkinter as tk
from PIL import Image, ImageDraw

root = tk.Tk()
root.title("Графический редактор")


canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

draw_color = "black"


def draw(event):
    x1, y1 = event.x, event.y
    x2, y2 = event.x, event.y
    canvas.create_line(x1, y1, x2, y2, fill=draw_color, width=3)


canvas.bind("<B1-Motion>", draw)

def change_color(new_color):
    global draw_color
    draw_color = new_color


toolbar = tk.Frame(root, relief=tk.RAISED, bd=2)
toolbar.pack(side=tk.TOP, fill=tk.X)


colors = ["red", "green", "blue", "black"]
for color in colors:
    color_button = tk.Button(toolbar, bg=color, width=3, height=1, command=lambda c=color: change_color(c))
    color_button.pack(side=tk.LEFT)
from tkinter import filedialog


def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        canvas_image = canvas.postscript(colormode="color")
        img = Image.open(io.BytesIO(canvas_image.encode("utf-8")))
        img.save(file_path)


def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.resize((canvas_width, canvas_height), Image.ANTIALIAS)
        canvas_image = ImageDraw.Draw(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


file_menu = tk.Menu(menu_bar)
file_menu.add_command(label="Сохранить", command=save_image)
file_menu.add_command(label="Открыть", command=open_image)
menu_bar.add_cascade(label="Файл", menu=file_menu)
root.mainloop()
