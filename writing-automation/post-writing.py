#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
submit-writing.py is a user interface to allow for the easy addition of writing pieces to trentonbauer.com/writing.html
'''

from datetime import datetime, timezone
import subprocess
import re
import tkinter as tk
from tkinter import filedialog

filename = "please select an image"

def sanitize_preview_text(txt: str):
    txt = txt.replace("\n", " ")
    txt = txt[:512]
    end = min(txt.rfind(' '), txt.rfind('.'), txt.rfind(';'), txt.rfind(','))
    txt = txt[:end] + " . . ."
    return txt

def sanitize_body_text(txt: str):
    txt = txt.replace("\n", "</p>\n            <p>")
    txt = txt.replace("<p></p>", "<br>")
    return txt

def construct_new_link_html(file_name: str, image_name: str, image_alt: str, title: str, body_text: str):
    with open("./writing-link-template.txt", "r") as file:
        html = file.read()
        html = html.replace("%IMAGETARGET%", image_name)
        html = html.replace("%ALTTARGET%", image_alt)
        html = html.replace("%TITLETARGET%", title)
        html = html.replace("%BODYTARGET%", sanitize_preview_text(body_text))
        html = html.replace("%NEWFILENAME%", file_name)
    return html

def construct_new_writing_html(file_name: str, image_name: str, image_alt: str, title: str, subtitle: str, body_text: str):
    with open("./writing-template.txt", "r") as file:
        html = file.read()
        html = html.replace("%IMAGETARGET%", image_name)
        html = html.replace("%ALTTARGET%", image_alt)
        html = html.replace("%TITLETARGET%", title)
        html = html.replace("%SUBTITLETARGET%", subtitle)
        html = html.replace("%BODYTARGET%", body_text)
        html = html.replace("%IDTARGET%", file_name)
        current_time = datetime.now(timezone.utc)
        formatted_time = current_time.isoformat(timespec='milliseconds') + 'Z'
        html = html.replace("%DATETIMETARGET%", str(formatted_time))
    return html

def construct_file_name(input_string: str):
    # sanitize the string: remove invalid characters
    sanitized_string = re.sub(r'[<>:"/\\|?*]', "", input_string)
    # remove leading/trailing spaces
    sanitized_string = sanitized_string.strip()
    # Limit the length of the file name to avoid system issues
    sanitized_string = sanitized_string[:255]
    # Replace spaces with underscores
    sanitized_string = sanitized_string.replace(" ", "-")
    return sanitized_string + ".html"

def submit():
    title = title_entry.get()
    new_file_name = construct_file_name(title)
    subtitle = subtitle_entry.get()
    body_text = text_entry.get("1.0",'end-1c')
    image_filepath = image_explorer.cget("text")
    image_name = image_filepath[image_filepath.rindex("/")+1:]
    image_alt = image_alt_entry.get()
    window.destroy()

    # move image to images directory
    subprocess.run(["image-mover.bat", image_filepath.replace("/", "\\")])

    # construct new html for link
    insertlinkhtml = construct_new_link_html(new_file_name, image_name, image_alt, title, body_text)
    
    # edit writing.html
    with open("../pages/writing.html", "r") as file:
        oldhtml = file.read()
    newhtml = oldhtml[:oldhtml.index("<!-- automated post target -->")+len("<!-- automated post target -->")] + insertlinkhtml + oldhtml[oldhtml.index("<!-- automated post target -->")+len("<!-- automated post target -->"):]
    with open("../pages/writing.html", "w") as file:
        file.write(newhtml)

    # construct new html for article page
    newhtml = construct_new_writing_html(new_file_name, image_name, image_alt, title, subtitle, body_text)

    with open("../pages/writings/" + new_file_name, "w") as file:
        file.write(newhtml)

    # commit and push changes
    subprocess.run(["commit.bat", image_name, new_file_name])

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
