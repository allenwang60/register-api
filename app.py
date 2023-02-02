from flask import Flask, render_template, request, url_for
from pymongo import MongoClient
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import input_required, length, ValidationError
from flask_wtf.csrf import CSRFProtect, CSRFError


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config["SECRET_KEY"] = 'any secret string'

client = MongoClient("mongodb://localhost:27017/")
db = client["database"]
user = db["users"]

class RegisterForm(FlaskForm):
    username = StringField(validators=[input_required(), length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[input_required(), length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        username = user.query.filter_by(username=username.data).first()

        if username:
            raise ValidationError("That username already exists. Please choose a different one.")





@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/')
def login():
    return render_template('/Home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = user.find_one({'username' : request.form['username']})

        if account:
            error = 'Account already exists !'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'email is required.'


    return render_template('/register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)