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
    skintype = db.Column(db.String(20), nullable=False)
    products = db.relationship('Product', backref='author', passive_deletes=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    skintype = db.Column(db.String(20), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    product_name = db.Column(db.Text, nullable=False)
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
    ingredients = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150))  
    
class Products(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    product_type = db.Column(db.String(150))
    ingredients = db.Column(db.String(2000))
    skintype = db.Column(db.Integer, db.ForeignKey('user.skintype', ondelete="CASCADE"), nullable=False)