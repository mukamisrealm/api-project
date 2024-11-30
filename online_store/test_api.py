import requests
import json

# Set the base URL of the Flask API
base_url = 'http://127.0.0.1:5000/products'

# ----------- 1. Test POST (Create a Product) -----------
def create_product():
    data = {
        "name": "Smartphone",
        "description": "A new smartphone",
        "price": 699.99
    }
    response = requests.post(base_url, json=data)
    print("POST Status Code:", response.status_code)
    print("POST Response Body:", response.json())

# ----------- 2. Test GET (Get all products) -----------
def get_products():
    response = requests.get(base_url)
    print("GET Status Code:", response.status_code)
    print("GET Response Body:", response.json())

# ----------- 3. Test PUT (Update a Product) -----------
def update_product(product_id):
    data = {
        "name": "Updated Smartphone",
        "description": "An upgraded smartphone",
        "price": 799.99
    }
    url = f"{base_url}/{product_id}"
    response = requests.put(url, json=data)
    print("PUT Status Code:", response.status_code)
    print("PUT Response Body:", response.json())



# ------------ Run the tests ------------

# 1. Create a new product
create_product()

# 2. Get all products (to see if the new product is added)
get_products()

# 3. Update the product with ID 1 (change ID to one that exists in your database)
update_product(1)


