# convert the origianl image to gray image and binary image

import pytesseract as pt
from PIL import Image

image_path = "/home/csseiot/Desktop/first_pic.jpg"

img = Image.open(image_path)

gray_img = img.convert('L')

binary_image = gray_img.point(lambda x:0 if x < 128 else 255, '1')

gray_img.save("/home/csseiot/Desktop/first_pic_gray.jpg")
binary_image.save("/home/csseiot/Desktop/first_pic_bi.jpg")
#gray_img.show()
#binary_image.show()

#text = pt.image_to_string(img)

#print("printing")
#print(text)