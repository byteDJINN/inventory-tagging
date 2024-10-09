import requests

# Define the base URL of your PocketBase instance
base_url = 'https://inventory.bytedjinn.com/db'  # Replace with your PocketBase instance URL

# Define the collection from which you want to fetch data
collection = 'items'

# Full API URL for accessing the collection
url = f"{base_url}/api/collections/{collection}/records"

# Make a GET request to retrieve records from the collection
response = requests.get(url)


# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    print("Data retrieved successfully:")
    print(data["items"])
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
for record in data['items']:
    print(f"Product: {record['name']}, Price: {record['price']}")