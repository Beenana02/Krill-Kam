import tkinter as tk
from tkinter import ttk
from tkinter import *
import ttkbootstrap as ttk
import cv2
from PIL import Image, ImageTk
from time import strftime

def stretch_image(event):
    global newImage_tk
    widthS = event.width
    heightS = event.height
    newImage=fish.resize((widthS,heightS))
    newImage_tk=ImageTk.PhotoImage(newImage)
    backgrounds.create_image(0,0, image=newImage_tk, anchor='nw')

def fill_image(event):
    global newImage_tk
    backgroundsRatio = event.width/event.height

    if backgroundsRatio>fishRatio:
        width =int(event.width)
        height =int(width/fishRatio)
    else:
        height =int(event.height)
        width =int(height*fishRatio)
    resizedImage= fish.resize((width,height))
    newImage_tk=ImageTk.PhotoImage(resizedImage)
    backgrounds.create_image(int(event.width/2),
                             int(event.height/2), 
                             anchor ='center',
                             image=newImage_tk)

def full_image(event):
    

root = ttk.Window(themename='journal')
root.title("Krill Kam!")
root.state('zoomed')

root.columnconfigure(0,weight =1, uniform='a')
root.rowconfigure((0),weight =1, uniform='a')

currentImage="GUIimages/asadal_stock_194.jpg"
fish=Image.open(currentImage)
fishRatio = fish.size[0]/fish.size[1]
fishIma=ImageTk.PhotoImage(fish)

#background
backgrounds= tk.Canvas(root,background='black', bd=0, highlightthickness=0, relief='ridge')
backgrounds.grid(column=0, row=0, sticky='nsew')

backgrounds.bind('<Configure>', fill_image)

def time_now():
    currentTime= strftime('%D %I:%M:%S %p ')
    localTime.config(text=currentTime)
    localTime.after(1500, time_now)

#current time section
# clockFrame= ttk.Frame(root)
# clockFrame.pack(padx=20, pady=20)


# localTime= ttk.Label(clockFrame, background='lightblue', foreground='white', font=('Courier New', 40))
# localTime.pack()
# time_now()

root.mainloop()