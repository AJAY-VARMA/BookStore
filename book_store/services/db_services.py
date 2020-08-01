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
from .mail_service import MailService
from .response import *
from .static_data import order_max,order_min,redis_time
from flask_redis import FlaskRedis
from redis.exceptions import ConnectionError
from .serializer import ProductSchema,ProductOrderSchema

redis = FlaskRedis()

load_dotenv('bookenv/.env')
secret_key = os.getenv('secret_key')

class DataBase:
    @staticmethod
    def change_products_quantity_in_db(username):
        try:
            books_data = json.loads(redis.get('books_data'))
            user = User.query.filter_by(username = username).first()
            order = OrderData.query.filter_by(user_id = user.id).first()
            list_of_books = books_data[:-1]
            for each_book in list_of_books:
                quantity = each_book['quantity']
                book_id = each_book['pid']
                book_data = ProductData.query.filter_by(pid = book_id).first()
                book_data.quantity = book_data.quantity - quantity
                db.session.commit()
                order_with_products  = OrderWithProducts(order_id = order.orderid,product_id = book_id,quantity = quantity)
                db.session.add(order_with_products)
                db.session.commit()
                redis.delete('books')
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)
        except (ConnectionError,TypeError):
            raise InvalidUsageError(redis_error[500],500)

    @staticmethod
    def get_order_id():
        order_id = random.randint(order_min,order_max)
        present = bool(OrderData.query.filter_by(orderid = order_id).first())
        if present:
            DataBase.get_order_id()
        return order_id

    @staticmethod
    def add_order(username):
        try:
            books_data = json.loads(redis.get('books_data'))
            list_of_books = books_data[-1]
            total_price = list_of_books['total-Price']
            user = User.query.filter_by(username = username).first()
            address = UserAddress.query.filter_by(user_id = user.id).first()
            order_id = DataBase.get_order_id()
            order = OrderData(user_id= user.id,address_id = address.address_id,orderid = order_id,total_price = total_price)
            db.session.add(order)
            db.session.commit()
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)
        except (ConnectionError,TypeError):
            raise InvalidUsageError(redis_error[500],500)
    
    @staticmethod
    def get_user_details(username):
        try:
            books_data = json.loads(redis.get('books_data'))
            user = User.query.filter_by(username = username).first()
            address_data = UserAddress.query.filter_by(user_id = user.id).first()
            order = OrderData.query.filter_by(user_id = user.id).first()
            list_of_books = books_data[:-1]
            products_schema =  ProductOrderSchema(many = True)
            books = products_schema.dump(list_of_books)
            price = DataBase.calculate_price(books)
            books.append({"total-Price" : price})
            user_mail = user.email
            order_id = order.orderid
            address = address_data.address
            list_of_details = [user_mail,order_id,address]
            details_to_send_msg = [order_id,address_data.mobilenumber,price]
            return list_of_details,books,details_to_send_msg
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)

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
        try:
            if redis.exists("items"):
                return json.loads(redis.get('items'))
            user = User.query.filter_by(username = user_name).first()
            list_of_books = [each_book for each_book in user.wishlist]
            products_schema =  ProductSchema(many = True)
            books = products_schema.dump(list_of_books)
            json_books = json.dumps(books)
            redis.set(name = 'items',value = json_books)
            redis.expire('items' ,redis_time)
            return books_with_keys
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)
        except (ConnectionError,TypeError):
            raise InvalidUsageError(redis_error[500],500)

    @staticmethod
    def add_to_wishlist(user_name,book_id):
        try:
            user = User.query.filter_by(username = user_name).first()
            book_data = ProductData.query.filter_by(pid = book_id).first()
            user.wishlist.append(book_data)
            db.session.commit()
            redis.delete('items')
            return cart_response["added"]
        except FlushError :
            raise InvalidUsageError(cart_response[400], 400)
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
        [price := price + each_book['price'] for each_book in books]
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
            redis.delete('books_data')
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)  
        except (ConnectionError):
            raise InvalidUsageError(redis_error[500],500)

    @staticmethod
    def update_cart(user_name,product_id,quantity):
        is_product_present = False
        try:
            quantity = int(quantity)
            product_id = int(product_id)
            book_data = ProductData.query.filter_by(pid = product_id).first()
            if book_data.quantity < quantity:
                return response['quantity'],400
            books_data = json.loads(redis.get('books_data'))
            list_of_books = books_data[:-1]
            for each_book in list_of_books:
                if each_book['pid'] == product_id:
                    is_product_present = True
                    each_book["quantity"] = quantity
                    price = book_data.price
                    each_book["price"] = price * quantity
            price = DataBase.calculate_price(list_of_books)
            list_of_books.append({"total-Price" : price})
            json_books = json.dumps(list_of_books)
            redis.set(name = 'books_data',value = json_books)
            redis.expire('books_data' ,redis_time)
            if is_product_present:
                return list_of_books,200
            return response[400],400
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)
        except (ConnectionError,TypeError):
            raise InvalidUsageError(redis_error[500],500)
        except ValueError:
            raise InvalidUsageError(update_error[400],400)

    @staticmethod
    def display_cart(user_name):
        try:
            if redis.exists('books_data'):
                return json.loads(redis.get('books_data'))
            user = User.query.filter_by(username = user_name).first()
            list_of_books = [each_book for each_book in user.cart]
            products_schema =  ProductSchema(many = True)
            books = products_schema.dump(list_of_books) 
            for each_book in books:
                each_book["quantity"] = 1
            price = DataBase.calculate_price(books)
            books.append({"total-Price" : price})
            json_books = json.dumps(books)
            redis.set(name = 'books_data',value = json_books)
            redis.expire('books_data' ,redis_time)
            return books
        except (InvalidRequestError,OperationalError,CompileError):
            raise InvalidUsageError(sql[500], 500)
        except (ConnectionError,TypeError):
            raise InvalidUsageError(redis_error[500],500)

    @staticmethod
    def add_to_cart(user_name,book_id):
        try:
            user = User.query.filter_by(username = user_name).first()
            book_data = ProductData.query.filter_by(pid = book_id).first()
            if book_data.quantity > 0:
                user.cart.append(book_data)
                db.session.commit()
                redis.delete('books_data')
                return make_response(response["added"],200)
            return make_response(response[200],200)
        except FlushError:
             return make_response(response[400],400)
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
            books_data = ProductData.query.filter((ProductData.author == search_value) | (ProductData.title == search_value)).all()
            products_schema =  ProductSchema(many = True)
            all_books = products_schema.dump(books_data) 
            return all_books
        except (InvalidRequestError,OperationalError) :
            raise InvalidUsageError(sql[500], 500)

    @staticmethod
    def get_books_data_from_db():
        try:
            if redis.exists("books"):
                return json.loads(redis.get('books'))
            books_data = ProductData.query.all()
            products_schema =  ProductSchema(many = True)
            all_books = products_schema.dump(books_data)
            json_books = json.dumps(all_books) 
            redis.set(name = 'books',value = json_books)
            redis.expire('books' ,redis_time)
            return all_books
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)
        except (ConnectionError,TypeError):
            raise InvalidUsageError(redis_error[500],500)

    # static method to add user in db
    # for registration api
    @staticmethod
    def add_user_to_db(user_name,email,password):
        try:
            MailService.send_mail_with_link(user_name,email)
            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username= user_name, email=email, password=hashed_password,confirmed = False)
            db.session.add(new_user)
            db.session.commit()
            return make_response(registration_response[200],200)
        except sqlalchemy.exc.IntegrityError:
            return make_response(registration_response[409],409)
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)

    # static method to check user 
    # for login api
    @staticmethod
    def check_user_in_db(user_name,password):
        try:
            user = User.query.filter_by(username=user_name).first()
            if user:
                if check_password_hash(user.password, password):
                    if user.confirmed:
                        return True,True
                    return True,False
            return False,False
        except (InvalidRequestError,OperationalError):
            raise InvalidUsageError(sql[500], 500)
            