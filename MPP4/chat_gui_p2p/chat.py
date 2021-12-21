from tkinter import *
from datetime import datetime
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import os
from tkvideo import tkvideo
import socket
import threading

SERVER = ('localhost', 55555)
myPort = int(input("Digite a porta: "))

class Client:
    def __init__(self, largura, altura):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', myPort))
        self.sock.sendto(str(myPort).encode(), SERVER)

        self.window = Tk()
        self.window.title("Atividade 4")
        self.window.config(background='#1e1e1e')
        self.window.geometry('730x600+400+100')

        self.canva = Canvas(self.window, width=710, height=530)
        self.canva.config(background='white')
        self.canva.pack(side = TOP, padx = 10, pady = 10)

        self.gui_done = False

        global photoimage_list
        photoimage_list = []

        self.otherPort = self.get_other_user_port()
        self.createWidgets()
        

        listener = threading.Thread(target = self.listen)
        listener.start()


    def createWidgets(self):
        font_tuple = ("Helvetica", 12, "bold")

        # text area 
        self.txt_area = Text(self.canva, border=0, background='#323232')
        self.txt_area.config(width=670, height=40, foreground = 'white')
        self.txt_area.pack(side = TOP, padx = 0, pady = 0)


        # text field
        self.txt_field = Entry(self.window, width=26, background='#6c6c6c', foreground='white')
        self.txt_field.place(x=10, y=545, width=400, height=44)


        # send button
        self.send_button = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.send)
        self.send_button.config(text='enviar', font=font_tuple, foreground='black')
        self.send_button.place(x=415, y=545)


        # clear button
        self.trashButton = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.clear)
        self.trashButton.config(text='apagar', font=font_tuple, background='red')
        self.trashButton.place(x=622, y=545)

        # select file button
        self.selectButton = Button(self.window, width=9, height=2, relief='raised', state='active', pady=3, command=self.files)
        self.selectButton.config(text='anexo', font=font_tuple, foreground='black')
        self.selectButton.place(x=519, y=545)

        self.gui_done = True

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
            self.sock.sendto(tempMessage.encode('utf-8'), ('localhost', self.otherPort))
            self.txt_field.delete(0, END)
    

    def listen(self):
        while True:
            if self.gui_done:
                data = self.sock.recv(1024)
                self.txt_area.insert(END, data.decode('utf-8'))
    
    def clear(self, event=None):
        self.txt_area.delete(1.0, END)


    def files(self, event=None):
        global my_image
        global photoimage_list

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        tempMessage = "[{}]: {}".format(dt_string, "\n")

        filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"), ("mp3 files", "*.mp3"), ("mp4 files", "*.mp4"), ("mov files", "*.mov")))
        arquivo, extn = os.path.splitext(filename)
        
        extn = extn.lower()

        if extn == '.png' or extn == '.jpg':
            my_image = ImageTk.PhotoImage(Image.open(filename).resize((200, 200), Image.ANTIALIAS))
            photoimage_list.append(my_image)
            self.txt_area.insert(END, tempMessage)
            self.txt_area.insert(END, "Arquivo {} enviado.\n".format(extn))
            self.txt_area.image_create(END, image=my_image)
            self.txt_area.insert(END, "\n\n")
            self.sock.sendto(bytes(my_image), ('localhost', self.otherPort))

        elif extn == '.mov' or extn == '.mp4':
            
            self.txt_area.insert(END, tempMessage)
            self.txt_area.insert(END, "Arquivo {} enviado.\n".format(extn))


            video_label = Label(self.window)
           
            player = tkvideo(filename, video_label, loop = 1, size = (640,360))
            player.play()
            self.txt_area.window_create(END, window= video_label)

            self.txt_area.insert(END, "\n\n")

        elif extn == '.mp3':
            self.txt_area.insert(END, tempMessage)
            self.txt_area.insert(END, "Arquivo {} enviado.\n".format(extn))
            # adicionar codigo de musica aqui
            self.txt_area.insert(END, "\n\n")



    def start(self):
        self.window.mainloop()

    
    def get_other_user_port(self):
        while True:
            data = self.sock.recv(1024).decode()

            if data.strip() == 'ready':
                print('checked in with server, waiting')
                break

        data = self.sock.recv(1024).decode()
        ip, sport, dport = data.split(' ')
        sport = int(sport)
        dport = int(dport)

        print('\ngot peer')
        print('  ip:          {}'.format(ip))
        print('  source port: {}'.format(sport))
        print('  dest port:   {}\n'.format(dport))


        print('punching hole')

        self.sock.sendto(b'0', (ip, dport))

        print('ready to exchange messages\n')

        return dport
        


if __name__ == '__main__':
    interface = Client(10, 600).start()