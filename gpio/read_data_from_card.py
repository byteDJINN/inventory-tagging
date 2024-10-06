import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
#from RPLCD import CharLCD
import RPi.GPIO as GPIO

#lcd = CharLCD(cols=16,rows=2,pin_rs=7,pin_e=5,pins_data=[6,12,22,18],numbering_mode=GPIO.BCM)
#lcd.write_string(u'Hello,world')
#GPIO.cleanedup()

reader = SimpleMFRC522()

print("place tour card")

id,text = reader.read()

print(f"Card ID : {id}")
print(f"Card text : {text}")

