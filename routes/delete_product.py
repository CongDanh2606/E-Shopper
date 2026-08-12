from flask import Blueprint, redirect, url_for, session
from db import get_connection

delete_product_bp = Blueprint('delete_product', __name__)


@delete_product_bp.route('/delete-product/<int:id>')
def delete(id):


    if "user_id" not in session:
        return redirect(url_for("login.login"))

    conn = get_connection()
    cur = conn.cursor()


    cur.execute(
        """
        DELETE FROM product
        WHERE id = %s
        AND id_user = %s
        """,
        (
            id,
            session["user_id"]
        )
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('my-product.my_product'))

