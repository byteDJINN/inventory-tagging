from app import app
from app import sockets
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

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(latest_device_data)

@app.route('/api/button-press', methods=['POST'])
def button_press_api():
    global button_press_count
    button_press_count += 1
    print(f"Button press registered. Total count: {button_press_count}")
    return jsonify({'message': 'Button press registered successfully'})
