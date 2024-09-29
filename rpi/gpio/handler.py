import RPi.GPIO as GPIO
import requests
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD) # BOARD or BCM
BUTTON_PIN = 12  # Change this to your actual button pin in BOARD numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

API_URL = "http://localhost:5000/api/button-press"

def button_press():
    try:
        response = requests.post(API_URL)
        if response.status_code == 200:
            print("Button press registered successfully")
        else:
            print(f"Failed to register button press. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending request: {e}")

print("GPIO handler running. Press CTRL+C to exit.")
try:
    button_state = GPIO.input(BUTTON_PIN)
    while True:
        new_state = GPIO.input(BUTTON_PIN)
        if new_state != button_state:
            if new_state == GPIO.LOW:
                button_press()
            button_state = new_state
        time.sleep(0.5)  # Small delay to prevent excessive CPU usage
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO handler stopped.")