from flask import render_template,make_response
class DataBase:    
    @staticmethod
    def add_to_db(data):
        try:
            user_name = data['user_name']
            email =  data['email']
            # password = data['password']
            # pass_token = jwt.encode({'password':password},app.config['secret_key'])
            # cur = mysql.connection.cursor()
            # cur.execute("INSERT INTO userinfo(user_name,email,password) VALUES(%s,%s,%s)"
            #     ,(user_name,email,pass_token))
            # mysql.connection.commit()
            # cur.close()
            return make_response(render_template('register_sucess.html'))
        except:
            pass