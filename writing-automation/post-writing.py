#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
submit-writing.py is a user interface to allow for the easy addition of writing pieces to trentonbauer.com/writing.html
'''

import subprocess
import tkinter as tk
from tkinter import filedialog

filename = "please select an image"

def submit():
    title = title_entry.get()
    subtitle = subtitle_entry.get()
    body_text = text_entry.get("1.0",'end-1c')
    image_filepath = image_explorer.cget("text")
    image_name = image_filepath[image_filepath.rindex("/")+1:]
    image_alt = image_alt_entry.get()
    window.destroy()

    # move image to images directory
    subprocess.run(["image-mover.bat", image_filepath.replace("/", "\\")])

    # construct new html
    with open("./writing-template.txt", "r") as file:
        inserthtml = file.read()
        inserthtml = inserthtml.replace("%IMAGETARGET%", image_name)
        inserthtml = inserthtml.replace("%ALTTARGET%", image_alt)
        inserthtml = inserthtml.replace("%TITLETARGET%", title)
        inserthtml = inserthtml.replace("%SUBTITLETARGET%", subtitle)
        body_text = body_text.replace("\n", "</p>\n            <p>").replace("<p></p>", "<br>")
        inserthtml = inserthtml.replace("%BODYTARGET%", body_text)
        inserthtml = inserthtml.replace("%IDTARGET%", title.lower().strip().replace(" ", "-"))
    
    # edit writing.html
    with open("../pages/writing.html", "r") as file:
        oldhtml = file.read()
    newhtml = oldhtml[:oldhtml.index("<!-- automated post target -->")+len("<!-- automated post target -->")] + inserthtml + oldhtml[oldhtml.index("<!-- automated post target -->")+len("<!-- automated post target -->"):]
    with open("../pages/writing.html", "w") as file:
        file.write(newhtml)

    # commit and push changes
    subprocess.run(["commit.bat", image_name])

def pick_image():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = [('image files', '.png'), ('image files', '.jpg'), ('image files', '.jpeg')])
    image_explorer.configure(text=filename)

window = tk.Tk()
window.title("Post Writing")

# title
title_frame = tk.Frame(master=window)
tk.Label(master=title_frame, text="Title: ", font="Tahoma 20 bold", width=14, anchor="w").grid(row=1, column=1, padx=25, pady=5)
title_entry = tk.Entry(master=title_frame, width=100, font="Tahoma 15")
title_entry.grid(row=1, column=2, padx=25, pady=5)
title_frame.pack(anchor="w")

# subtitle
subtitle_frame = tk.Frame(master=window)
tk.Label(master=subtitle_frame, text="Subtitle: ", font="Tahoma 20 bold", width=14, anchor="w").grid(row=1, column=1, padx=25, pady=5)
subtitle_entry = tk.Entry(master=subtitle_frame, width=100, font="Tahoma 15")
subtitle_entry.grid(row=1, column=2, padx=25, pady=5)
subtitle_frame.pack(anchor="w")

# image
image_frame = tk.Frame(master=window)
tk.Label(master=image_frame, text="Image: ", font="Tahoma 20 bold", width=14, anchor="w").grid(row=1, column=1, padx=25, pady=5)
image_explorer = tk.Button(master=image_frame, text=filename, command=pick_image)
image_explorer.grid(row=1, column=2, padx=25, pady=5)
image_frame.pack(anchor="w")

# image alt text
image_alt_frame = tk.Frame(master=window)
tk.Label(master=image_alt_frame, text="Image Alt Text: ", font="Tahoma 20 bold", width=14, anchor="w").grid(row=1, column=1, padx=25, pady=5)
image_alt_entry = tk.Entry(master=image_alt_frame, width=100, font="Tahoma 15")
image_alt_entry.grid(row=1, column=2, padx=25, pady=5)
image_alt_frame.pack(anchor="w")

# text
text_frame = tk.Frame(master=window)
tk.Label(master=text_frame, text="Body Text: ", font="Tahoma 20 bold", width=14, anchor="w").grid(row=1, column=1, padx=25, pady=5)
text_entry = tk.Text(master=text_frame, width=100, font="Tahoma 15")
text_entry.grid(row=1, column=2, padx=25, pady=5)
text_frame.pack(anchor="w")

# submit
tk.Button(master=window, text="Submit", command=submit).pack(pady=10)

window.mainloop()
