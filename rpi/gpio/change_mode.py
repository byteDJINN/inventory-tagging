import threading
from gpiozero import Button, LED
from time import time,sleep

from app.sockets import socketio
print("sadfasdf")


led = LED(11)
btn = Button(4)
led.on()
btn.wait_for_press()
led.off()

def switch_mode(flag:list,socketio):
    flag.append(1)
    if len(flag) > 2:
        flag.clear()
    index  = len(flag)
    mode=[{'mode':'query'},{'mode':'inventory'},{'mode':'checkout'}]
    socketio.emit('mode_change', mode[index]['mode'] )


def listen_button_press(socketio,btn, led):
    flag = []
    switch_mode(flag,socketio)
    while True:
        print("mode21")
        sleep(2)
#         led.on()
#         start = time()
#         btn.wait_for_press()
#         led.off()
#         end = time()
#         print(end-start)

thread = threading.Thread(target=listen_button_press, args=(socketio,btn,led))

thread.daemon = True
thread.start()
