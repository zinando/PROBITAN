"""This is the main application file. We import all modules/functions necessary to execute commands into this file and then make them to perform the required tasks.

First we create the application window (Tikinter).
"""
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
from helpers import myfunc as func
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
main = ctk.CTk()

#main window attributes
main.geometry("560x400")

#main window title
main.title("PROBITAN")

# Add image file
image = Image.open('appfiles/images/bg/bg_image.PNG')
bg = ImageTk.PhotoImage(image)
#bg = PhotoImage(file = "appfiles/images/bg/bg_image.PNG")
  
# Create Canvas
canvas1 = Canvas(main, width = 560, height = 400)  
canvas1.pack(fill = "both", expand = True)  
# Display image
canvas1.create_image(0, 0, image = bg, anchor = "nw")

#buttons 
start_btn = ctk.CTkButton(main, text="Start New Project", width=20, command=func.upload_file)#.place(x=180,y=200)
select_btn = ctk.CTkButton(main, text="Select Project", width=20)#.place(x=300,y=200)

button1_canvas = canvas1.create_window( 180, 200, anchor = "nw", window = start_btn)
button2_canvas = canvas1.create_window( 300, 200, anchor = "nw", window = select_btn)


#call a loop function main window
main.mainloop()

