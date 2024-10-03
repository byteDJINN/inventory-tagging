import RPi.GPIO as GPIO
from RPLCD import CharLCD
import subprocess
import time

# Importing from inventory and customer scripts.
from inventory import add_inventory
from customer import customer_checkout

# Setting up GPIO.
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # GPIO pin 21 for mode switching.

lcd = CharLCD(cols = 16, rows = 2, pin_rs = 7,pin_e = 5, pins_data = [6, 12, 22, 18], numbering_mode = GPIO.BCM)

# Initial mode set to Inventory.
mode = "Inventory"

def switch_mode():
    global mode
    lcd.clear()
    
    if mode == "Inventory":
        mode = "Customer"
        lcd.write_string("Customer Mode")
        
        product = input("Enter Product")
        quantity = int(input("Enter quantity"))
        
        procezz = subprocess.Popen(["python3", "/home/csseiot/Desktop/RFID/customer.py"], stdin = subprocess.PIPE)
        procezz.communicate(input = f"{product}/n{quantity}/n".encode())
    else:
        mode = "Inventory"
        lcd.write_string("Inventory Mode")
        
        product = input("Enter Product")
        quantity = int(input("Enter quantity"))
        
        process = subprocess.Popen(["python3", "/home/csseiot/Desktop/RFID/inventory.py"], stdin = subprocess.PIPE)
        process.communicate(input = f"{product}/n{quantity}/n".encode())

# Initial display on LCD
lcd.clear()
#subprocess.call(["python3", "/home/csseiot/Desktop/RFID/inventory.py"])
lcd.write_string("123 Inventory Mode")

#### Swtich Inventory Mode to Customer Mode.
try:
    while True:
        if GPIO.input(21) == GPIO.HIGH:
            switch_mode()
            time.sleep(0.5)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()


 


