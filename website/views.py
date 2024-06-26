from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Feedback, Comment, Product, User_Profile
from . import db
from analyze import analyzer_tool
from werkzeug.utils import secure_filename
import os
import logging
from flask import Flask 

views = Blueprint("views", __name__)

#HOME
@views.route("/")
@views.route("/home")
def home():
    return render_template("directory.html")

@views.route("/analyzer")
def analyzer():
    return render_template("analyzer.html")

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
            #add into database
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
    post = Post.query.get(id)  

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:  #check if the current user is the author of the post
        flash("You do not have permission to delete this post.", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')
        return redirect(url_for("views.blog"))  #returning page after successfully deleting the post

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
        product_category = request.form.get('product_category')
        text = request.form.get('text')
        image = request.files.get('image')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            feedback = Feedback(product_input=product_input, product_category=product_category, text=text, image=filename, user=current_user.id)

        elif image and not allowed_file(image.filename):
            flash('Invalid file type. Allowed types are: pdf, png, jpg, jpeg', category='error')     
            return redirect(request.url)
        
        else:
            feedback = Feedback(product_input=product_input, product_category=product_category, text=text, user=current_user.id)

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

@views.route("/productFeedbacks/<product_category>")
@login_required
def productFeedbacks(product_category):
    product = Feedback.query.filter_by(product_category=product_category).first()

    if not product :
        flash ("Feedback does not exists.", category="error")
        return redirect(url_for('views.display_feedbacks'))
    
    feedbacks = Feedback.query.filter_by(product_category=product_category).all()
    return render_template("product_type_feedbacks.html",  user=current_user, feedbacks=feedbacks, product_category=product_category)


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
    
    #if user upload image
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        product = Product(product_name=product_name, product_brand=product_brand, product_category=product_category, product_ingredients=product_ingredients, image=filename, skintype=skintype, user=user_id)

    elif image and not allowed_file(image.filename):
        flash('Invalid file type. Allowed types are: pdf, png, jpg, jpeg', category='error')     
        return redirect(request.url)
    
    #if user does not upload image
    else:
        product = Product(product_name=product_name, product_brand=product_brand, product_category=product_category, product_ingredients=product_ingredients, user=user_id, skintype=skintype)
    
    db.session.add(product)
    db.session.commit()
    flash('A new product was successfully saved into the database!', category='success')
    return redirect(url_for('views.analyzer'))   

#ABOUT US
@views.route("/aboutUs")
def about():
    return render_template("AboutUs.html")
 
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
        product_category = request.form['product_category'].capitalize()

        print(f"Received skintype: {skintype}, product_category: {product_category}")

        try:
            recommended_products = Product.query.filter_by(skintype=skintype, product_category=product_category).all()
            
            #print the query results to debug
            print(f"Recommended Products: {recommended_products}")
            
            #additional debug: Print all products to ensure data is present
            #all_products = Product.query.all()

            ##print(f"All Products: {all_products}")
        except Exception as e:
            print(f"Error retrieving products: {e}")
            recommended_products = []
    else:
        recommended_products = []
    
    
    all_products = Product.query.all()
    print(f"All Products: {all_products}")
    return render_template('recommendation.html', suggestions=recommended_products)



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
            # Update the existing user profile
            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.phone = phone
            existing_user.bio = bio
            db.session.commit()
            flash('User profile updated successfully!', 'success')
        else:
            # Create a new user profile
            user = User_Profile(first_name=first_name, last_name=last_name, email=email, phone=phone, bio=bio)
            db.session.add(user)
            db.session.commit()
            flash('User profile created successfully!', 'success')

        return redirect(url_for('views.user_profile'))

    user = User.query.first()  # Get the first user for simplicity
    return render_template('profile.html', user=user)

#search bar (blog) 
@views.route('/search_posts', methods=['GET'])
def search_posts():
    query = request.args.get('q', '')
    results = Post.query.filter(Post.text.ilike(f'%{query}%')).all()
    search_results = []

    for result in results:
        post_info = {
            'id': result.id,
            'header': result.text[:30],  
            'body': result.text
        }
        search_results.append(post_info)

    return jsonify(search_results)

@views.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view-post.html', post=post)
