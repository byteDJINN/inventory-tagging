# Flask server
# python app.py & python GPIO_handler.py &
import threading
import time
import json
from flask import render_template, jsonify, request
from flask import Flask
import json
import threading
import time
from flask_socketio import SocketIO


app = Flask(__name__)

# Import routes will trigger the routes to be added to the Flask app

from flask import render_template, jsonify, request


latest_device_data = {}
button_press_count = 0

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

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/add-product')
def add_product():
    return render_template('add_inventory.html')


@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(latest_device_data)

@app.route('/api/button-press', methods=['POST'])
def button_press_api():
    global button_press_count
    button_press_count += 1
    print(f"Button press registered. Total count: {button_press_count}")
    return jsonify({'message': 'Button press registered successfully'})

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    # Handle incoming message from the client
    print('Received message:', message)
    # Perform necessary actions or send a response

@socketio.on('connect')
def handle_connect():
    # Handle client connection
    print('Client connected')
    # socketio.emit('scan', 'asdfasfwf23!!@')
    # Perform necessary actions

# Define more event handlers as needed

@socketio.on('scan')
def handle_checkout(message):
    # Handle incoming message from the client
    print('Received message:', message)
    # Perform necessary actions or send a response

x = [{
     "product_id": "471580",
     "colour": "blue",
     "price": "24.90",
     "size": "XS",
     "category": "T-shirts",
     "brand": "Uniqlo",
     "title": "Uniqlo U AIRism Cotton Oversized Crew Neck Half Sleeve T-Shirt",
     }]
def background_task():
    """Example of how to send server-generated events to clients."""
    while True:
        x[-1]['product_id'] = str(int(x[-1]['product_id']) + 1)
        x[-1]['price'] = str(float(x[-1]['price']) + 1)
        socketio.emit('scan', json.dumps(x[-1])  )
        time.sleep(1)
thread = threading.Thread(target=background_task)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    