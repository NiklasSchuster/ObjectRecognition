import requests
from datetime import datetime
import base64

url = "http://localhost:5000/exc3/image"

UUID = "UUID" + datetime.today().strftime('%Y%m%d%H:%M:%S')

with open("input_folder/000000000016.jpg", "rb") as image_file:
    img_encoded = base64.b64encode(image_file.read()).decode('utf-8')

data = {"id": UUID, "image_data": img_encoded}

response = requests.post(url, json=data)

print(f"status_code: {response.status_code}")
print(f"msg: {response.json()}")