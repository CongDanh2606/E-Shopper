from flask import Flask, Blueprint, request, session, redirect, url_for, render_template
import re
from werkzeug.security import check_password_hash
from db import get_connection


login_bp = Blueprint('login', __name__)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

@login_bp.route('/login', methods=['POST', 'GET'])
def login():

    errors = {}
    email_login = ""
    password_login = ""

    if request.method == "POST":
        email_login = request.form.get("email_login", "").strip()
        password_login = request.form.get("password_login", "").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
                "SELECT * FROM user WHERE email = %s", (email_login,)
            )
        
        user = cur.fetchone()


        if not email_login: 
            errors['email_login'] = "Vui lòng nhập email!"

        elif not is_valid_email(email_login):
            errors['email_login'] = "Email không hợp lệ!"

        elif not user:
            errors['email_login'] = "Email không tồn tại!"

        elif not password_login:
            errors['password_login'] = "Vui lòng nhập mật khẩu!"

        elif not check_password_hash(user['password'], password_login):
            errors['password_login'] = "Mật khẩu không đúng!"

        if not errors:
            session.permanent = True

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            cur.close()
            conn.close()

            return redirect(url_for("home.home"))

    return render_template("login-register.html", errors=errors, email_login=email_login)