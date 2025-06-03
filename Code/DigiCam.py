import time
import pygame
import gpiozero
from picamera2 import Picamera2, Preview

cam = Picamera2()

turnedOn = True
input("start")
cam.start_preview(Preview.QTGL)
cam.start()

input("stop")
cam.stop_preview()

#while True:
   # if(turnedOn):
  #      cam.start_preview(Preview.QTGL)
   # else:
   #     cam.stop_preview()
