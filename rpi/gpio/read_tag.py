import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
from time import sleep
import requests
from urllib.parse import quote

reader = SimpleMFRC522()

# Define the base URL of your PocketBase instance
base_url = 'https://inventory.bytedjinn.com/db'  # Replace with your PocketBase instance URL

# Define the collection from which you want to fetch data
collection = 'items'

def start_read_tag_id(socketio, led, lcd):
    tag_id = ""
    previous = "init"
    while True:
        sleep(0.5) # optimize performance
        tag_id,text = reader.read()
        if tag_id == previous:
            sleep(2)
            continue
        
        #database
        filter_value = quote(f"tagID='{tag_id}'")  # this line is used to standardize format to URL
        url = f"{base_url}/api/collections/{collection}/records?filter={filter_value}"


        response = requests.get(url)

        if response.status_code == 200:
            records = response.json()
            print("Records retrieved successfully:")
            item = records["items"]

        # fetch the item from cloud
    '''
    item = {
         "tag_id": "471580",
         "colour": "blue",
         "price": "24.90",
         "size": "XS",
         "category": "T-shirts",
         "brand": "Uniqlo",
         "title": "Uniqlo U AIRism Cotton Oversized Crew Neck Half Sleeve T-Shirt",
         }
    '''
        socketio.emit('scan', json.dumps(item))
        lcd.lcd_string(f"{item['name']}",lcd.LCD_LINE_1)                    
        lcd.lcd_string(f"A${item['price']}-{item['brand']}",lcd.LCD_LINE_2)  #cause there is no brand attribute, this needs to be changed to another attribute
        led.blink(0.1,0.1,2)
        
        previous = tag_id
        print(f"Card ID : {tag_id}")
#         print(f"Card text : {text}")
