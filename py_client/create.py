import requests

headers = {'Authorization': 'Bearer 80d48ec3de9d2d9d3d9f8424a9a99178143d7a65'}
endpoint = "http://localhost:8000/api/products/" #http://127.0.0.1:8000

data = {
	"title": "Hello, with old token.",
	"price": 20.00
}

get_response =  requests.post(endpoint, json=data, headers=headers) 
print(get_response.json())
