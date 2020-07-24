from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    address = db.relationship('UserAddress',backref = 'user')
    order = db.relationship('OrderData',backref = 'user')

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
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    address_id = db.Column(db.Integer,db.ForeignKey('user_address.address_id'))
    orderid = db.Column(db.String(25), primary_key=True)
    total_price = db.Column(db.Integer)

class UserAddress(db.Model):
    address_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    name = db.Column(db.String(50))
    mobilenumber = db.Column(db.BigInteger)
    address = db.Column(db.String(500))
    pincode = db.Column(db.Integer)
    order = db.relationship('OrderData',backref = 'address',uselist = False)