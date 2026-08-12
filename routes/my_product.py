from flask import Flask, render_template, redirect, url_for, Blueprint, session
from db import get_connection


my_product_bp = Blueprint('my-product', __name__)


@my_product_bp.route('/my-product')
def my_product():


    if "user_id" not in session:
        return redirect(url_for("login.login"))

    conn = get_connection()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT * FROM product WHERE id_user = %s
        """, (session["user_id"])
    )

    products = cur.fetchall()


    cur.close()
    conn.close()


    return render_template("my-product.html", products=products)