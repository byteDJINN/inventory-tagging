import requests
from urllib.parse import quote

# Define the base URL of your PocketBase instance
base_url = 'https://inventory.bytedjinn.com/db'  # Replace with your PocketBase instance URL

# Define the collection from which you want to fetch data
collection = 'items'

tagid_value = 'hello'  # replace it with tagid

filter_value = quote(f"tagID='{tagid_value}'") 

# Full API URL for accessing the collection
url = f"{base_url}/api/collections/{collection}/records?filter={filter_value}"


response = requests.get(url)

if response.status_code == 200:
    records = response.json()
    print("Records retrieved successfully:")
    print(records["items"])
else:
    print(f"Failed to retrieve the records. Status code: {response.status_code}")