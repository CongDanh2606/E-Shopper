from flask import Blueprint, render_template, session
from db import get_connection

index_bp = Blueprint('index', __name__)


@index_bp.route('/index')
def index():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM product
    """)

    products = cur.fetchall()

    cart = session.get('cart', [])

    cart_count = sum(item['qty'] for item in cart)

    cur.close()
    conn.close()

    return render_template(
        'index.html',
        products=products,
        cart_count=cart_count
    )