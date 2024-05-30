from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Feedback, Comment, Product
from . import db
from analyze import analyzer_tool
from werkzeug.utils import secure_filename
import os

views = Blueprint("views", __name__)

#HOME
@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")

#BLOG
@views.route("/Blog")
@login_required 
def blog():    
    posts = Post.query.all()
    return render_template("blog.html", user=current_user, posts = posts)

#CREATE POST
@views.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')
        skintype = request.form.get('skintype')

        if text and skintype:
            post = Post(text=text, skintype=skintype, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.blog'))
        else:
            flash('Post cannot be empty', category='error')
          
    return render_template('create_post.html', user=current_user)

#DELETE POST
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

#POST USERNAME
@views.route("/posts/<username>")
@login_required
def posts(username) :
    user = User.query.filter_by(username=username).first()

    if not user :
        flash ("User is not exist.", category="error")
        return redirect(url_for('views.blog'))
    
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

#ANALYZER TOOL
@views.route("/analyze", methods=['POST'])
def analyze():
    # to get the ingredients entered 
    ingredients = request.form.get('ingredients')

    # analyzing ingredients
    result = analyzer_tool(ingredients)
    return render_template('home.html', result=result) #render result in {{ result }} in home.html

#FEEDBACK AND UPLOAD PICTURE
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename  and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/feedback", methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == "POST":
        product_name = request.form.get('product_name')
        text = request.form.get('text')
        image = request.files.get('image')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            feedback = Feedback(product_name=product_name, text=text, image=filename, user=current_user.id)

        elif image and not allowed_file(image.filename):
            flash('Invalid file type. Allowed types are: pdf, png, jpg, jpeg', category='error')     
            return redirect(request.url)
        
        else:
            feedback = Feedback(product_name=product_name, text=text, user=current_user.id)

        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!', category='success')
        return redirect(url_for('views.display_feedbacks'))
    
    return render_template('feedback.html', user=current_user)

@views.route("/delete-feedback/<int:id>")
@login_required
def delete_feedback(id):
    feedback = Feedback.query.filter_by(id=id).first()

    if not feedback:
        flash("Feedback does not exist.", category='error')

    elif current_user.id != feedback.user :
        flash('You do not have permission to delete this feedback.', category='error')

    else:
        db.session.delete(feedback)
        db.session.commit()
        flash('Feedback deleted.', category='success')

    return redirect(url_for('views.display_feedbacks'))  
          
@views.route("/display_feedbacks")
def display_feedbacks():
    feedbacks = Feedback.query.all()
    return render_template('display_feedbacks.html', user=current_user, feedbacks=feedbacks)

@views.route("/feedbacks/<username>")
@login_required
def feedbacks(username):
    user = User.query.filter_by(username=username).first()

    if not user :
        flash ("User is not exist.", category="error")
        return redirect(url_for('views.display_feedbacks'))
    
    feedbacks = user.feedbacks
    return render_template("reviews.html", user=current_user, feedbacks=feedbacks, username=username)


#CREATE COMMENT
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id) :
    text = request.form.get('text')

    if not text :
        flash('Comment cannot be empty.')
    else : 
        post = Post.query.filter_by(id=post_id).first()
        if post :
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else : 
            flash('Post does not exists.', category='error')

        return redirect(url_for('views.blog'))

#DELETE COMMENT
@views.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id) :
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment :
        flash('Comment does not exists', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment', category='error')
    else :
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.blog'))

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = Product.query.filter(Product.product_name.ilike(f'%{query}%')).all()
        return jsonify([{'product_brand': result.product_brand, 'product_name': result.product_name, 'product_category': result.product_category, 'ingredients': result.ingredients} for result in results])
    

@views.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    product_brand = request.form['product_brand']
    product_category = request.form['product_category']
    ingredients = request.form['ingredients']
    #image = request.files['image']
    product = Product(product_name=product_name, product_brand=product_brand, product_category=product_category, ingredients=ingredients)
    db.session.add(product)
    db.session.commit()
    flash('A new product was successfully saved into the database!', category='success')
    return redirect(url_for('views.home'))   
 
#SKINTYPE
@views.route("/share/<skintype>")
@login_required
def share(skintype) :
    user= User.query.filter_by(skintype=skintype).first

    if not user :
        flash('No user with that skintype exists', category='error')
        return redirect(url_for(blog.html))

    posts = Post.query.filter_by(skintype=skintype).all()
    return render_template("skintype.html", user=current_user, posts=posts, skintype=skintype)

#RECOMMENDATION
@views.route('/recommendations', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'POST':
        skintype = request.form.get('skintype')
        product_category = request.form.get('product_category')
        
        # Get recommendations
        suggestion = get_recommendations(skintype, product_category)
        
        return jsonify(suggestion=suggestion)
    else:
        return render_template('recommendation.html')

def get_recommendations(skintype, product_category):
    recommendations = {
        'normal': {
            'cleanser': ['Normal Cleanser A', 'Normal Cleanser B'],
            'toner': ['Normal Toner A', 'Normal Toner B'],
            'serum': ['Normal Serum A', 'Normal Serum B'],
            'essence': ['Normal Essence A', 'Normal Essence B'],
            'moisturizer': ['Normal Moisturizer A', 'Normal Moisturizer B'],
            'sunscreen': ['Normal Sunscreen A', 'Normal Sunscreen B']
        },
        'oily': {
            'cleanser': ['Oily Cleanser A', 'Oily Cleanser B'],
            'toner': ['Oily Toner A', 'Oily Toner B'],
            'serum': ['Oily Serum A', 'Oily Serum B'],
            'essence': ['Oily Essence A', 'Oily Essence B'],
            'moisturizer': ['Oily Moisturizer A', 'Oily Moisturizer B'],
            'sunscreen': ['Oily Sunscreen A', 'Oily Sunscreen B']
        },
        'dry': {
            'cleanser': ['Dry Cleanser A', 'Dry Cleanser B'],
            'toner': ['Dry Toner A', 'Dry Toner B'],
            'serum': ['Dry Serum A', 'Dry Serum B'],
            'essence': ['Dry Essence A', 'Dry Essence B'],
            'moisturizer': ['Dry Moisturizer A', 'Dry Moisturizer B'],
            'sunscreen': ['Dry Sunscreen A', 'Dry Sunscreen B']
        },
        'combination': {
            'cleanser': ['Combination Cleanser A', 'Combination Cleanser B'],
            'toner': ['Combination Toner A', 'Combination Toner B'],
            'serum': ['Combination Serum A', 'Combination Serum B'],
            'essence': ['Combination Essence A', 'Combination Essence B'],
            'moisturizer': ['Combination Moisturizer A', 'Combination Moisturizer B'],
            'sunscreen': ['Combination Sunscreen A', 'Combination Sunscreen B']
        },
        'sensitive': {
            'cleanser': ['Sensitive Cleanser A', 'Sensitive Cleanser B'],
            'toner': ['Sensitive Toner A', 'Sensitive Toner B'],
            'serum': ['Sensitive Serum A', 'Sensitive Serum B'],
            'essence': ['Sensitive Essence A', 'Sensitive Essence B'],
            'moisturizer': ['Sensitive Moisturizer A', 'Sensitive Moisturizer B'],
            'sunscreen': ['Sensitive Sunscreen A', 'Sensitive Sunscreen B']
        }
    }
    
    return recommendations[skintype][product_category]

