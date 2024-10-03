# customer.py
import time
import requests

reader = SimpleMFRC522()
url_cus = "http://flask/get-data-from-database"
data_cus = {}
def customer_checkout():
    print("This is Customer Mode")
    print("place tour card")
    id_cus,text = reader.read()
    
    result = await pb.collection("item").getList(1,50,{filter:f'id = "{id_cus}"'}) 
    price = result['items'][0]
    response = request.post(url,json=data_cus)
    
    
    #product = input("Enter product name: ")
    
    #print(product)
    #product = input("Enter Product Name: ")
    #quantity = int(input("Enter quantity to add: "))
    
    #price = float(input("Enter price per item: "))
    
    #print(f"Customer: Product - {product}, Quantity - {quantity}")
    
if __name__ == "__main__":
    customer_checkout()