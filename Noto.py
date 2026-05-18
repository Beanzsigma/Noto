import customtkinter as ctk
import sounddevice as sd
import struct
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
from groq import Groq
from comtypes import CLSCTX_ALL
from tkinter import Canvas, Text
from PIL import Image, ImageSequence, ImageTk
import pythoncom 
from dotenv import load_dotenv
import threading
from groq import Groq
from tkinter import filedialog
afterid = None
import sys
import os
load_dotenv()
GROQkey = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQkey)
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
def summarizegroq(notes):
    response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "system","content": "You summarize notes into clear and concise key points. Use short bullet points. If the notes are too short or something like that, "
    "take your best guess, and NEVER ask questions and stuff like that. YOU ARE SUPPOSED TO SUMMARIZE NOTES, if the given notes don't explain stuff, you also don't explain stuff. All you do is summarize that's it. Don't"
    "include anything else, just these things."},{"role": "user","content": notes}],
        temperature=0.3,
        max_tokens=300)
    return response.choices[0].message.content
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
    def savenotes(e=None):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w", encoding='utf-8') as file:
                file.write(notebox.get("1.0", "end-1c"))
    def loadnotes(e=none)
    def summarizenotes(e=None):
        notes= notebox.get("1.0", "end-1c")
        summarybox.delete("1.0", "end")
        if notes.strip() =="":
            summarybox.insert('1.0', "Insert text first.")
            return
        summarybox.insert("1.0", "Summarizing...")
        def runsummarynotes():
            try:
                summary = summarizegroq(notes)
                app.after(0, lambda: showsummary(summary))
            except Exception as ex:
                app.after(0, lambda: showsummary(f"Error: {ex}"))
        def showsummary(summary):
            summarybox.delete("1.0", 'end')
            summarybox.insert("1.0", summary)
        threading.Thread(target=runsummarynotes, daemon=True).start()
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
    canvas.tag_bind(submitshdw, "<Button-1>", summarizenotes)
    canvas.tag_bind(submit, "<Button-1>", summarizenotes)


main()
app.mainloop()