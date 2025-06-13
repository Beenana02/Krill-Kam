import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import cv2
from PIL import Image, ImageTk
from time import strftime

root = ttk.Window()
root.title("Krill Kam!")
root.geometry('320x240')
root.minsize(320,240)
root.maxsize(1280,960)
root.columnconfigure(0,weight =1, uniform='a')
root.columnconfigure(1,weight =2, uniform='a')
root.rowconfigure((0),weight =1, uniform='a')
root.rowconfigure((1),weight =2, uniform='a')


#create transparent background


# --- functions --- #
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

#fits to camera preview to canvas while keeping aspect ratio
def fit_image(image, width, height):

    old_width, old_height = image.size
    aspectRatio = old_width/old_height
    currentRatio=width/height
    if(currentRatio>aspectRatio):
        nHeight= height
        nWidth= int(nHeight*aspectRatio)
    else:
        nWidth=width
        nHeight=int(nWidth/aspectRatio)
    resizedImage= image.resize((nWidth,nHeight),Image.LANCZOS)
    return ImageTk.PhotoImage(resizedImage)


#camera stuff
def show_frame():
   # get frame
   ret, frame = cap.read()
   
   if ret:
       # cv2 uses `BGR` but `GUI` needs `RGB`
       
       cv2frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

       # convert to PIL image
       img = Image.fromarray(cv2frame)

       #resize window

       widthS=int(previewArea.winfo_width())
       heightS=int(previewArea.winfo_height())
       resizedImage = fit_image(img,widthS,heightS)

       # convert to Tkinter image
       photo = resizedImage
       
       # solution for bug in `PhotoImage`
       cameraLabel.photo = photo
       
       # replace image in label
       cameraLabel.configure(image=photo)  
   
   # run again after 20ms (0.02s)
   root.after(20, show_frame)

#Gets local time
def time_now():
    currentTime= strftime('%D %I:%M:%S %p ')
    localTime.config(text=currentTime)
    localTime.after(1500, time_now)


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
backgrounds.grid(column=0, row=0, columnspan=root.grid_size()[0],rowspan=root.grid_size()[1], sticky='nsew')

#camera/photo sections
previewFrame=tk.Frame(root)
previewFrame.grid(column=1,row=0, rowspan=root.grid_size()[1], sticky='nesw')

previewArea=tk.Frame(previewFrame, bg='black')
previewArea.pack(fill='both',expand=True)
previewArea.update()

#set up camera preview gotten from stack overflow for basics, plan to update later
cap = cv2.VideoCapture(0)
image_id = None
cameraLabel= ttk.Label(previewArea)
cameraLabel.pack(fill='both', expand=True)

#Clock feature
localTime= ttk.Label(previewFrame, background=None, foreground='black', font=('Courier New', 10))
localTime.pack(fill='x',anchor='ne')
time_now()

#Live Camera feed buttons
camera_buttons=[]
buttonFrame = tk.Frame(root)
buttonFrame.grid(column=0,row=0,sticky='nesw')

capture=ttk.Button(buttonFrame, text='Capture')
camera_buttons.append(capture)

record=ttk.Button(buttonFrame, text='Record')
camera_buttons.append(record)

reviewMode=ttk.Button(buttonFrame, text='Review')
camera_buttons.append(reviewMode)

settings=ttk.Button(buttonFrame, text='settings')
camera_buttons.append(settings)


for index, button in enumerate(camera_buttons):
    button.pack(fill='both',expand=True,padx=1,pady=1)
    #button.config(background = 'red', foreground='black')

#krillCanvas= ttk.Canvas(root,background='blue')
#krillCanvas.grid(column=0,row=1,sticky='nesw')

show_frame()
root.mainloop()
cap.release()