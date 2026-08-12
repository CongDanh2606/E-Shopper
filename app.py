from flask import Flask
from datetime import timedelta
from routes.login import login_bp
from routes.register import register_bp
from routes.logout import logout_bp
from routes.home import home_bp
from routes.account import account_bp
from routes.my_product import my_product_bp
from routes.add_product import add_product_bp
from routes.edit_product import edit_product_bp
from routes.delete_product import delete_product_bp
from routes.index import index_bp
from routes.cart import cart_py

app = Flask(__name__)


app.secret_key = 'my_online_shop'
app.permanent_session_lifetime = timedelta(minutes=30)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(home_bp)
app.register_blueprint(account_bp)
app.register_blueprint(my_product_bp)
app.register_blueprint(add_product_bp)
app.register_blueprint(edit_product_bp)
app.register_blueprint(delete_product_bp)
app.register_blueprint(index_bp)
app.register_blueprint(cart_py)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)    