from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/blog")
@login_required
def blog():
    return render_template("blog.html", name=current_user.username)

@views.route("/tips")
def tips():
    return render_template("tips.html")

@views.route("/home")
def home():
    return render_template("home.html")

