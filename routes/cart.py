from flask import Flask, Blueprint, render_template, request, jsonify, session, redirect, url_for
from db import get_connection


cart_py = Blueprint('cart', __name__)


@cart_py.route('/cart', methods=['POST'])
def add_to_cart():

    product_id = request.json.get('product_id')

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM product WHERE id = %s", (product_id,)
    )
    product = cur.fetchone()

    if not product: 
        return jsonify({
            'status': 'fail',
            'message': 'Product not found'
        }), 404

    cart = session.get('cart', [])

    cur.close()
    conn.close()

    found = False 

    for item in cart:
        if item['id'] == product_id:
            item['qty'] += 1
            found = True
            break


    if not found:
        product_data = {
            'id': product['id'],
            'title': product['title'],
            'price': float(product['price']),
            'image': product['image'],
            'qty': 1
        }

        cart.append(product_data)

    session['cart'] = cart

    return jsonify({
        'status': 'success',
        'product': session['cart']
    })

@cart_py.route('/show-cart')
def show_cart():

    cart = session.get('cart', [])

    return render_template('cart.html', products=cart)