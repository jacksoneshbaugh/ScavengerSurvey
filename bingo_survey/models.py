"""
Models for the Bingo Survey application.
"""
__author__ = "Jackson Eshbaugh"
__version__ = "03/13/2024"

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Relationship

from bingo_survey import login_manager, db


class Survey(db.Model):
    """
    Survey model to hold a list of questions.
    :param id: The survey's id.
    :param name: The survey's name.
    :param questions: The survey's questions.
    """

    id: Integer = Column(Integer, primary_key=True)
    name: String = Column(String(80), nullable=False)
    active: Boolean = Column(Boolean, nullable=False, default=True)

    questions = relationship('SurveyQuestion', back_populates='survey')

    def __repr__(self) -> str:
        return f'<Survey {self.name}>'


class SurveyQuestion(db.Model):
    """
    Survey question model.
    :param id: The question's id.
    :param survey_id: The id of the survey the question is associated with.
    :param question: The question.
    :param responses: The responses to the question.
    """

    id: Integer = Column(Integer, primary_key=True)
    survey_id: Integer = Column(Integer, ForeignKey('survey.id'))
    question: String = Column(String(500), nullable=False)

    responses: Relationship = relationship('SurveyResponse', back_populates='question')

    survey: Relationship = relationship('Survey', back_populates='questions')

    def __repr__(self) -> str:
        return f'<SurveyQuestion {self.question}>'


class SurveyResponse(db.Model):
    """
    Survey response model to hold a user's response to a particular survey question.
    :param id: The response's id.
    :param user_id: The id of the user who responded.
    :param question_id: The id of the question that was responded to.
    :param response: The user's response to the question.
    """

    id: Integer = Column(Integer, primary_key=True)
    user_id: Integer = Column(Integer, ForeignKey('user.id'))
    question_id: Integer = Column(Integer, ForeignKey('survey_question.id'))
    response: String = Column(String(500), nullable=False)

    user: Relationship = relationship('User', back_populates='responses')
    question: Relationship = relationship('SurveyQuestion', back_populates='responses')

    def __repr__(self) -> str:
        return f'<SurveyResponse {self.response}>'


class User(db.Model):
    """
    User model.

    :param id: The user's id.
    :param name: The user's name.
    :param email: The user's email.
    :param password: The user's password. Will be hashed.
    :param authenticated: Whether the user is authenticated.
    """
    id: Integer = Column(Integer, primary_key=True)
    name: String = Column(String(80), unique=True, nullable=False)
    email: String = Column(String(120), unique=True, nullable=False)
    password: String = Column(String(80), nullable=False)
    authenticated: Boolean = Column(Boolean, default=False)

    responses: Relationship = relationship('SurveyResponse', back_populates='user')

    def __repr__(self) -> str:
        return f'<User {self.email}>'

    @property
    def is_authenticated(self) -> Boolean:
        """
        Checks if the user is authenticated.
        :return: True if the user is authenticated, False otherwise.
        """
        return self.authenticated

    def get_id(self) -> Integer:
        """
        Gets the user's id.
        :return: The user's id.
        """
        return self.id

    @property
    def is_active(self) -> bool:
        """
        All users are active.
        :return: True
        """
        return True

    @property
    def is_anonymous(self) -> bool:
        """
        Anonymous users are not supported.
        :return: False
        """
        return False


pass


@login_manager.user_loader
def user_loader(user_id) -> User | None:
    """
     Given a *user_id*, return the associated User object.
     :return: The User object.
     """
    result = db.session.execute(db.select(User).where(User.id == user_id)).first()
    return result[0] if result else None


@login_manager.request_loader
def request_loader(request) -> User | None:
    """
     Given a *request*, return a User object or None.
     :return: The User object or None.
    """
    email = request.form.get('email')
    result = db.session.execute(db.select(User).where(User.email == email)).first()
    return result[0] if result else None
