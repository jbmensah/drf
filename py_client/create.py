import requests

endpoint = "http://localhost:8000/api/products/" #http://127.0.0.1:8000

data = {
	"title": "Hello, CREATE MODEL MIXIN.",
	"price": 22.99
}

get_response =  requests.post(endpoint, json=data) 
print(get_response.json())
