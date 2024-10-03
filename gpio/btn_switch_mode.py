import RPi.GPIO as GPIO
from RPLCD import CharLCD
import subprocess
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

lcd = CharLCD(cols = 16, rows = 2, pin_rs = 7,pin_e = 5, pins_data = [6, 12, 22, 18], numbering_mode = GPIO.BCM)

mode = "Inventory"

def switch_mode():
    global mode
    if mode == "Inventory":
        mode = "Customer"
        lcd.clear()
        lcd.write_string("Customer Mode")
        subprocess.call(["python3", "/home/csseiot/Desktop/RFID/customer.py"])
    else:
        mode = "Inventory"
        lcd.clear()
        lcd.write_string("Inventory Mode")
        subprocess.call(["python3", "/home/csseiot/Desktop/RFID/inventory.py"])

# Initial display
subprocess.call(["python3", "/home/csseiot/Desktop/RFID/inventory.py"])
lcd.write_string("123 Inventory Mode")

#### Swtich Inventory Mode to Customer Mode.
try:
    while True:
        if GPIO.input(21) == GPIO.HIGH:
            switch_mode()
            time.sleep(0.5)
        
        while GPIO.input(21) == GPIO.HIGH:
            time.sleep(0.1)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()
