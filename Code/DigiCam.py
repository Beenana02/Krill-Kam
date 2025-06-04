from time import strftime
import pygame
from gpiozero import Button
from picamera2 import Picamera2, Preview



cam = Picamera2()
previewB = Button(14)
photoB = Button(15)

#set preview parameters
#previewPara = cam.create_preview_configuration(Preview.QT)


turnedOn = True

cam.start_preview(Preview.QTGL)
cam.start(show_preview=True)


def capture():
    cam.capture_file('/home/krill/camera/{strftime("%Y%m%d-%H%M%S")}.jpg')

while True:
    if previewB.is_pressed:
        if(turnedOn == True):
            turnedOn = False
            cam.stop_preview()
        elif(turnedOn == False):
            turnedOn = True
            cam.start_preview(Preview.QTGL)
    if(turnedOn == True):
        photoB.when_pressed = capture