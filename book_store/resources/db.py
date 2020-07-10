from flask import render_template,make_response,url_for,redirect,jsonify
from app  import app
# from book_store.app  import app
import jwt,jinja2
from flask_mysqldb import MySQL
from .error_handler import InvalidUsageError
from flask_sqlalchemy import SQLAlchemy,sqlalchemy
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError,OperationalError,InvalidRequestError,CompileError
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

class ProData(db.Model):
    Pid = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    title = db.Column(db.String(300))
    image = db.Column(db.String(300))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    description = db.Column(db.String(6000))

class DataBase:
    @staticmethod
    def sort_books_by_price(value):
        try:
            book_details = ProData.query.order_by(desc("price")).all()
            if value:
                book_details = ProData.query.order_by("price").all()
            return DataBase.to_add_keys(book_details)
        except (InvalidRequestError,OperationalError,CompileError) :
            raise InvalidUsageError('mysql connection or syntax is improper', 500)
        
    @staticmethod
    def search_book(book_id):
        try:
            book_details = ProData.query.filter_by(author = book_id).all()
            if len(book_details) == 0:
                book_details = ProData.query.filter_by(title = book_id).all()
            return DataBase.to_add_keys(book_details)
        except (InvalidRequestError,OperationalError) :
            raise InvalidUsageError('mysql connection or syntax is improper', 500)

    @staticmethod
    def to_add_keys(book_details):
        book_list = []
        for each_book in book_details:
            book_list.append(
                {
                "book_id":each_book.Pid,
                "author" : each_book.author,
                "title" : each_book.title,
                "image" : each_book.image,
                "quantity" : each_book.quantity,
                "price" : each_book.price,
                "description":each_book.description
                }
            )
        return book_list

    @staticmethod
    def get_data_from_db():
        try:
            book_details = ProData.query.all()
            return DataBase.to_add_keys(book_details)
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError('mysql connection or syntax is improper', 500)

    @staticmethod
    def add_to_db(user_name,email,password,mail_msg):
        try:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username= user_name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'response': mail_msg}),200)
        except sqlalchemy.exc.IntegrityError:
            return make_response(jsonify({'response': "user name or email already exists"}),400)
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError('mysql connection or syntax is improper', 500)


    @staticmethod
    def check_user_in_db(user_name,password):
        try:
            user = User.query.filter_by(username=user_name).first()
            if user:
                if check_password_hash(user.password, password):
                   return True
            return False
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError('mysql connection or syntax is improper', 500)
            

            