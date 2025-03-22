import requests

response = requests.post('http://127.0.0.1:8002/api/process', files={'image': open('pantry.png', 'rb')})
print(response.json())