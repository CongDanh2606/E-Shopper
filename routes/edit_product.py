from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_connection

edit_product_bp = Blueprint('edit_product', __name__)


@edit_product_bp.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit(id):

    if "user_id" not in session:
        return redirect(url_for("login.login"))

    conn = get_connection()
    cur = conn.cursor()


    if request.method == 'POST':

        title = request.form['title']
        price = request.form['price']

        cur.execute(
            """
            UPDATE product
            SET title = %s,
            price = %s
            WHERE id = %s
            AND id_user = %s
            """,
            (
                title,
                price,
                id,
                session["user_id"]
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('my-product.my_product'))

    cur.execute(
        """
        SELECT *
        FROM product
        WHERE id = %s
        AND id_user = %s
        """,
        (
            id,
            session["user_id"]
        )
    )

    product = cur.fetchone()

    cur.close()
    conn.close()

    
    if not product:
        return "Không tìm thấy sản phẩm hoặc bạn không có quyền sửa sản phẩm này."

    return render_template("edit-product.html",product=product)

