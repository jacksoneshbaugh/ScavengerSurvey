"""
A model to hold a user's responses to the survey questions.
"""
__author__ = "Jackson Eshbaugh"
__version__ = "03/12/2024"

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class SurveyResponse(db.Model):
    """
    Survey response model to hold a user's response to a particular survey question.
    :param id: The response's id.
    :param user_id: The id of the user who responded.
    :param question_id: The id of the question that was responded to.
    :param response: The user's response to the question.
    """

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    question_id = Column(Integer, ForeignKey('survey_question.id'))
    response = Column(String(500), nullable=False)

    user = relationship('User', back_populates='responses')
    question = relationship('SurveyQuestion', back_populates='responses')

    def __repr__(self):
        return f'<SurveyResponse {self.response}>'
