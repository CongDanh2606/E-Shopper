from flask import Flask, Blueprint, render_template, request, current_app
import re
import os
from werkzeug.security import generate_password_hash
from db import get_connection


register_bp = Blueprint('register', __name__)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)


ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'gif'}
MAX_FILE_SIZE = 1

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@register_bp.route('/register', methods=['GET', 'POST'])
def register():

    errors = {}
    name = ""
    email = ""
    password = ""
    file = ""


    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        file = request.files.get('avatar')

        if not name:
            errors['name'] = "Vui lòng nhập tên!"

        if not email:
            errors['email'] = "Vui lòng nhập email!"
        elif not is_valid_email(email):
            errors['email'] = "Email không hợp lệ!"

        if not password:
            errors['password'] = "Vui lòng nhập mật khẩu!" 

        if not file or file.filename == "":
            errors['file'] = "Vui lòng chọn một file!"

        elif not allowed_file(file.filename):
            errors['file'] = "Chỉ chấp nhận file ảnh (png, jqg, jqeg, gif)!"

        else: 
            file.seek(0, os.SEEK_END)
            file.size = file.tell()
            file.seek(0)

            if file.size > MAX_FILE_SIZE * 1024 * 1024:
                errors['file'] = "File quá lớn!"

        if not errors:
            hashed_password = generate_password_hash(password)

            UPLOAD_FOLDER = os.path.join(current_app.root_path, "static", "uploads", "avatar")

            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            avatar = f"uploads/avatar/{file.filename}"

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO user (email, password, name, avatar) VALUES (%s, %s, %s, %s)", (email, hashed_password, name, avatar)
            )

            conn.commit()

            cur.close()
            conn.close()

    return render_template('login-register.html', errors=errors, name=name, email=email)