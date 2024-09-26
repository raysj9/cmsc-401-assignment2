from flask import Flask, jsonify, request
app = Flask(__name__)

products = [
    {"id": 1, "title": "Apple", "price": 2, "stock": 22},
    {"id": 2, "title": "Eggs", "price": 4, "stock": 63},
    {"id": 3, "title": "Lettuce", "price": 5, "stock": 6},
    {"id": 4, "title": "Orange Juice", "price": 3, "stock": 29},
    {"id": 5, "title": "Turkey", "price": 50, "stock": 12}
]

# Endpoint 1: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})

# Endpoint 2: Get product details by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return jsonify({"product": product})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Add a new product
@app.route('/products', methods=['POST'])
def create_product():
    new_product = {
        "id": len(products) + 1,
        "title": request.json.get('title'),
        "price": request.json.get('price'),
        "stock": request.json.get('stock')
    }
    products.append(new_product)
    return jsonify({"message": "Product created", "product": new_product}), 201

if __name__ == '__main__':
    app.run(debug=True)