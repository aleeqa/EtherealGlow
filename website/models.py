from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    feedbacks = db.relationship('Feedback', backref='author', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    skintype = db.Column(db.Text, nullable=False)
    products = db.relationship('Product', backref='author', passive_deletes=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    skintype = db.Column(db.Text, nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    product_input = db.Column(db.Integer, db.ForeignKey('product.product_name', ondelete="CASCADE"), nullable=False)
    product_category = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150))  
    date_created = db.Column(db.DateTime(timezone=True), default=func.now()) 

class Comment(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

class Product(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    product_brand = db.Column(db.Text, nullable=False)
    product_name = db.Column(db.Text, nullable=False)
    product_category = db.Column(db.Text, nullable=False)
    product_ingredients = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150))
    skintype = db.Column(db.Text, nullable=False)  
    product_feedback = db.relationship('Feedback', backref='product', passive_deletes=True)

class User_Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    bio = db.Column(db.Text, nullable=True)

