print('sockets.py')
# import json
import threading
import time
from app import app
from flask_socketio import SocketIO
import enum
from time import time,sleep

from gpiozero import Button, LED
import gpio.lcd_screen as lcd
import gpio.read_tag as tag

led = LED(2)
btn = Button(3)
 
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


# def background_task():
#     """Example of how to send server-generated events to clients."""
#     while True:
#         x[-1]['product_id'] = str(int(x[-1]['product_id']) + 1)
#         x[-1]['price'] = str(float(x[-1]['price']) + 1)
#         socketio.emit('scan', json.dumps(x[-1])  )
#         # socketio.emit("change_mode","checkout")
#         time.sleep(1)
# thread = threading.Thread(target=background_task)
# thread = threading.Thread(target=)

#thread.daemon = True
#thread.start()
def switch_mode(flag:list,socketio):
    flag.append(1)
    if len(flag) > 2:
        flag.clear()
    index  = len(flag)
    mode=[{'mode':''},{'mode':'checkout'},{'mode':'add-product'}]
    text = mode[index]['mode']
    socketio.emit('change_mode', text )
    if text == '':
        text = 'Query'
 
    lcd.lcd_string("Mode:",lcd.LCD_LINE_1)
    lcd.lcd_string(text,lcd.LCD_LINE_2)

def listen_button_press(socketio,btn, led):
    flag = []
    while True:
        btn.wait_for_press()
        sleep(0.2)
        switch_mode(flag,socketio)
        
        led.blink(0.1,0.1,3)



#btn.wait_for_press()


thread_scan = threading.Thread(target=tag.start_read_tag_id, args=(socketio,led,lcd))
thread_scan.daemon = True
thread_scan.start()

thread = threading.Thread(target=listen_button_press, args=(socketio,btn,led))
thread.daemon = True
thread.start()
