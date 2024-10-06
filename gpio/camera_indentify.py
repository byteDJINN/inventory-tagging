from picamera2 import Picamera2
import RPi.GPIO as GPIO
import time


def camera_indentify():   
    camera = Picamera2()
    config = camera.create_still_configuration()
    camera.configure(config)
    camera.start()
    time.sleep(2)
    print("ready to take picture")
    camera.capture_file('/home/csseiot/Desktop/Firstpic.jpg')
    camera.stop()


    text= pytesseract.image_to_string(gray_image)
    print("rego text")
    print(text)

if 




