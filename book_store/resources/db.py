from flask import render_template,make_response,url_for,redirect
import sys,os
sys.path.append('.')
from app  import app
# from book_store.app  import app
import jwt,jinja2
from flask_mysqldb import MySQL
from .error_handler import InvalidUsageError
from MySQLdb._exceptions import ProgrammingError,OperationalError

mysql = MySQL(app)

class DataBase:
    @staticmethod
    def get_book_data_by_id(book_id):
        # try:
            # book_id = '23'
            cur = mysql.connection.cursor()
            query_string = "SELECT * FROM products_data WHERE Pid = %s"
            cur.execute(query_string, (book_id))
            books_data = cur.fetchall()
            cur.close()
            return books_data
        # except (ProgrammingError,OperationalError) :
        #     raise InvalidUsageError('mysql connection or syntax is improper', 500)

    @staticmethod
    def get_data_from_db():
        try:
            cur = mysql.connection.cursor()
            result_value = cur.execute("select * from products_data")
            user_details = cur.fetchall()
            cur.close()
            return user_details
        except (ProgrammingError,OperationalError):
            raise InvalidUsageError('mysql connection or syntax is improper', 500)

    @staticmethod
    def add_to_db(user_name,email,password):
        try:
            # user_name = data['user_name']
            # email =  data['email']
            # password = data['password']
            pass_token = jwt.encode({'password':password},app.config['secret_key'])
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user_data(Username,email,password) VALUES(%s,%s,%s)"
                ,(user_name,email,pass_token))
            # mysql.connection.commit()
            cur.close()
        except jinja2.exceptions.TemplateNotFound:
            raise InvalidUsageError("template not found",404)
        except (ProgrammingError,OperationalError):
            raise InvalidUsageError('mysql connection or syntax is improper', 500)


    @staticmethod
    def check_user_in_db(user_name,password):
        # try:
            cur = mysql.connection.cursor()
            result_value = cur.execute("select * from user_data")
            user_details = cur.fetchall()
            for each_user in user_details:
                data = jwt.decode(each_user[3],app.config['secret_key'])
                if (each_user[1] == user_name) & (data['password'] == password):
                    return True
                    # return redirect(url_for('getbooks'))
            # return make_response(render_template('login_failed.html'))
            return False
        # except jinja2.exceptions.TemplateNotFound:
        #     raise InvalidUsageError("template not found",404)
        # except (ProgrammingError,OperationalError):
        #     raise InvalidUsageError('mysql connection or syntax is improper', 500)

            