import requests

endpoint = "http://localhost:8000/api/products/1234567/" #http://127.0.0.1:8000

get_response =  requests.get(endpoint) 
print(get_response.json())
