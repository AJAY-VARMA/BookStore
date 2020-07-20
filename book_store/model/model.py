# from book_store.app  import app
from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

wishlist_relation = db.Table('wishlist_relation',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
        db.Column('product_id',db.Integer,db.ForeignKey('product_data.pid'))
        )
        
cart_relation = db.Table('cart_relation',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
        db.Column('product_id',db.Integer,db.ForeignKey('product_data.pid'))
        )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    confirmed = db.Column(db.Boolean, nullable=False)
    address = db.relationship('OrderData',backref = 'user',uselist = False)

class ProductData(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    title = db.Column(db.String(300))
    image = db.Column(db.String(300))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    description = db.Column(db.String(6000))
    cart_item = db.relationship('User',secondary = cart_relation,backref = db.backref('cart',lazy = 'dynamic'))
    wishlist_item = db.relationship('User',secondary = wishlist_relation,backref = db.backref('wishlist',lazy = 'dynamic'))

class OrderData(db.Model):
    username = db.Column(db.String(25),db.ForeignKey('user.username'),primary_key = True)
    mobilenumber = db.Column(db.BigInteger)
    orderid = db.Column(db.String(25), unique=True)
    address = db.Column(db.String(500))
