import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as ttk
import cv2
from PIL import Image, ImageTk
from time import strftime
import os

root = ttk.Window(themename='morph')
root.title("Krill Kam!")
root.geometry('320x240')
root.minsize(320,240)
root.maxsize(1280,960)
root.columnconfigure(0,weight =1, uniform='a')
root.columnconfigure(1,weight =5, uniform='a')
root.rowconfigure((0),weight =1, uniform='a')
root.rowconfigure((1),weight =2, uniform='a')
root.rowconfigure((2),weight =1, uniform='a')

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

#Gets fps of camera
def fps_counter():
    fps = cap.get(cv2.CAP_PROP_FPS)
    fpsLabel.config(text='FPS: '+str(fps))
    fpsLabel.after(2000, fps_counter)

#Gets local time
def time_now():
    currentTime= strftime('%D %I:%M:%S %p ')
    localTime.config(text=currentTime)
    localTime.after(1500, time_now)

#Power down camera
def power_off():
    powerWindow = tk.Toplevel()

    powerWindow.title("power off")
    powerWindow.geometry('320x240')
    powerWindow.grid_columnconfigure((0,1),weight=1,uniform='a')
    powerWindow.rowconfigure((0,1),weight=1,uniform='a')
    centerWindows(powerWindow)

    #display screen background
    load=Image.open('GUIimages/exitScreen.png')
    photo1=fit_image(load, 320, 240)
    background = ttk.Label(powerWindow,image=photo1)
    background.image = photo1
    background.grid(column=0,row=0, rowspan=2, columnspan=2, sticky='news')
    
    yesB=ttk.Button(powerWindow,text='Yes',command=lambda: root.destroy(), bootstyle='danger')
    yesB.grid(column=0,row=1, sticky='sw')
    noB=ttk.Button(powerWindow,text='No', command=lambda: powerWindow.destroy())
    noB.grid(column=1,row=1, sticky='se')


    #if powered off from screen it will display a popup message first then shutdown
            

    #if powered down from switch button it will complete a safe shutdown

#Review photos window
def create_photo_window():
    global photoLabel
    global prevK
    global nextK
    global counter
    global photo_window
    #basic canvas
    photo_window = tk.Toplevel()
    photo_window.title("Photo Reviewer")
    photo_window.geometry('320x240')
    photo_window.grid_columnconfigure((0,1),weight=1,uniform='a')
    photo_window.rowconfigure((0,1),weight=1,uniform='a')
    centerWindows(photo_window)

    #photo canvas
    photoLabel= ttk.Label(photo_window, text='place holder', background='black', anchor= 'center')
    photoLabel.grid(column=0,row=0,columnspan=photo_window.grid_size()[0], rowspan=photo_window.grid_size()[1])
    
    title = ttk.Label(photo_window,text='Review your images!',anchor='center')
    title.grid(column=0,row=1, columnspan=photo_window.grid_size()[0], sticky='sew')
    #forward/ backward options
    prevK = ttk.Button(photo_window,text='Prev', command= last_photo)
    prevK.grid(column=0,row=1,sticky='sw')
    nextK = ttk.Button(photo_window,text='Next', command= next_photo)
    nextK.grid(column=1,row=1,sticky='se')
    #photo counter + exit button
    counter = ttk.Label(photo_window, text=str(imageCounter)+'/'+str(len(photosPath)), anchor='center')
    counter.grid(column=1,row=1,sticky='ne')
    returnB = ttk.Button(photo_window,text='EXIT', command= lambda: photo_window.destroy())
    returnB.grid(column=0,row=0,sticky='wn')

    display_image(imageCounter)
    
def display_image(photoNum):
    global photo_window
    global counter
    if(photoNum< len(photosPath)):
        loaded = Image.open(photosPath[photoNum])
        widthS=int(photo_window.winfo_width())
        heightS=int(photo_window.winfo_height())-int(counter.winfo_height())
        newLoadedPhoto= fit_image(loaded, widthS, widthS)
        photoLabel.config(text= None, image=newLoadedPhoto)
        photoLabel.image = newLoadedPhoto

def next_photo():
    global imageCounter
    global counter
    if(0<= imageCounter < len(photosPath)):
        imageCounter += 1
        display_image(imageCounter)
        counter.config(text=str(imageCounter)+'/'+str(len(photosPath)))
    else:
        print('no more photos')
    print(imageCounter)
    
def last_photo():
    global imageCounter
    global counter
    if(0< imageCounter <= len(photosPath)):
        imageCounter -= 1
        display_image(imageCounter)
        counter.config(text=str(imageCounter)+'/'+str(len(photosPath)))
    else:
        print('no more photos')
    print(imageCounter)

#detects which photo the app is viewing
imageCounter = 0

# get photos from certain folder change this to the folder you want
imageFolder="C:/Users/Gabi/Documents/KrillKam/Krill-Kam-/Screenshots"
photosPath = []
def get_photos(folder):
    for photo in os.listdir(folder):
        photo_end= os.path.splitext(photo)[1]
        if(photo_end.lower() in {'.png','.jpeg','.jpg'}):
            photoPath = os.path.join(folder, photo)
            photosPath.append(photoPath)
get_photos(imageFolder)

#center app on launch
def centerWindows(window):
    window.update_idletasks()
    screen_width=window.winfo_screenwidth()
    screen_height=window.winfo_screenheight()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (screen_width//2 - (width//2))
    y = (screen_height//2 - (height//2) )
    window.geometry(f"{width}x{height}+{x}+{y}")
    #window.attributes('-topmost', True)
    window.overrideredirect(True)
    window.bind('<Escape>',lambda event: root.destroy())
centerWindows(root)


#set background
blueBack=Image.open('GUIimages/blue-background.jpeg')
blueRatio = blueBack.size[0]/blueBack.size[1]
blueImage=ImageTk.PhotoImage(blueBack)

backgrounds= tk.Canvas(root,background='black', bd=0, highlightthickness=0, relief='ridge')

backgrounds.bind('<Configure>', lambda event: fill_image(event, blueBack,blueRatio))
backgrounds.grid(column=0, row=0, columnspan=root.grid_size()[0],rowspan=root.grid_size()[1], sticky='nsew')

#camera/photo sections (holds time, live preview, etc)
previewFrame=tk.Frame(root)
previewFrame.grid(column=1,row=0, rowspan=root.grid_size()[1], sticky='nesw')
previewFrame.columnconfigure((0,1,2),weight=1, uniform='a')
previewFrame.rowconfigure((0,2),weight=1, uniform='a')
previewFrame.rowconfigure(1,weight=4,uniform='a')

#Actual area for camera and photo preview to go
previewArea=tk.Frame(previewFrame, bg='black')
previewArea.grid(column=0,row=1, columnspan=previewFrame.grid_size()[0], rowspan=previewFrame.grid_size()[1], sticky='nesw')
previewArea.update()

#set up camera preview gotten from stack overflow for basics, plan to update later
cap = cv2.VideoCapture(0)
image_id = None
cameraLabel= ttk.Label(previewArea)
cameraLabel.pack(fill='both', expand=True)

#Clock feature
localTime= ttk.Label(previewFrame, background=None, foreground='black', font=('Courier New', 7))
localTime.grid(column=0,row=0,columnspan=previewFrame.grid_size()[0],sticky='nw')
time_now()

#Camera info text
fpsLabel = ttk.Label(previewFrame, foreground='black', font=('Courier New', 7))
fpsLabel.grid(column=0,row=2, sticky='ws')
fps_counter()

#Live Camera feed buttons
camera_buttons=[]
buttonFrame = tk.Frame(root)
buttonFrame.grid(column=0,row=0, rowspan=2, sticky='nesw')

capture=ttk.Button(buttonFrame, text='Capture')
camera_buttons.append(capture)

recPicStart= tk.PhotoImage('GUIimages/Icons/recordStart.png')
record=ttk.Button(buttonFrame,image=recPicStart )
camera_buttons.append(record)

reviewMode=ttk.Button(buttonFrame, text='Review', command=create_photo_window)
camera_buttons.append(reviewMode)

settings=ttk.Button(buttonFrame, text='settings')
camera_buttons.append(settings)

#Power button
powerOff= ttk.Button(root, text="Power", command=lambda:power_off())
powerOff.grid(column=0, row=2,sticky='ews')


for index, button in enumerate(camera_buttons):
    button.pack(fill='both',expand=True,padx=1,pady=1)

#krillCanvas= ttk.Canvas(root,background='blue')
#krillCanvas.grid(column=0,row=1,sticky='nesw')

#testing windows
#create_photo_window()
#power_off()

show_frame()
root.mainloop()
cap.release()