from app import app
from flask import render_template, jsonify, request
from gpio.camera import camera
from gpio.ocr import submit_text
from libcamera import controls
import threading
from app.sockets import socketio

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

@app.route('/capture', methods=['GET'])
def capture():
#     path = "/home/csseiot/Desktop/xxx.jpg"
#     camera.capture_file(path)
#     camera.stop_preview()
#     camera.stop()
    submit_text(socketio)
    
    return jsonify({'message': 'camera stop'})
    
@app.route('/start-cam', methods=['GET'])
def start_cam():
    camera.start(show_preview=True)
    camera.set_controls({
        "AfMode": controls.AfModeEnum.Continuous,
        "AfSpeed": controls.AfSpeedEnum.Fast
        })
    return jsonify({'message': 'camera start'})
    
# @app.route('/stop-cam', methods=['GET'])
# def stop_cam()

    return jsonify({'message': 'Capture successfully'})



