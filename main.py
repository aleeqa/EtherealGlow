from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__, static_url_path='/static')



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/Login")
def login():
    return "This is login page."

@app.route("/Logout")
def logout():
    return "This is logout page."

@app.route("/Signup")
def signup():
    return "This is sign up page."

@app.route("/Admin")
def admin():
    return "This is admin page."

@app.route("/AboutUs")
def about():
    return "This is about_us page."

@app.route("/Blog")
def blog():
    return "This is blog page."

if __name__ == "__main__":
    app.run(debug=True)