import pytesseract
import RPi.GPIO as GPIO
import time

text_one = pytesseract.image_to_string('/home/csseiot/Desktop/first_pic.jpg')

text = pytesseract.image_to_string('/home/csseiot/Desktop/first_pic_gray.jpg')
text_bi = pytesseract.image_to_string('/home/csseiot/Desktop/first_pic_bi.jpg')

print ("-----------")
print(text_one)
print ("-----------")
print(text)
print ("-----------")
print(text_bi)