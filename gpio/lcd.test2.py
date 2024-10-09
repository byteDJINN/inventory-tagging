from RPLCD import CharLCD
import RPi.GPIO as GPIO

lcd = CharLCD(cols=16,rows=2,pin_rs=7,pin_e=5,pins_data=[6,12,22,18],numbering_mode=GPIO.BCM)
lcd.write_string(u'Hello,world')
GPIO.cleanup()