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

@cart_py.route('/cart-action', methods=['POST']) 
def cart_action():

    data = request.get_json()

    product_id = str(data.get('product_id'))

    action = int(data.get('action'))

    cart = session.get('cart', [])

    product = None

    for item in cart:

        if str(item['id']) == product_id:

            product = item

            break

    if product is None:

        return jsonify({

            'status': 'fail', 

            'message': 'Sản phẩm không có trong giỏ hàng'
            
        })

    if action == 1:

        product['qty'] += 1

    elif action == 2:

        if product['qty'] >= 2:

            product['qty'] -= 1

        else:

            return jsonify({
                'status': 'fail',
                'message': 'Không thể xóa sản phẩm số lượng nhỏ hơn 1'
            })

    elif action == 3:

        cart.remove(product)

        session['cart'] = cart
        session.modified = True

        return jsonify({
            'status': 'success',
            'action': 3
        })

    else:

        return jsonify({
            'status': 'fail',
            'message': 'Yêu cầu không hợp lệ!'
        })

    session['cart'] = cart

    session.modified = True

    price = float(product['price'])

    qty = product['qty']

    total = price * qty

    sub_total = 0 

    for item in cart:

        item_price = float(item['price'])

        item_qty = item['qty']

        sub_total += item_price * item_qty

    cart_total = sub_total + 2

    return jsonify({

        'status': 'success',

        'product_id': product_id,

        'qty': qty,

        'total': total,

        'sub_total': sub_total,

        'cart_total': cart_total

    })

@cart_py.route('/show-cart')
def show_cart():

    cart = session.get('cart', [])

    return render_template('cart.html', products=cart)