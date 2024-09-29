# Flask server
# python app.py & python GPIO_handler.py &

from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import threading
import time

app = Flask(__name__)

latest_device_data = {}
button_press_count = 0

# GPIO setup
GPIO.setmode(GPIO.BOARD)
BUTTON_PIN = 12
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Flask routes
@app.route('/receive-data', methods=['POST'])
def receive_data():
    global latest_device_data
    device_data = request.json
    latest_device_data = device_data
    print(f'Received data from device: {device_data}')
    return jsonify({'message': 'Data received successfully'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(latest_device_data)

@app.route('/api/button-press', methods=['POST'])
def button_press_api():
    global button_press_count
    button_press_count += 1
    print(f"Button press registered. Total count: {button_press_count}")
    return jsonify({'message': 'Button press registered successfully'})

# GPIO handler function
def gpio_handler():
    global button_press_count
    print("GPIO handler running. Press CTRL+C to exit.")
    try:
        button_state = GPIO.input(BUTTON_PIN)
        while True:
            new_state = GPIO.input(BUTTON_PIN)
            if new_state != button_state:
                if new_state == GPIO.LOW:
                    button_press_count += 1
                    print(f"Button pressed. Total count: {button_press_count}")
                button_state = new_state
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("GPIO handler stopped.")

if __name__ == '__main__':
    # Start GPIO handler in a separate thread
    gpio_thread = threading.Thread(target=gpio_handler, daemon=True)
    gpio_thread.start()

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)