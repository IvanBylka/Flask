from flask import Flask, jsonify
from flask import request
from flask import render_template_string,render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    name: Mapped[str] = mapped_column(db.String(128), nullable=False)
    email: Mapped[str] = mapped_column(db.String(128), nullable=False)
    data: Mapped[str] = mapped_column(db.String(128), nullable=False)

    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return  check_password_hash(self.password, password)

with app.app_context():
    db.create_all()


@app.route
def get_users():
    users = Users.query.all()

    users_data = [
        {
            'id' : user.id,
            'name': user.name,
            'email': user.email,
            'data': user.data
        }
        for user in users
    ]
    return jsonify(users_data)


@app.route('/')
def index():
    return render_template("index.html")
# @app.route("/register",methods = ['GET',"POST"])
# def register():
#     return render_template("register.html")
def show_the_login_form():
    return render_template_string("""
        <form method="POST">
            <h3>Login</h3>
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login"> 
        </form>
    """)


def do_the_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "username" and password == "password":
        return index()
    else:
        return "Invalid credentials. Please try again."


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


def show_the_registration():
    return render_template("register.html")


def do_the_registration():
    email = request.form.get('email')
    first_password = request.form.get('firstpassword')
    second_password = request.form.get('secondpassword')

    if first_password != second_password:
        return "Пароли не совпадают!"

    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return "Такой пользователь уже существует. Пожалуйста выберите другое имя пользвателя"


@app.route("/register",methods=['GET',"POST"])
def registation():
    if request.method == "POST":
        return do_the_registration()
    else:
        return show_the_registration()


app.run(debug=True)
