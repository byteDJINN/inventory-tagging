# Flask server
# python app.py & python GPIO_handler.py &

import threading
import time
import json

from flask import Flask

app = Flask(__name__)

# Import routes will trigger the routes to be added to the Flask app
from app import routes



if __name__ == '__main__':

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)