from flask import make_response,jsonify
from model.model import *
from flask_sqlalchemy import sqlalchemy
from .error_handler_service import InvalidUsageError
from sqlalchemy import desc
from sqlalchemy.exc import *
from sqlalchemy.orm.exc import *
from werkzeug.security import generate_password_hash, check_password_hash
import os,jwt,random,json,time
from dotenv import load_dotenv
from .response import *
from flask_redis import FlaskRedis

redis = FlaskRedis()

load_dotenv('bookenv/.env')
secret_key = os.getenv('secret_key')
books_data = []

class DataBase:
    @staticmethod
    def change_products_quantity_in_db():
        try:
            books_data = json.loads(redis.get('books_data'))
            list_of_books = books_data[:-1]
            for each_book in list_of_books:
                quantity = each_book['quantity']
                book_id = each_book['book_id']
                book_data = ProductData.query.filter_by(pid = book_id).first()
                book_data.quantity = book_data.quantity - quantity
                db.session.commit()
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def add_order(username):
        try:
            books_data = json.loads(redis.get('books_data'))
            list_of_books = books_data[-1]
            total_price = list_of_books['total-Price']
            user = User.query.filter_by(username = username).first()
            order_id = random.randint(1000,100000)
            address = UserAddress.query.filter_by(user_id = user.id).first()
            order = OrderData(user_id= user.id,address_id = address.address_id,orderid = order_id,total_price = total_price)
            db.session.add(order)
            db.session.commit()
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)
    
    @staticmethod
    def get_user_details(username):
        try:
            books_data = json.loads(redis.get('books_data'))
            user = User.query.filter_by(username = username).first()
            address = UserAddress.query.filter_by(user_id = user.id).first()
            order = OrderData.query.filter_by(user_id = user.id).first()
            list_of_books = books_data[:-1]
            books =  DataBase.add_keys(list_of_books)
            price = DataBase.calculate_price(books)
            books.append({"total-Price" : price})
            user_mail = user.email
            order_id = order.orderid
            address = address.address
            list_of_details = [user_mail,order_id,address]
            return list_of_details,books
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def add_keys(books_data):
        book_list = []
        for each_book in books_data:
            book_list.append(
                {
                "author" : each_book["author"],
                "title" : each_book["title"],
                "price" : each_book["price"],
                "quantity" : each_book["quantity"],
                "image" : each_book["image"]
                }
            )
        return book_list

    @staticmethod
    def add_to_address_db(username,name,mobile_number,address,pincode):
        try:
            user = User.query.filter_by(username = username).first()
            address = UserAddress(user_id= user.id,name = name,mobilenumber = mobile_number,address = address,pincode = pincode)
            db.session.add(address)
            db.session.commit()
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)
        except sqlalchemy.exc.IntegrityError:
            raise InvalidUsageError(order_post[400],400)

    @staticmethod
    def display_wishlist(user_name):
        list_of_books = []
        try:
            if redis.exists("items"):
                return json.loads(redis.get('items'))
            user = User.query.filter_by(username = user_name).first()
            for each_book in user.wishlist:
                list_of_books.append(each_book)
            books_with_keys = DataBase.to_add_keys(list_of_books)
            json_books = json.dumps(books_with_keys)
            redis.set(name = 'items',value = json_books)
            redis.expire('items' ,(2*60*60))
            return books_with_keys
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def add_to_wishlist(user_name,book_id):
        try:
            user = User.query.filter_by(username = user_name).first()
            book_data = ProductData.query.filter_by(pid = book_id).first()
            user.wishlist.append(book_data)
            db.session.commit()
            redis.delete('items')
            return wishlist[200]
        except FlushError :
            raise InvalidUsageError(wishlist[400], 400)
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def check_token(token):
        try:
            data = jwt.decode(token,secret_key)
            email =data['email']
            user = User.query.filter_by(email = email).first()
            if user:
                user.confirmed = True
            db.session.commit()
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)
    
    @staticmethod
    def calculate_price(books):
        price = 0 
        for each_book in books:
            price += each_book['price']
        return price
    
    @staticmethod
    def get_list_of_books(user):
        list_of_books = []
        for each_book in user.cart:
            list_of_books.append(each_book)
        return list_of_books

    #  static methods for add,delete,update,display
    # for cart api
    @staticmethod
    def remove_from_cart(user_name,book_id):
        try:
            user = User.query.filter_by(username = user_name).first()
            book_data = ProductData.query.filter_by(pid = book_id).first()
            user.cart.remove(book_data)
            db.session.commit()
            return cart_del[200]
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)  

    @staticmethod
    def update_cart(user_name,product_id,quantity):
        is_product_present = False
        try:
            book_data = ProductData.query.filter_by(pid = product_id).first()
            if book_data.quantity < quantity:
                return cart_quantity[400],400
            books_data = json.loads(redis.get('books_data'))
            list_of_books = books_data[:-1]
            for each_book in list_of_books:
                if each_book['book_id'] == product_id:
                    is_product_present = True
                    each_book["quantity"] = quantity
                    price = each_book["price"]
                    each_book["price"] = price * quantity
            price = DataBase.calculate_price(list_of_books)
            list_of_books.append({"total-Price" : price})
            json_books = json.dumps(list_of_books)
            redis.set(name = 'books_data',value = json_books)
            redis.expire('books_data' ,(24*60*60))
            if is_product_present:
                return list_of_books,200
            return cart[400],400
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def display_cart(user_name):
        try:
            if redis.exists("books_data"):
                return json.loads(redis.get('books_data'))
            user = User.query.filter_by(username = user_name).first()
            list_of_books = DataBase.get_list_of_books(user)
            books =  DataBase.to_add_keys(list_of_books)
            for each_book in books:
                each_book["quantity"] = 1
            price = DataBase.calculate_price(books)
            books.append({"total-Price" : price})
            json_books = json.dumps(books)
            redis.set(name = 'books_data',value = json_books)
            redis.expire('books_data' ,(24*60*60))
            return books
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def add_to_cart(user_name,book_id):
        try:
            user = User.query.filter_by(username = user_name).first()
            book_data = ProductData.query.filter_by(pid = book_id).first()
            if book_data.quantity > 0:
                user.cart.append(book_data)
                db.session.commit()
                redis.delete('books_data')
                return cart[200]
            return cart[400]
        except FlushError:
            raise InvalidUsageError(wishlist[400], 400)
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)


    # static method for the sorting
    # for sort api
    @staticmethod
    def sort_books_by_price(value):
        try:
            books_data = ProductData.query.order_by(desc("price")).all()
            if value:
                books_data = ProductData.query.order_by("price").all()
            return DataBase.to_add_keys(books_data)
        except (InvalidRequestError,OperationalError,CompileError) :
            raise InvalidUsageError(sql[500], 500)


    # static methods  for search,and get books
    # for get book api  
    @staticmethod
    def search_book(search_value):
        try:
            books_data = ProductData.query.filter_by(author = search_value).all()
            if len(books_data) == 0:
                books_data = ProductData.query.filter_by(title = search_value).all()
            return DataBase.to_add_keys(books_data)
        except (InvalidRequestError,OperationalError) :
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def to_add_keys(books_data):
        book_list = []
        for each_book in books_data:
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
    def get_books_data_from_db():
        try:
            if redis.exists("books"):
                return json.loads(redis.get('books'))
            books_data = ProductData.query.all()
            books_with_keys =  DataBase.to_add_keys(books_data)
            json_books = json.dumps(books_with_keys)
            redis.set(name = 'books',value = json_books)
            redis.expire('books' ,(2*60*60))
            return books_with_keys
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)


    # static method to add user in db
    # for registration api
    @staticmethod
    def add_user_to_db(user_name,email,password,mail_msg):
        try:
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username= user_name, email=email, password=hashed_password,confirmed = False)
            db.session.add(new_user)
            db.session.commit()
            return make_response(jsonify({'response': mail_msg}),200)
        except sqlalchemy.exc.IntegrityError:
            return make_response(login[401],401)
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)


    # static method to check user 
    # for login api
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
            raise InvalidUsageError(sql[500], 500)
            

            