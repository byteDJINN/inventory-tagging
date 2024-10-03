import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    data = input("Enter the data to write to the card")
    print("Place your card near the reader...")
    reader.write(str(data))
    print("Data written successfully")
finally:
    GPIO.cleanup()
