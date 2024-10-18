import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
from time import sleep
import requests
from requests.utils import quote
reader = SimpleMFRC522()

# Define the base URL of your PocketBase instance
base_url = 'https://inventory.bytedjinn.com/db'  # Replace with your PocketBase instance URL

# Define the collection from which you want to fetch data
collection = 'items'

def start_read_tag_id(socketio, led, lcd):
    tag_id = ""
    while True:
        sleep(0.5) # optimize performance
        tag_id,text = reader.read()
        tag_id = str(tag_id)
        tag_id = tag_id.zfill(15)
        #database

        # this line is used to standardize format to URL
        url = f"{base_url}/api/collections/{collection}/records/{tag_id}"

        
        response = requests.get(url)

        if response.status_code == 200:
            print("Records retrieved successfully:")
            records = response.json()
            print(json.dumps(records))
           
            socketio.emit('scan', json.dumps(records))

            item = records
            name = item["name"]
            
            lcd.lcd_string(f"{item['name']}",lcd.LCD_LINE_1)                    
            lcd.lcd_string(f"A${item['price']}-{item['name']}",lcd.LCD_LINE_2)  #cause there is no brand attribute, this needs to be changed to another attribute
            led.blink(0.1,0.1,2)
            filter_value = f"(name='{quote(name)}')"
            
            
            url = f"{base_url}/api/collections/{collection}/records?filter={filter_value}"
            response = requests.get(url)
            records = response.json()
            items = records["items"]
            print(json.dumps(items))
            socketio.emit('scan_q', json.dumps(items))

        # fetch the item from cloud
            
            
        
        else:
            lcd.lcd_string("Tag ID:", lcd.LCD_LINE_1)
            lcd.lcd_string(f"{tag_id}",lcd.LCD_LINE_2)
            socketio.emit('scan', tag_id)
        print(f"Card ID : {tag_id}")
        #print(f"Card text : {text}")
