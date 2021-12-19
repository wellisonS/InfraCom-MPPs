import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk


def stop_rec():
    global running
    running = False

    start_button.config(state="normal")
    stop_button.config(state="disabled")

def start_capture():
    global capture, last_frame

    capture = cv2.VideoCapture(0)
    
    fourcc = cv2.VideoWriter_fourcc("X", "V", "I", "D")
    video_writer = cv2.VideoWriter(r"sample.avi", fourcc, 30.0, (640, 480))

    while running:
        rect, frame =  capture.read()

        if rect:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            last_frame = Image.fromarray(cv2image)
            video_writer.write(frame)

    capture.release()
    video_writer.release()

def update_frame():
    if last_frame is not None:
        tk_img = ImageTk.PhotoImage(master=video_label, image=last_frame)
        video_label.config(image=tk_img)
        video_label.tk_img = tk_img

    if running:
        root.after(10, update_frame)

def start_rec():
    global running

    running = True
    thread = threading.Thread(target=start_capture, daemon=True)
    thread.start()
    update_frame()

    start_button.config(state="disabled")
    stop_button.config(state="normal")

def closeWindow():
    stop_rec()
    root.destroy()


running = False
after_id = None
last_frame = None

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", closeWindow)

video_label = tk.Label()
video_label.pack(expand=True, fill="both")

start_button = tk.Button(text="Start", command=start_rec)
start_button.pack()
stop_button = tk.Button(text="Stop", command=stop_rec, state="disabled")
stop_button.pack()

root.mainloop()