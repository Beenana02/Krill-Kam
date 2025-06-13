import tkinter as tk
from tkinter import ttk
from tkinter import *
import ttkbootstrap as ttk
import cv2
from PIL import Image, ImageTk
from time import strftime

#fills images
def fill_image(event,imaged,ratio):
    global newImage_tk
    backgroundsRatio = event.width/event.height

    if backgroundsRatio>ratio:
        width =int(event.width)
        height =int(width/ratio)
    else:
        height =int(event.height)
        width =int(height*ratio)

    resizedImage= imaged.resize((width,height))
    newImage_tk=ImageTk.PhotoImage(resizedImage)
    backgrounds.create_image(int(event.width/2),
                             int(event.height/2), 
                             anchor ='center',
                             image=newImage_tk)

root = ttk.Window()
root.title("Krill Kam!")
root.geometry('320x240')
root.minsize(320,240)
root.maxsize(1280,960)
root.columnconfigure(0,weight =1, uniform='a')
root.rowconfigure((0),weight =1, uniform='a')

#center app
root.update_idletasks()
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
width = root.winfo_width()
height = root.winfo_height()
x = (screen_width//2 - (width//2))
y = (screen_height//2 - (height//2) )
root.geometry(f"{width}x{height}+{x}+{y}")

#root.overrideredirect(True)
root.bind('<Escape>',lambda event: root.quit())

#set background
blueBack=Image.open('GUIimages/blue-background.jpeg')
blueRatio = blueBack.size[0]/blueBack.size[1]
blueImage=ImageTk.PhotoImage(blueBack)

backgrounds= tk.Canvas(root,background='black', bd=0, highlightthickness=0, relief='ridge')

backgrounds.bind('<Configure>', lambda event: fill_image(event, blueBack,blueRatio))
backgrounds.grid(column=0, row=0, sticky='nsew')

root.mainloop()