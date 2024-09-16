import uuid
import base64
import requests
import sys


# Temporary for local development
SERVER_URL = 'http://host.docker.internal:5173'

tags = []

for i in range(3):
    tags.append(str(uuid.uuid4()))

# API endpoint
api_url = f"{SERVER_URL}/api/add-item"

# Prepare the payload
payload = {
    "name": "Test Item",
    "tags": tags
}

# Send POST request to the API
try:
    response = requests.post(api_url, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    print("Item added successfully!")
except requests.exceptions.RequestException as e:
    print(f"Error adding item: {e}")