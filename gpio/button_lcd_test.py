import RPi.GPIO as GPIO
from RPLCD import CharLCD
import time

#GPIO.setwarnings(False) #turn on if not working
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

print("Button + LCD Testing")

while True:
    if GPIO.input(21) == GPIO.HIGH:
        lcd = CharLCD(cols=16,rows=2,pin_rs=7,pin_e=5,pins_data=[6,12,22,18],numbering_mode=GPIO.BCM)
        lcd.write_string("Clicked btn display text 2asfdasf")
        GPIO.cleanup()
        time.sleep(0.3)
        print("Test Complete")
        

 
