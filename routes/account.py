from flask import Flask, Blueprint, render_template, session, url_for, redirect, request
from db import get_connection
from werkzeug.security import generate_password_hash
import re


account_bp = Blueprint('account', __name__)


@account_bp.route('/account', methods=['POST', 'GET'])
def update():

    if "user_id" not in session:
        return redirect(url_for("login.login"))

    conn = get_connection()
    cur = conn.cursor()


    errors = {}
    success = ""

    if request.method == 'POST':

        name = request.form.get("name", "")
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.match(pattern, email):
            errors['email'] = "Email không hợp lệ!"

        if not errors:


            if password:
                hashed_password = generate_password_hash(password)

        

                cur.execute(
                    """UPDATE user SET name = %s, email = %s, password = %s WHERE id = %s""", (name, email, hashed_password, session["user_id"])
                )


            else: 
                cur.execute(
                    """UPDATE user SET name = %s, email = %s WHERE id = %s""", (name, email, session["user_id"])
                )

            conn.commit()

            success = "Cập nhật thông tin thành công!"

    cur.execute(
        "SELECT * FROM user WHERE id = %s", (session["user_id"],)
    )
            
    user = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("account.html", user=user, errors=errors, success=success)