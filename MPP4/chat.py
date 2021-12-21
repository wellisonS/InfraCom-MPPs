from tkinter import *
from datetime import datetime
from tkinter import font
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import cv2 
import os
#from pygame.music import play
from tkvideo import tkvideo
import pygame



class GUI:
    def __init__(self, largura, altura):
        self.window = Tk()
        self.window.title("Atividade 4")
        self.window.config(background='#1e1e1e')
        self.window.geometry('730x600+400+100')

        self.canva = Canvas(self.window, width=710, height=530)
        #self.canva.grid(row=0,column=0,columnspan=2)
        #self.canva.place(x=10, y=10, width=710, height=700)
        self.canva.config(background='white')
        self.canva.pack(side = TOP, padx = 10, pady = 10)

        global photoimage_list
        photoimage_list = []
        global filename

        pygame.mixer.init()

        self.createWidgets()

    def createWidgets(self):
        font_tuple = ("Helvetica", 12, "bold")

        # text area 
        self.txt_area = Text(self.canva, border=0, background='#323232')
        self.txt_area.config(width=670, height=40)
        #self.txt_area.place(x=10, y=10, width=710, height=700)
        self.txt_area.pack(side = TOP, padx = 0, pady = 0)


        # text field
        self.txt_field = Entry(self.window, width=26, background='#6c6c6c', foreground='white')
        self.txt_field.place(x=10, y=545, width=400, height=44)


        # send button
        self.send_button = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.send)
        self.send_button.config(text='enviar', font=font_tuple, foreground='black')
        self.send_button.place(x=415, y=545)


        # clear button
        #trashPhoto=PhotoImage(file="trash_black.png")
        self.trashButton = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.clear)
        self.trashButton.config(text='apagar', font=font_tuple, background='red')
        self.trashButton.place(x=622, y=545)


        # select file button
        self.selectButton = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.files)
        self.selectButton.config(text='anexo', font=font_tuple, foreground='black')
        self.selectButton.place(x=519, y=545)

        
        # key return/enter
        self.window.bind('<Return>', self.send)


    def send(self, event=None):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        texto = self.txt_field.get() + '\n\n'

        if texto == '\n\n':
            self.txt_field.delete(0, END)
        else:
            tempMessage = "[{}]: {}".format(dt_string, texto)
            self.txt_area.insert(END, tempMessage)
            self.txt_field.delete(0, END)

    
    def clear(self, event=None):
        self.txt_area.delete(1.0, END)


    def files(self, event=None):
        global my_image
        global photoimage_list
        global filename

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        tempMessage = "[{}]: {}".format(dt_string, "\n")

        filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"), ("mp3 files", "*.mp3"), ("mp4 files", "*.mp4"), ("mov files", "*.mov")))
        arquivo, extn = os.path.splitext(filename)

        if extn == '.png' or extn == '.jpg':
            my_image = ImageTk.PhotoImage(Image.open(filename).resize((200, 200), Image.ANTIALIAS))
            photoimage_list.append(my_image)
            self.txt_area.insert(END, tempMessage)
            self.txt_area.insert(END, "Arquivo {} enviado.\n".format(extn))
            self.txt_area.image_create(END, image=my_image)
            self.txt_area.insert(END, "\n\n")

        elif extn == '.mov' or extn == '.mp4':
            self.txt_area.insert(END, tempMessage)
            self.txt_area.insert(END, "Arquivo {} enviado.\n".format(extn))




            video_label = Label(self.window)
            #video_label.pack()
            player = tkvideo(filename, video_label, loop = 1, size = (640,360))
            player.play()
            self.txt_area.window_create(END, window= video_label)

            # cap = cv2.VideoCapture(filename)
            # while (True):
            #     ret, frame = cap.read()
            #     frame = cv2.resize(frame, (640, 360))
            #     cv2.imshow('video play', frame)
            #     if (cv2.waitKey(1) & 0xFF == ord('q')):
            #         break
            self.txt_area.insert(END, "\n\n")

        elif extn == '.mp3':
            self.txt_area.insert(END, tempMessage)
            self.txt_area.insert(END, "Arquivo {} enviado.\n".format(extn))
            # adicionar codigo de musica aqui

            audio_label = Label(self.window, width=200, height=100)
            playAudioButton = Button(audio_label, text="play", font=('Helvetica', 20),  command= self.playAudio)
            playAudioButton.pack(side = LEFT, padx = 0, pady = 0)
            stopAudioButton = Button(audio_label, text="pause", font=('Helvetica', 20),  command= self.stopAudio)
            stopAudioButton.pack(side = RIGHT, padx = 0, pady = 0)

            self.txt_area.window_create(END, window= audio_label)
            self.txt_area.insert(END, "\n\n")


    def playAudio(self):
        global filename
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops=0)
        print("socorro deus entrou aqui")

    def stopAudio(self):
        pygame.mixer.music.stop()



    def start(self):
        self.window.mainloop()
        


if __name__ == '__main__':
    interface = GUI(10, 600).start()

