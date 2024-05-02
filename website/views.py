from flask import Blueprint, render_template,request
from flask_login import login_required, current_user
from analyze import analyzer_tool

views = Blueprint("views", __name__)



@views.route("/Blog")
@login_required
def blog():    
    return render_template("blog.html", user=current_user)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")

@views.route("/analyze", methods=['POST'])
def analyze():
    # to get the ingredients entered 
    ingredients = request.form.get('ingredients')

    # analyzing ingredients
    result = analyzer_tool(ingredients)
    return render_template('home.html', result=result) #render result in {{ result }} in home.html