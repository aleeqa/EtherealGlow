from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from package.models import User
from package import db
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import bcrypt

app = Flask(__name__, static_url_path='/static')



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/Login")
def login():
    return render_template("login.html")

@app.route("/Logout")
def logout():
    return redirect(url_for("login"))

@app.route('/Signup')
def signup():
    return render_template('signup.html')
  
@app.route("/Admin")
def admin():
    return "This is admin page"

@app.route("/AboutUs")
def about():
    return "This is about_us page."

@app.route("/Blog")
def blog():
   return render_template("blog.html")

if __name__ == "__main__":
    app.run(debug=True)