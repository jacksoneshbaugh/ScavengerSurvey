"""
Root of the BingoSurvey application.
This is a creative way to take a survey or play a progressive game
over some period of time.
"""

___author___ = "Jackson Eshbaugh"
___version___ = "03/11/2024"

import os

import bcrypt
import flask
import flask_login
from flask import Flask, render_template, url_for, redirect, get_flashed_messages
from dotenv import load_dotenv
from flask_login import login_required, current_user
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from validation_utils import validate_email, validate_password


class Base(DeclarativeBase):
    """
    Base class for all models.
    """
    pass


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Import models after db is created
from models.user_model import User

with app.app_context():
    db.create_all()

# Bingo Board consists of 5x5 grid of question objects (id and prompt and completed)
board = [
    {'id': 1, 'prompt': 'What is the capital of France?', 'completed': True},
    {'id': 2, 'prompt': 'What is the capital of Germany?', 'completed': False},
    {'id': 3, 'prompt': 'What is the capital of Italy?', 'completed': False},
    {'id': 4, 'prompt': 'What is the capital of Spain?', 'completed': False},
    {'id': 5, 'prompt': 'What is the capital of Portugal?', 'completed': False},
    {'id': 6, 'prompt': 'What is the capital of Belgium?', 'completed': False},
    {'id': 7, 'prompt': 'What is the capital of Netherlands?', 'completed': False},
    {'id': 8, 'prompt': 'What is the capital of Luxembourg?', 'completed': False},
    {'id': 9, 'prompt': 'What is the capital of Denmark?', 'completed': False},
    {'id': 10, 'prompt': 'What is the capital of Sweden?', 'completed': True},
    {'id': 11, 'prompt': 'What is the capital of Norway?', 'completed': False},
    {'id': 12, 'prompt': 'What is the capital of Finland?', 'completed': False},
    {'id': 13, 'prompt': 'What is the capital of Iceland?', 'completed': False},
    {'id': 14, 'prompt': 'What is the capital of Ireland?', 'completed': False},
    {'id': 15, 'prompt': 'What is the capital of United Kingdom?', 'completed': False},
    {'id': 16, 'prompt': 'What is the capital of Switzerland?', 'completed': False},
    {'id': 17, 'prompt': 'What is the capital of Austria?', 'completed': False},
    {'id': 18, 'prompt': 'What is the capital of Czech Republic?', 'completed': False},
    {'id': 19, 'prompt': 'What is the capital of Slovakia?', 'completed': False},
    {'id': 20, 'prompt': 'What is the capital of Hungary?', 'completed': False},
    {'id': 21, 'prompt': 'What is the capital of Poland?', 'completed': False},
    {'id': 22, 'prompt': 'What is the capital of Lithuania?', 'completed': False},
    {'id': 23, 'prompt': 'What is the capital of Latvia?', 'completed': False},
    {'id': 24, 'prompt': 'What is the capital of Estonia?', 'completed': False},
    {'id': 25, 'prompt': 'What is the capital of Russia?', 'completed': False}
]


# Routes

@app.route('/board')
# @login_required
def bingo_board():
    """
    Renders the bingo board.

    :return: the rendered bingo board.
    """

    messages = get_flashed_messages(with_categories=True)

    return render_template('board.html', title='Board', data=board, messages=messages)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the index page, unless the user is logged in. Then it redirects to the board.

    :return: the rendered index page.
    """

    messages = get_flashed_messages(with_categories=True)

    if current_user.is_authenticated:
        return redirect(url_for('board'))
    return render_template('index.html', title='Home', messages=messages)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders the login page or redirects to the board if the user is already logged in.
    Also logs the user in.
    :return: the rendered login page or a redirect to the board.
    """

    messages = get_flashed_messages(with_categories=True)

    if flask.request.method == 'GET':
        return render_template('login.html', title='Login', messages=messages)

    form = flask.request.form

    if form['email'] and form['password']:
        email = form['email']
        password = form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            flask_login.login_user(user)
            return redirect(url_for('board'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Renders the registration page or registers the user.
    :return: the rendered registration page or a redirect to the login page.
    """

    messages = get_flashed_messages(with_categories=True)

    if current_user.is_authenticated:
        return redirect(url_for('board'))

    if flask.request.method == 'GET':
        return render_template('register.html', title='Register', messages=messages)

    form = flask.request.form

    if form['email'] and form['password1'] and form['password2'] and form['name']:
        email = form['email']
        name = form['name']
        password1 = form['password1']
        password2 = form['password2']

        # Validate email and password
        email_valid = validate_email(email)
        password_valid = validate_password(password1, password2)

        # Compile all error messages and redirect if any errors

        if not email_valid:
            flash("Invalid email.", "error")

        if not password_valid[0]:
            flash("Password must be at least 8 characters.", "error")

        if not password_valid[1]:
            flash("Password must contain at least one number.", "error")

        if not password_valid[2]:
            flash("Password must contain at least one special character.", "error")

        if not password_valid[3]:
            flash("Passwords do not match.", "error")

        if not email_valid or not password_valid[0] or not password_valid[1] or not password_valid[2]:
            return redirect(url_for('register'))

        # We have valid entries at this point.
        # Next, check to see if the email is already in use.

        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email is already in use. Maybe you meant to login?", "error")
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Successfully registered! Please login.", "success")
        return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    """
    Logs the user out.
    :return: a redirect to the index page.
    """

    flask_login.logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
