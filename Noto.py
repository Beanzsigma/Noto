import customtkinter as ctk
import sounddevice as sd
import struct
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from groq import Groq
from tkinter import Canvas, Text
from PIL import Image, ImageSequence, ImageTk
import pythoncom 
import threading
afterid = None
import sys
import os
app = ctk.CTk()
app.title("Noto")
app.geometry('600x600')
app.resizable(False, False)
FR_PRIVATE = 0x10
def getpath(relativepath):
    try:
        basepath = sys._MEIPASS
    except AttributeError:
        basepath = os.path.abspath('.')
    return os.path.join(basepath, relativepath)
def loadfont(fontpath):
    windll.gdi32.AddFontResourceExW(fontpath, FR_PRIVATE, 0)
loadfont(getpath("Khuja-Uppercase.otf"))
def gifbg():
    global afterid
    if afterid:
        app.after_cancel(afterid)
    for widget in app.winfo_children():
        widget.destroy()
    frames = []
    gif = Image.open(getpath("coolstar.gif"))
    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy().convert("RGBA")
        r, g, b, a = frame.split()
        a = a.point(lambda x:x*0.4)
        frame.putalpha(a)
        frames.append(ImageTk.PhotoImage(frame.resize((600, 600))))
    canvas = Canvas(app, width=600, height=600, highlightthickness=0, bd=0, bg='black')
    canvas.place(x=0, y=0)
    canvasbg = canvas.create_image(0, 0, anchor='nw')
    def animate(frame_index=0):
        global afterid
        canvas.itemconfig(canvasbg, image=frames[frame_index])
        canvas._frames = frames
        afterid = app.after(20, animate, (frame_index+1) % len(frames))
    animate()
    return canvas, canvasbg
def main():
    canvas, canvasbg = gifbg()
    canvas.create_text(300, 30, text="yo", font=('Khuja Uppercase Uppercase', 21), fill="#ffffff", anchor="center")



main()


app.mainloop()