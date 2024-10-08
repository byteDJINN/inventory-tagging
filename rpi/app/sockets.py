import json
import threading
import time
from app import app
from flask_socketio import SocketIO

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

@socketio.on('receive')
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
        x[-1]['product_id'] = str(int(x[-1]['product_id']) + 1)
        x[-1]['price'] = str(float(x[-1]['price']) + 1)
        socketio.emit('scan', json.dumps(x[-1])  )
thread = threading.Thread(target=background_task)
thread.daemon = True
thread.start()