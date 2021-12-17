from tkinter import *
import  tkinter as tk
from datetime import datetime
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import ImageTk, Image

def add_image():
    text.image_create(tk.END, image = img) # Example 1
    #text.window_create(tk.END, window = tk.Label(text, image = img)) # Example 2

root = tk.Tk()

text = tk.Text(root)
text.pack(padx = 20, pady = 20)

tk.Button(root, text = "Insert", command = add_image).pack()

img = tk.PhotoImage(file = "Capturar.PNG")

root.mainloop()