from wtforms import Form,StringField,TextAreaField,PasswordField,validators

class RegisterForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [
        validators.Length(min=8, max=50),
        validators.EqualTo('confirm')
    ])
    confirm = PasswordField('confirm')

class LoginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Length(min=8, max=50)])