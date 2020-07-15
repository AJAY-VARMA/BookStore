from flask import render_template,make_response,url_for,redirect,jsonify
# from app  import app
from model.model import *
import jwt
from flask_mysqldb import MySQL
from flask_sqlalchemy import sqlalchemy
from .error_handler_service import InvalidUsageError
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError,OperationalError,InvalidRequestError,CompileError
from werkzeug.security import generate_password_hash, check_password_hash
import os,jwt
from dotenv import load_dotenv

load_dotenv('bookenv/.env')
secret_key = os.getenv('secret_key')

class DataBase:
        
    @staticmethod
    def display_wishlist(user_name):
        list_of_books = []
        try:
            user = User.query.filter_by(username = user_name).first()
            for each_book in user.wishlist:
                list_of_books.append(each_book)
            return DataBase.to_add_keys(list_of_books)
        except:
            pass

    @staticmethod
    def add_to_wishlist(user_name,book_id):
        # try:
            user = User.query.filter_by(username = user_name).first()
            book_details = ProductData.query.filter_by(pid = book_id).first()
            user.wishlist.append(book_details)
            db.session.commit()
        # except :
        #     pass

    @staticmethod
    def check_token(token):
        try:
            data = jwt.decode(token,secret_key)
            email =data['email']
            user = User.query.filter_by(email = email).first()
            if user:
                user.confirmed = True
            db.session.commit()
        except :
            pass
    
    @staticmethod
    def calculate_price(books):
        price = 0 
        for each_book in books:
            price += each_book['price']
        return price

    @staticmethod
    def display_cart(user_name):
        list_of_books = []
        try:
            user = User.query.filter_by(username = user_name).first()
            for each_book in user.cart:
                list_of_books.append(each_book)
            books =  DataBase.to_add_keys(list_of_books)
            price = DataBase.calculate_price(books)
            return books,price
        except:
            pass

    @staticmethod
    def add_to_cart(user_name,book_id):
        try:
            user = User.query.filter_by(username = user_name).first()
            book_details = ProductData.query.filter_by(pid = book_id).first()
            user.cart.append(book_details)
            db.session.commit()
        except :
            pass

    @staticmethod
    def sort_books_by_price(value):
        try:
            book_details = ProductData.query.order_by(desc("price")).all()
            if value:
                book_details = ProductData.query.order_by("price").all()
            return DataBase.to_add_keys(book_details)
        except (InvalidRequestError,OperationalError,CompileError) :
            raise InvalidUsageError('mysql connection or syntax is improper', 500)
        
    @staticmethod
    def search_book(sort_value):
        try:
            book_details = ProductData.query.filter_by(author = sort_value).all()
            if len(book_details) == 0:
                book_details = ProductData.query.filter_by(title = sort_value).all()
            return DataBase.to_add_keys(book_details)
        except (InvalidRequestError,OperationalError) :
            raise InvalidUsageError('mysql connection or syntax is improper', 500)

    @staticmethod
    def to_add_keys(book_details):
        book_list = []
        for each_book in book_details:
            book_list.append(
                {
                "book_id":each_book.pid,
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
            book_details = ProductData.query.all()
            return DataBase.to_add_keys(book_details)
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError('mysql connection or syntax is improper', 500)

    @staticmethod
    def add_to_db(user_name,email,password,mail_msg):
        try:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username= user_name, email=email, password=hashed_password,confirmed = False)
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
                if user.confirmed:
                    if check_password_hash(user.password, password):  
                        return True
            return False
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError('mysql connection or syntax is improper', 500)
            

            