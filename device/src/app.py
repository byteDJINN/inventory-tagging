# Flask server

from flask import Flask, render_template, jsonify

app = Flask(__name__)

button_press_count = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/button-press', methods=['POST'])
def button_press():
    global button_press_count
    button_press_count += 1
    return jsonify({"success": True, "count": button_press_count}), 200

@app.route('/api/button-count', methods=['GET'])
def get_button_count():
    return jsonify({"count": button_press_count}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)