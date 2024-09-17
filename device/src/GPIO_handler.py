import RPi.GPIO as GPIO
import requests
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 18  # Change this to your actual button pin
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

API_URL = "http://localhost:5000/api/button-press"

def button_callback(channel):
    try:
        response = requests.post(API_URL)
        if response.status_code == 200:
            print("Button press registered successfully")
        else:
            print(f"Failed to register button press. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending request: {e}")

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

print("GPIO handler running. Press CTRL+C to exit.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO handler stopped.")