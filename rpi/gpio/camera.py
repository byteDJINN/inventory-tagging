from picamera2 import Picamera2
from libcamera import controls
import time
camera = Picamera2()
# camera.configure(camera.create_video_configuration(main={"size": (1920, 1200)}))




if __name__ == '__main__':
    print(__name__)
    path = "/home/csseiot/Desktop/xxx.jpg"
    camera.start(show_preview=True)
    camera.set_controls({
    "AfMode": controls.AfModeEnum.Continuous,
    "AfSpeed": controls.AfSpeedEnum.Fast
    })
    time.sleep(3)
    camera.capture_file(path)
    camera.stop_preview()
    camera.stop()

    
    
    