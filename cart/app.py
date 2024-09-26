from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

cart = [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1},
    {"product_id": 3, "quantity": 3},
    {"product_id": 4, "quantity": 2},
    {"product_id": 5, "quantity": 1}
]


@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart_items = []
    total_price = 0

    for item in cart:
        # Get details from product service
        response = requests.get(f'https://cmsc-401-assignment2.onrender.com/products/{item["product_id"]}')
        if response.status_code == 200:
            product_data = response.json().get('product', {})
            
            # Calculate item total price
            item_total = product_data.get('price', 0) * item['quantity']
            total_price += item_total

            cart_items.append({
                'product_name': product_data.get('title', 'Unknown'),
                'quantity': item['quantity'],
                'price': product_data.get('price', 0),
                'item_total': item_total
            })
        else:
            cart_items.append({
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'error': 'Product not found'
            })

    return jsonify({
        'user_id': user_id,
        'cart_items': cart_items,
        'total_price': total_price
    })

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)

    response = requests.get(f'https://cmsc-401-assignment2.onrender.com/products/{product_id}')
    if response.status_code != 200:
        return jsonify({"error": "Product not found"}), 404
    
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity
            break
    else:
        cart.append({"product_id": product_id, "quantity": quantity})

    return jsonify({
        "message": "Product added to cart",
        "product_id": product_id,
        "quantity_added": quantity
    }), 201

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    quantity = request.json.get('quantity', 1)

    response = requests.get(f'https://cmsc-401-assignment2.onrender.com/products/{product_id}')
    if response.status_code != 200:
        return jsonify({"error": "Product not found"}), 404
    
    for item in cart:
        if item['product_id'] == product_id:
            if item['quantity'] >= quantity:
                item['quantity'] -= quantity
                break
            else:
                return jsonify({"error": "Quantity it too high. Not enough in cart."}), 404

    return jsonify({"message": "Product removed from cart"})

if __name__ == '__main__':
    app.run(debug=True)