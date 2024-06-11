from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)  # Fix: Passing the name explicitly

@auth.route("/Login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash("Welcome back radiant skin seekers!", category='success')
            return redirect(url_for('views.blog'))
        else:
            flash('Password is incorrect.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/Signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if User.query.filter_by(email=email).first():
            flash('Email is already in use.', category='error')
        elif User.query.filter_by(username=username).first():
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        elif len(username) < 6 or len(password1) < 6:
            flash('Username and Password should be at least 6 characters long.', category='error')
        elif len(email) < 4 or '@' not in email or '.' not in email:
            flash("Invalid email.", category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created successfully!', category='success')
            return redirect(url_for('views.blog'))

    return render_template("signup.html", user=current_user)


@auth.route("Logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category='success')
    return redirect(url_for("views.home"))

@auth.route("Logout Account")
@login_required
def logoutaccount():
    logout_user()
    flash("Logged out successfully!", category='success')
    return redirect(url_for("views.home"))

    