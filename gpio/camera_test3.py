## ---- This work
from picamera2 import Picamera2
import time

camera = Picamera2()

config = camera.create_still_configuration()
camera.configure(config)

camera.start()
time.sleep(2)


camera.set_controls({"AfTrigger" :1})
time.sleep(2)

print("ready to take picture")
camera.capture_file('/home/csseiot/Desktop/first_pic.jpg')
camera.stop()

'''
text= pytesseract.image_to_string(gray_image)
print("rego text")
print(text)
'''