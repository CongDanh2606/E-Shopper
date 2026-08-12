from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, current_app
from db import get_connection
import os


add_product_bp = Blueprint('add_product', __name__)


ALLOWED_FILE_EXTENSION = ['jpg', 'jpeg', 'png', 'gif']


def allowed_file_name(filename):
    return (
        '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSION
    )


@add_product_bp.route('/add-product', methods=['GET', 'POST'])
def add_product():

    errors = {}

    if "user_id" not in session:
        return redirect(url_for("login.login"))


    if request.method == 'POST':
        title = request.form.get("title", "").strip()
        price = request.form.get("price", "").strip()
        image = request.files.get("image")

        if not title:
            errors['title'] = "Vui lòng nhập tên sản phẩm!"

        if not price:
            errors['price'] = "Vui lòng nhập giá sản phẩm!"

        if not image or image.filename == "":
            errors['image'] = "Vui lòng chọn ảnh sản phẩm!"

        elif not allowed_file_name(image.filename):
            errors['image'] = "Ảnh không đúng định dạng (jpg, jpeg, png, gif)"

        if not errors:

            upload_folder = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "product"
            )

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            image_path = os.path.join(
                upload_folder,
                image.filename
            )

            image.save(image_path)

            image_db = f"uploads/product/{image.filename}"

            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                    INSERT INTO product
                    (id_user, title, price, image)
                    VALUES (%s, %s, %s, %s)
                """,
                (
                    session['user_id'],
                    title,
                    price,
                    image_db
                )
            )

            conn.commit()

            cur.close()
            conn.close()

            return redirect(url_for("my-product.my_product"))

    return render_template('add-product.html', errors=errors)
