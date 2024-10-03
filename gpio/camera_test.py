from picamera2 import Picamera2
import time

camera = Picamera2()
config = camera.create_still_configurarion()
camera.configure(config)

camera.start()
time.sleep(2)
print("ready to take picture")
camera.capture_file('/Firstpic,jpg')
camera.stop()
  