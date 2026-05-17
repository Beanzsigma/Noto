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
loadfont(getpath("Magnolia.ttf"))
def gifbg():
    global afterid
    if afterid:
        app.after_cancel(afterid)
    for widget in app.winfo_children():
        widget.destroy()
    frames = []
    gif = Image.open(getpath("infbg.gif"))
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
    canvas.create_text(304, 34, text="Noto", font=("Khuja Uppercase Uppercase", 37), fill="#585454", anchor='center')
    canvas.create_text(300, 30, text="Noto", font=('Khuja Uppercase Uppercase', 37), fill="#bbb5b5", anchor="center")
    notebox = ctk.CTkTextbox(app, width=500, height=225, fg_color="#111111", text_color="white", border_color="white", border_width=1, corner_radius=8, font=("OriginalMagnolia", 14), wrap='word')
    notebox.place(x=50, y=80)
    summarybox = ctk.CTkTextbox(app, width=500, height=188, fg_color="#111111", text_color='white', border_color="white", border_width=1, corner_radius=8, font=('OriginalMagnolia', 14), wrap='word')
    summarybox.place(x=50, y=385)
    submitshdw = canvas.create_text(303, 353, text="Summarize", font=('Khuja Uppercase Uppercase', 24), fill="#585454", anchor='center')
    submit = canvas.create_text(300, 350, text="Summarize", font=('Khuja Uppercase Uppercase', 24), fill="#bbb5b5", anchor='center')
    def enter(e):
        canvas.itemconfig(submitshdw, fill="#0a0a0a")
        canvas.itemconfig(submit, fill="#585454")
    def leave(e):
        canvas.itemconfig(submit, fill="#bbb5b5")
        canvas.itemconfig(submitshdw, fill="#585454")
    canvas.tag_bind(submit, "<Enter>", enter)
    canvas.tag_bind(submitshdw, "<Enter>", enter)
    canvas.tag_bind(submitshdw, "<Leave>", leave)
    canvas.tag_bind(submit, "<Leave>", leave)
    canvas.tag_bind(submitshdw, "<Button-1>", main)
    canvas.tag_bind(submit, "<Button-1>", main)

main()


app.mainloop()