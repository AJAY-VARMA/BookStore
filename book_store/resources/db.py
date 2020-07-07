from flask import render_template,make_response,url_for,redirect
import sys,os
sys.path.append('.')
from app import app
import jwt
from flask_mysqldb import MySQL

mysql = MySQL(app)

class DataBase:
    @staticmethod
    def get_data_from_db():
        try:
            cur = mysql.connection.cursor()
            result_value = cur.execute("select * from products_data")
            user_details = cur.fetchall()
            cur.close()
            return user_details
        except:
            pass

    @staticmethod
    def add_to_db(data):
        try:
            user_name = data['user_name']
            email =  data['email']
            password = data['password']
            pass_token = jwt.encode({'password':password},app.config['secret_key'])
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user_data(Username,email,password) VALUES(%s,%s,%s)"
                ,(user_name,email,pass_token))
            mysql.connection.commit()
            cur.close()
            return make_response(render_template('register_sucess.html'))
        except:
            pass

    @staticmethod
    def check_user_in_db(user_name,password):
        try:
            cur = mysql.connection.cursor()
            result_value = cur.execute("select * from user_data")
            user_details = cur.fetchall()
            for each_user in user_details:
                data = jwt.decode(each_user[3],app.config['secret_key'])
                if (each_user[1] == user_name) & (data['password'] == password):
                    return redirect(url_for('getbooks'))
            return make_response(render_template('login_failed.html'))
        except:
            pass
            