from tkinter import *
from tkvideo import tkvideo
from tkinter import filedialog

root = Tk()
my_label = Label(root)
my_label.pack()

filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"), ("mp3 files", "*.mp3"), ("mp4 files", "*.mp4"), ("mov files", "*.mov")))

player = tkvideo(filename, my_label, loop = 1, size = (1280,720))
player.play()

root.mainloop()