from time import strftime
import pygame
from gpiozero import Button
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder



cam = Picamera2()
previewB = Button(14)
photoB = Button(15)
videoB = Button(18)

#set preview parameters
#previewPara = cam.create_preview_configuration(Preview.QT)
video_config = cam.create_video_configuration()
cam.configure(video_config)
encoder = H264Encoder()


turnedOn = True
recording = False

cam.start_preview(Preview.QTGL)
cam.start(show_preview=True)


def capture():
    currentTime= strftime("%d-%m-%y-%I:%M:%S")
    #make sure to change this to your wanted save location
    cam.capture_file('/home/krill/camera/'+currentTime+'.jpg')
def video_capture():
    if(recording == True):
        currentTime= strftime("%d-%m-%y-%I:%M:%S")
        cam.start_recording(encoder, '/home/krill/camera/'+currentTime+'.h264')
    elif(recording == False):
        cam.stop_recording()




while True:
    if previewB.is_pressed:
        if(turnedOn == True):
            turnedOn = False
            cam.stop_preview()
        elif(turnedOn == False):
            turnedOn = True
            cam.start_preview(Preview.QTGL)
    if videoB.is_pressed:
        video_capture()
        if(recording == True):
            recording = False
        elif(recording == False):
            recording = True
    if(turnedOn == True and recording == False):
        photoB.when_pressed = capture