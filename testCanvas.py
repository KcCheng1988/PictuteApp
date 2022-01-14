import tkinter as tk
from tkinter import ttk
import cv2
from PIL import ImageTk, Image

"https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan"
"https://tkdocs.com/tutorial/canvas.html"
def zoom_in(event, base_factor=0.5):
   x = canvas.canvasx(event.x)
   y = canvas.canvasy(event.y)
   factor = 1.001 ** event.delta
   canvas.scale('all', x, y, factor, factor)

# https://tkdocs.com/shipman/
root = tk.Tk()

sample_img_path = r"C:\Users\ckc3b\Desktop\sample.jpg"
sample_img = cv2.imread(sample_img_path)
sample_img = cv2.cvtColor(sample_img, cv2.COLOR_BGR2RGB)
imgh, imgw = sample_img.shape[:2]
img = ImageTk.PhotoImage(Image.fromarray(sample_img))

# create canvas
# Event class: https://tkdocs.com/shipman/event-handlers.html
# Key names: https://tkdocs.com/shipman/key-names.html
# https://python-course.eu/tkinter/events-and-binds-in-tkinter.php
canvas = tk.Canvas(height=imgh, width=imgw, cursor='crosshair')
canvas.create_image(0,0, anchor='nw', image=img)
canvas.bind('<MouseWheel>', zoom_in)
canvas.grid()

root.mainloop()


