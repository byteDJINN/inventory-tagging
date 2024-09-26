# Flask server
# python app.py & python GPIO_handler.py &

from flask import Flask, render_template, jsonify,request

app = Flask(__name__)

latest_device_data = {}

# Endpoint to receive data from devices
@app.route('/receive-data', methods=['POST'])
def receive_data():
    global latest_device_data
    device_data = request.json  # Get JSON data from POST request
    latest_device_data = device_data  # Update latest data
    print(f'Received data from device: {device_data}')
    return jsonify({'message': 'Data received successfully'})

# Endpoint to serve the frontend and return the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to send data to the frontend
@app.route('/get-data', methods=['GET'])
def get_data():
    # Send the latest device data to the frontend as JSON
    return jsonify(latest_device_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)