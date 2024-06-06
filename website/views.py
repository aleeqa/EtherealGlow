from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Feedback, Comment, Product, User_Profile
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
    post = Post.query.get(id)  #use get() instead of filter_by(id=id).first() for simplicity

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:  #check if the current user is the author of the post
        flash("You do not have permission to delete this post.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
        return redirect(url_for("views.blog"))  #return after successfully deleting the post

    return redirect(url_for("views.blog")) 

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
    ingredients = request.form.get('ingredients')
    result = analyzer_tool(ingredients)
    return jsonify({"result": result})

#FEEDBACK AND UPLOAD PICTURE
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename  and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route("/feedback", methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == "POST":
        product_input = request.form.get('product_input')
        text = request.form.get('text')
        image = request.files.get('image')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            feedback = Feedback(product_input=product_input, text=text, image=filename, user=current_user.id)

        elif image and not allowed_file(image.filename):
            flash('Invalid file type. Allowed types are: pdf, png, jpg, jpeg', category='error')     
            return redirect(request.url)
        
        else:
            feedback = Feedback(product_input=product_input, text=text, user=current_user.id)

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

#SEARCH PRODUCT
@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = Product.query.filter(Product.product_name.ilike(f'%{query}%')).all()
        search_results = []

        for result in results:
            product_info = {
                'product_brand': result.product_brand,
                'product_name': result.product_name,
                'product_category': result.product_category,
                'product_ingredients': result.product_ingredients,
                'image': result.image
            }
            # Analyze ingredients for comedogenicity
            comedogenic_result = analyzer_tool(result.product_ingredients)
            product_info['comedogenic'] = comedogenic_result
            search_results.append(product_info)

        return jsonify(search_results)
        
@views.route('/autocomplete', methods=['POST'])
def autocomplete():
    query = request.form['query']
    results = Product.query.filter(Product.product_name.ilike(f'%{query}%')).limit(10).all()
    return jsonify([{'name': result.product_name} for result in results])

@views.route('/searchfeedback', methods=['GET', 'POST'])
def searchFeedback():
    if request.method == 'POST':
        query = request.form['query']
        results = Product.query.filter(Product.product_name.ilike(f'%{query}%')).all()
        search_results = []

        for result in results:
            product_info = {
                'product_name': result.product_name,
            }
            search_results.append(product_info)

        return jsonify(search_results)
    
#ADD NEW PRODUCT
@views.route('/add_product', methods=['GET','POST'])
def add_product():
    product_name = request.form['product_name']
    product_brand = request.form['product_brand']
    product_category = request.form['product_category']
    product_ingredients = request.form['product_ingredients']
    image = request.files['image']
    skintype = request.form['skintype']

    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        product = Product(product_name=product_name, product_brand=product_brand, product_category=product_category, product_ingredients=product_ingredients, image=filename, user=user_id)

    elif image and not allowed_file(image.filename):
        flash('Invalid file type. Allowed types are: pdf, png, jpg, jpeg', category='error')     
        return redirect(request.url)
    
    else:
        product = Product(product_name=product_name, product_brand=product_brand, product_category=product_category, product_ingredients=product_ingredients, user=user_id, skintype=skintype)
    
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
@views.route('/recommendations', methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        skintype = request.form['skintype']
        product_category = request.form['product_category']

        #retrieve recommended products from the database based on skintype and product_category
        recommended_products = Product.query.filter(skintype==skintype, product_category==product_category).all()
    else:
        recommended_products = []

    return render_template('recommendation.html', suggestions=recommended_products)


'''@views.route('/recommendations', methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        skintype = request.form['skintype']
        product_category = request.form['product_category']

        #retrieve recommended products from the database based on skin type and product category
        recommended_products = Product.query.filter_by(skintype=skintype, product_category=product_category).all()
    else:
        recommended_products = []

    return render_template('recommendation.html', suggestions=recommended_products)'''

#ai chatbox and my acccount 

@views.route('/ai_chatbox')
def ai():
    return render_template("Ai.html")

    #jasdev 
@views.route('/profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'POST':    
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        bio = request.form['bio']

        # Check if a user with this email already exists
        existing_user = User_Profile.query.filter_by(email=email).first()
        if existing_user:
            flash('A user with this email already exists.', 'error')
        else:
            user = User_Profile(first_name=first_name, last_name=last_name, email=email, phone=phone, bio=bio)
            db.session.add(user)
            db.session.commit()
            flash('User profile updated successfully!', 'success')
            return redirect(url_for('views.user_profile'))

    user = User.query.first()  # Get the first user for simplicity
    return render_template('profile.html', user=user)