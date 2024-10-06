import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
from time import sleep

reader = SimpleMFRC522()



def start_read_tag_id(socketio, led, lcd):
    tag_id = ""
    previous = "init"
    while True:
        sleep(0.5) # optimize performance
        tag_id,text = reader.read()
        if tag_id == previous:
            sleep(2)
            continue
        # request to databse and get some data here
        # code goes here
        # fetch the item from cloud
        item = {
         "tag_id": "471580",
         "colour": "blue",
         "price": "24.90",
         "size": "XS",
         "category": "T-shirts",
         "brand": "Uniqlo",
         "title": "Uniqlo U AIRism Cotton Oversized Crew Neck Half Sleeve T-Shirt",
         }

        item['tag_id'] = tag_id
        socketio.emit('scan', json.dumps(item))
        lcd.lcd_string(f"{item['title']}",lcd.LCD_LINE_1)
        lcd.lcd_string(f"A${item['price']}-{item['brand']}",lcd.LCD_LINE_2)
        led.blink(0.1,0.1,2)
        
        previous = tag_id
        print(f"Card ID : {tag_id}")
#         print(f"Card text : {text}")
