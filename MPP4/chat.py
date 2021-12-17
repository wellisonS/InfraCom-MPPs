from tkinter import *
from datetime import datetime
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import ImageTk, Image

class GUI:
    def __init__(self, largura, altura):
        self.window = Tk()
        self.window.title("Atividade 4")
        self.window.config(background='#1e1e1e')
        self.window.geometry('730x600+400+100')

        self.canva = Canvas(self.window, width=200, height=200)
        self.canva.grid(row=0,column=0,columnspan=2)
        self.canva.place(x=10, y=10, width=710, height=530)

        self.canva.pack()

        self.createWidgets()

    
    def createWidgets(self):
        font_tuple = ("Helvetica", 12, "bold")

        # text area 
        self.txt_area = Text(self.window, border=1, background='#323232')
        self.txt_area.place(x=10, y=10, width=710, height=530)


        # text field
        self.txt_field = Entry(self.window, width=26, background='#6c6c6c', foreground='white')
        self.txt_field.place(x=10, y=550, width=400, height=44)


        # send button
        self.send_button = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.send)
        self.send_button.config(text='enviar', font=font_tuple, foreground='black')
        self.send_button.place(x=415, y=550)


        # clear button
        #trashPhoto=PhotoImage(file="trash_black.png")
        self.trashButton = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.clear)
        self.trashButton.config(text='apagar', font=font_tuple, background='red')
        self.trashButton.place(x=622, y=550)


        # select file button
        self.selectButton = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.files)
        self.selectButton.config(text='anexo', font=font_tuple, foreground='black')
        self.selectButton.place(x=519, y=550)

        
        # key return/enter
        self.window.bind('<Return>', self.send)


    def send(self, event=None):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        texto = self.txt_field.get() + '\n'

        if texto == '\n':
            self.txt_field.delete(0, END)
        else:
            tempMessage = "[{}]: {}".format(dt_string, texto)
            self.txt_area.insert(END, tempMessage)
            self.txt_field.delete(0, END)

    
    def clear(self, event=None):
        self.txt_area.delete(1.0, END)


    def files(self, event=None):
        filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"), ("mp3 files", "*.mp3"), ("mp4 files", "*.mp4"), ("mov files", "*.mov")))
        my_image = ImageTk.PhotoImage(Image.open(filename))
        my_label = Label(image = my_image)
        my_label.pack()

        
    
        #my_label = Label(self.window, text=self.window.filename).pack()
        #my_image = ImageTk.PhotoImage(Image.open(self.window.filename))
        #my_image_label = Label(image=my_image).pack()

    
    def start(self):
        self.window.mainloop()
        



if __name__ == '__main__':
    interface = GUI(10, 600).start()

