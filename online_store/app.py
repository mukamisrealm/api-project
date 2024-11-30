from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the 'products' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Call the function to initialize the database
try:
    init_db()
except Exception as e:
    print(f"Error initializing database: {e}")

# Endpoint to fetch all products
@app.route('/products', methods=['GET'])
def get_products():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Execute a query to fetch all products
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    # Create a list of dictionaries to store product data
    product_list = [
        {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
        for row in products
    ]

    # Close the connection to the database
    conn.close()

    # Return the list of products in JSON format
    return jsonify(product_list)

# Endpoint to create a new product
@app.route('/products', methods=['POST'])
def create_product():
    # Get the JSON data from the request body
    data = request.json
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')

    # Check if name and price are provided
    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert the new product into the database
    cursor.execute(
        "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
        (name, description, price),
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({"message": "Product created successfully"}), 201

# Endpoint to update an existing product
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Get the JSON data from the request body
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Update the product in the database
    cursor.execute(
        """
        UPDATE products
        SET name = ?, description = ?, price = ?
        WHERE id = ?
        """,
        (name, description, price, product_id),
    )

    # Check if the product was updated
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({"message": "Product updated successfully"}), 200

# Endpoint to delete a product
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Delete the product from the database
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    # Check if the product was deleted
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    # Return a success message
    return jsonify({"message": "Product deleted successfully"}), 200

# Basic home endpoint
@app.route('/')
def home():
    return "Welcome to the Online Store Inventory API!"

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
