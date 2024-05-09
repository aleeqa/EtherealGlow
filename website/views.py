from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Post, User, Feedback
from . import db
from analyze import analyzer_tool
from .forms import InputForm
from werkzeug.utils import secure_filename
import os

views = Blueprint("views", __name__)

@views.route("/Blog")
@login_required 
def blog():    
    posts = Post.query.all()
    return render_template("blog.html", user=current_user, posts = posts)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")

@views.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if text:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))
        else:
            flash('Post cannot be empty', category='error')
          
    return render_template('create_post.html', user=current_user)

@views.route("/delete-post/<int:id>")
@login_required
def delete_post(id):
    post = Post.query.get(id)  # Use get() instead of filter_by(id=id).first() for simplicity

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:  # Check if the current user is the author of the post
        flash("You do not have permission to delete this post.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
        return redirect(url_for("views.blog"))  # Return after successfully deleting the post

    return redirect(url_for("views.blog"))  # Redirect even if there's an error

@views.route("/posts/<username>")
@login_required
def posts(username) :
    user = User.query.filter_by(username=username).first()

    if not user :
        flash ("User is not exist.", category="error")
        return redirect(url_for('views.blog'))
    
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/analyze", methods=['POST'])
def analyze():
    # to get the ingredients entered 
    ingredients = request.form.get('ingredients')

    # analyzing ingredients
    result = analyzer_tool(ingredients)
    return render_template('home.html', result=result) #render result in {{ result }} in home.html

@views.route("/feedback", methods=['GET', 'POST'])
@login_required
def feedback():
    form = InputForm()
    if form.validate_on_submit():
        product_name = form.product_name.data
        text = form.text.data
        image = form.image.data

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))  # Save image to a designated folder
            feedback = Feedback(product_name= product_name, text=text, image=filename, user_id=current_user.id)
        else:
            feedback = Feedback(product_name= product_name, text=text, user_id=current_user.id)

        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!', category='success')
        return redirect(url_for('views.display_feedbacks'))

    return render_template('feedback.html', user=current_user, form=form)

@views.route("/display_feedbacks")
def display_feedbacks():
    feedbacks = Feedback.query.all()
    return render_template('display_feedbacks.html', user=current_user, feedbacks=feedbacks)