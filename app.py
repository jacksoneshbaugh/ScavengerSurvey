"""
Root of the BingoSurvey application.
This is a creative way to take a survey or play a progressive game
over some period of time.
"""

___author___ = "Jackson Eshbaugh"
___version___ = "03/11/2024"

import logging
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

from validation_utils import validate_email, validate_password, escape_string


class Base(DeclarativeBase):
    """
    Base class for all models.
    """
    pass


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = os.getenv('SESSION_COOKIE_HTTPONLY').lower() == 'true'
app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Import models after db is created
from models.user_model import User
from models.survey_model import Survey
from models.survey_question_model import SurveyQuestion
from models.survey_response_model import SurveyResponse

with app.app_context():
    db.create_all()


# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the index page, unless the user is logged in. Then it redirects to the board.

    :return: the rendered index page.
    """

    if current_user.is_authenticated:
        return redirect(url_for('bingo_board'))
    return render_template('index.html', title='Home')


@app.route('/board', methods=['GET', 'POST'])
@login_required
def bingo_board():
    """
    Renders a bingo board survey.

    :return: the rendered bingo board.
    """

    if flask.request.method == 'POST':
        form = flask.request.form
        # Ony receive one response to one question each time
        question_id = form['prompt_id']
        response = form['response']

        if not response or not question_id:
            return redirect(url_for('bingo_board'))

        # save the response - if it exists, update it

        survey_response = (db.session.execute(db.select(SurveyResponse).where(SurveyResponse.user_id == current_user.id,
                                                                              SurveyResponse.question_id == question_id))
                           .first())
        if survey_response:
            survey_response = survey_response[0]
            survey_response.response = response
            db.session.commit()
            return redirect(url_for('bingo_board'))

        # The question hasn't been answered yet, so add a new response

        survey_response = SurveyResponse(user_id=current_user.id, question_id=question_id, response=response)
        db.session.add(survey_response)
        db.session.commit()

    # Get the survey from the database
    survey = db.session.execute(db.select(Survey).where(Survey.active == True)).first()[0]

    # Construct the board to send to the view
    board = []
    for question in survey.questions:
        # Check if the user has responded to the question
        response = (db.session.execute(db.select(SurveyResponse).where(SurveyResponse.user_id == current_user.id,
                                                                       SurveyResponse.question_id == question.id))
                    .first())
        if response:
            response = response[0]

        board.append({'id': question.id, 'prompt': question.question,
                      'response': response.response if response else ''})

    return render_template('board.html', title=survey.name, data=board, escape_string=escape_string)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Renders the login page or redirects to the board if the user is already logged in.
    Also logs the user in.
    :return: the rendered login page or a redirect to the board.
    """

    if current_user.is_authenticated:
        return redirect(url_for('bingo_board'))

    if flask.request.method == 'GET':
        return render_template('login.html', title='Login')

    form = flask.request.form

    if not form['email']:
        flash("Email is required.", "error")

    if not form['password']:
        flash("Password is required.", "error")

    if not form['email'] or not form['password']:
        return redirect(url_for('login'))

    email = form['email']
    password = form['password']

    result = db.session.execute(db.select(User).where(User.email == email)).first()
    user = result[0] if result else None

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

        user.authenticated = True
        db.session.commit()

        if flask_login.login_user(user):
            return redirect(url_for('bingo_board'))
        else:
            flash("Error authenticating", "error")
            return redirect(url_for('login'))
    else:
        flash("Invalid email and password combination.", "error")
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Renders the registration page or registers the user.
    :return: the rendered registration page or a redirect to the login page.
    """

    # if current_user.is_authenticated:
    #    return redirect(url_for('bingo_board'))

    if flask.request.method == 'GET':
        return render_template('register.html', title='Register')

    form = flask.request.form

    # Ensure all fields are filled out
    if not form['email']:
        flash("Email is required.", "error")
        print("Email is required.")

    if not form['password1']:
        flash("Password is required.", "error")
        print("Password is required.")

    if not form['password2']:
        flash("Password confirmation is required.", "error")
        print("Password confirmation is required.")

    if not form['name']:
        flash("Name is required.", "error")
        print("Name is required.")

    if not form['email'] or not form['password1'] or not form['password2'] or not form['name']:
        return redirect(url_for('register'))

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

    if not email_valid or not password_valid[0] or not password_valid[1] or not password_valid[2] or not password_valid[
        3]:
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

    user = current_user
    user.authenticated = False
    db.session.commit()
    flask_login.logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
