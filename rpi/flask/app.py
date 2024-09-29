# Flask server
# python app.py & python GPIO_handler.py &

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

latest_device_data = {}
button_press_count = 0

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

if __name__ == '__main__':

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)