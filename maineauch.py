import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageOps, ImageEnhance
import io
from tkinter import simpledialog

root = tk.Tk()
root.title("Графический редактор")
root.geometry("1200x800")  

# Темный режим
def toggle_theme():
    if root.cget('bg') == 'white':
        root.config(bg='#333333')
        canvas.config(bg='#333333')
        toolbar.config(bg='#333333')
        color_frame.config(bg='#333333')
        tool_frame.config(bg='#333333')
    else:
        root.config(bg='white')
        canvas.config(bg='white')
        toolbar.config(bg='white')
        color_frame.config(bg='white')
        tool_frame.config(bg='white')

canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack(pady=20) 

draw_color = "black"
eraser_on = False
eraser_size = 10
brush_size = 3 
original_image = None 

def draw(event):
    if eraser_on:
        canvas.create_rectangle(event.x - eraser_size // 2, event.y - eraser_size // 2, event.x + eraser_size // 2, event.y + eraser_size // 2, outline='white', fill='white', width=0)
    else:
        x1, y1 = event.x - brush_size // 2, event.y - brush_size // 2
        x2, y2 = event.x + brush_size // 2, event.y + brush_size // 2
        canvas.create_line(x1, y1, x2, y2, fill=draw_color, width=brush_size)

canvas.bind("<B1-Motion>", draw)

def change_color(new_color):
    global draw_color
    draw_color = new_color

def toggle_eraser():
    global eraser_on
    eraser_on = not eraser_on

def change_brush_size(new_size):
    global brush_size
    brush_size = new_size

toolbar = tk.Frame(root, relief=tk.RAISED, bd=2)
toolbar.pack(side=tk.TOP, fill=tk.X, pady=5)

color_frame = tk.Frame(toolbar, bg='white')
color_frame.pack(side=tk.LEFT, padx=5)

colors = ["red", "green", "blue", "black"]
for color in colors:
    color_button = tk.Button(color_frame, bg=color, width=3, height=1, relief=tk.RIDGE, bd=2, command=lambda c=color: change_color(c))
    if color == "red":
        color_button.configure(command=lambda: change_color("red"))
    else:
        color_button.configure(command=lambda c=color: change_color(c))
    color_button.pack(side=tk.LEFT, padx=2)

tool_frame = tk.Frame(toolbar, bg='white')
tool_frame.pack(side=tk.LEFT, padx=5)

eraser_button = tk.Button(tool_frame, text="Eraser", relief=tk.RIDGE, bd=2, command=toggle_eraser)
eraser_button.pack(side=tk.LEFT, padx=2)

brush_sizes = [1, 3, 5, 7, 9]
for size in brush_sizes:
    brush_button = tk.Button(tool_frame, text=str(size), width=2, relief=tk.RIDGE, bd=2, command=lambda s=size: change_brush_size(s))
    brush_button.pack(side=tk.LEFT, padx=2)

from tkinter import filedialog

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        canvas_image = canvas.postscript(colormode="color")
        img = Image.open(io.BytesIO(canvas_image.encode("utf-8")))
        img.save(file_path)

def open_image():
    global original_image
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.convert("RGB")  # Конвертация в RGB, если необходимо
        original_image = img.copy()  # Сохранение копии оригинального изображения
        img = img.resize((canvas_width, canvas_height), Image.ANTIALIAS)
        photo_img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)
        canvas.image = photo_img  # Сохранение ссылки на изображение

def clear_canvas():
    canvas.delete("all")
    global original_image
    original_image = None
    
def scale_image(scale_percent):
    if original_image:
        new_width = int(original_image.width * scale_percent / 100)
        new_height = int(original_image.height * scale_percent / 100)
        scaled_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
        photo_img = ImageTk.PhotoImage(scaled_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)
        canvas.image = photo_img  # Сохранение ссылки на изображение

def apply_grayscale():
    if original_image:
        grayscale_image = ImageOps.grayscale(original_image)
        photo_img = ImageTk.PhotoImage(grayscale_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)
        canvas.image = photo_img  # Сохранение ссылки на изображение

def apply_pink_filter():
    if original_image:
        pink_filter = ImageEnhance.Color(original_image).enhance(1.5)
        photo_img = ImageTk.PhotoImage(pink_filter)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)
        canvas.image = photo_img  

def apply_blue_filter():
    if original_image:
        blue_filter = ImageEnhance.Color(original_image).enhance(0.5)
        photo_img = ImageTk.PhotoImage(blue_filter)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)
        canvas.image = photo_img  

def crop_image():
    if original_image:
        crop_window = tk.Toplevel(root)
        crop_window.title("Обрезать изображение")

        crop_canvas = tk.Canvas(crop_window, width=original_image.width, height=original_image.height)
        crop_canvas.pack()
        photo_img = ImageTk.PhotoImage(original_image)
        crop_canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)

        start_x, start_y = None, None

        def start_crop(event):
            nonlocal start_x, start_y
            start_x, start_y = event.x, event.y

        def crop_image_done(event):
            nonlocal start_x, start_y
            end_x, end_y = event.x, event.y
            left = min(start_x, end_x)
            top = min(start_y, end_y)
            right = max(start_x, end_x)
            bottom = max(start_y, end_y)
            cropped_image = original_image.crop((left, top, right, bottom))
            photo_img = ImageTk.PhotoImage(cropped_image)
            canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)
            canvas.image = photo_img  
            crop_window.destroy()

        crop_canvas.bind("<Button-1>", start_crop)
        crop_canvas.bind("<B1-Motion>",
                         lambda event: crop_canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="red"))
        crop_canvas.bind("<ButtonRelease-1>", crop_image_done)

def flip_horizontal():
    if original_image:
        flipped_image = ImageOps.mirror(original_image)
        photo_img = ImageTk.PhotoImage(flipped_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)
        canvas.image = photo_img 

def rotate_image():
    if original_image:
        rotate_window = tk.Toplevel(root)
        rotate_window.title("Повернуть изображение")

        angle_label = tk.Label(rotate_window, text="Введите угол поворота (градусы):")
        angle_label.pack()

        angle_entry = tk.Entry(rotate_window)
        angle_entry.pack()

        def rotate_image_done():
            try:
                angle = int(angle_entry.get())
                rotated_image = original_image.rotate(angle, expand=True)
                photo_img = ImageTk.PhotoImage(rotated_image)
                canvas.create_image(0, 0, anchor=tk.NW, image=photo_img)

                canvas.image = photo_img  # Сохранение ссылки на изображение
                rotate_window.destroy()
               
            except ValueError:
                error_label = tk.Label(rotate_window, text="Введите целое число", fg="red")
                error_label.pack()

        rotate_button = tk.Button(rotate_window, text="Повернуть", command=rotate_image_done)
        rotate_button.pack()

def draw_rectangle():
    canvas.bind("<Button-1>", start_rectangle)
    canvas.bind("<B1-Motion>", draw_rectangle_on_canvas)
    canvas.bind("<ButtonRelease-1>", end_rectangle)

def start_rectangle(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def draw_rectangle_on_canvas(event):
    canvas.delete("rectangle")
    canvas.create_rectangle(start_x, start_y, event.x, event.y, outline=draw_color, tags="rectangle")

def end_rectangle(event):
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def draw_circle():
    canvas.bind("<Button-1>", start_circle)
    canvas.bind("<B1-Motion>", draw_circle_on_canvas)
    canvas.bind("<ButtonRelease-1>", end_circle)

def start_circle(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def draw_circle_on_canvas(event):
    canvas.delete("circle")
    radius = ((event.x - start_x) ** 2 + (event.y - start_y) ** 2) ** 0.5
    canvas.create_oval(start_x - radius, start_y - radius, start_x + radius, start_y + radius, outline=draw_color, tags="circle")

def end_circle(event):
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar)
file_menu.add_command(label="Сохранить", command=save_image)
file_menu.add_command(label="Открыть", command=open_image)
file_menu.add_separator()
file_menu.add_command(label="Очистить холст", command=clear_canvas)
menu_bar.add_cascade(label="Файл", menu=file_menu)

view_menu = tk.Menu(menu_bar)
view_menu.add_command(label="Сменить тему", command=toggle_theme)
menu_bar.add_cascade(label="Вид", menu=view_menu)

edit_menu = tk.Menu(menu_bar)
edit_menu.add_command(label="Масштабирование", command=lambda: scale_image(int(tk.simpledialog.askstring("Масштабирование", "Введите процент масштабирования (целое число):", parent=root))))
edit_menu.add_command(label="Черно-белый режим", command=apply_grayscale)
edit_menu.add_command(label="Розовый фильтр", command=apply_pink_filter)
edit_menu.add_command(label="Голубой фильтр", command=apply_blue_filter)
edit_menu.add_command(label="Обрезать", command=crop_image)
edit_menu.add_command(label="Отразить по горизонтали", command=flip_horizontal)
edit_menu.add_command(label="Повернуть", command=rotate_image)
menu_bar.add_cascade(label="Редактировать", menu=edit_menu)

draw_menu = tk.Menu(menu_bar)
draw_menu.add_command(label="Прямоугольник", command=draw_rectangle)
draw_menu.add_command(label="Круг", command=draw_circle)
menu_bar.add_cascade(label="Рисование", menu=draw_menu)

root.mainloop()
 
