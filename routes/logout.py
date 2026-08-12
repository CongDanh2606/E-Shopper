from flask import Flask, redirect, Blueprint, url_for, session

logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
def logout():

    session.clear()

    return redirect(url_for("login.login"))