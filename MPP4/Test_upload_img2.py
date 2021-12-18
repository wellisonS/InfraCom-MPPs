from tkinter import *
from datetime import datetime
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import ImageTk, Image

root = Tk()

# Position text in frame
Label(root, text = 'Position image on button', font =('<font_name>', 16)).pack(side = TOP, padx = 10, pady = 10)

# Create a photoimage object of the image in the path
filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"), ("mp3 files", "*.mp3"), ("mp4 files", "*.mp4"), ("mov files", "*.mov")))
photo = PhotoImage(file = filename)

# Resize image to fit on button
photoimage = photo.subsample(1, 2)

# Position image on button
Button(root, image = photoimage,).pack(side = BOTTOM, pady = 20)
mainloop()