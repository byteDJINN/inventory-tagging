#----error
import cv2
import pytesseract
from picamera2 import Picamera2

picam2 = Picamera2
picam2.configure(picam2.create_still_configuration())

picam2.start()
picam2.capture_file("image_first.jpg")
picam2.stop()


image = cv2.imread("image_first.jpg")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

text= pytesseract.image_to_string(gray_image)

print("rego text")
print(text)

cv2.imshow('cap img', gray_image)
cv2.waitKey(0)
cv2.destoryALLWindows()