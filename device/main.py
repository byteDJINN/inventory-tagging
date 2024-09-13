import uuid
import base64
import requests
import sys


# Temporary for local development
SERVER_URL = 'http://host.docker.internal:5173'

tags = []

for i in range(3):
    tags.append(str(uuid.uuid4()))

if len(sys.argv) < 2:
    print("Usage: python main.py <image_path>")
    sys.exit(1)

imagePath = sys.argv[1]

base64Image = base64.b64encode(open(imagePath, "rb").read()).decode("utf-8")

# API endpoint
api_url = f"{SERVER_URL}/api/add-item"

# Prepare the payload
payload = {
    "base64Image": base64Image,
    "tags": tags
}

# Send POST request to the API
try:
    response = requests.post(api_url, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    print("Item added successfully!")
except requests.exceptions.RequestException as e:
    print(f"Error adding item: {e}")