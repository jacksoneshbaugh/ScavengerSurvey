"""
A model of a survey question.
"""

__author__ = "Jackson Eshbaugh"
__version__ = "03/12/2024"

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class SurveyQuestion(db.Model):
    """
    Survey question model.
    :param id: The question's id.
    :param survey_id: The id of the survey the question is associated with.
    :param question: The question.
    :param responses: The responses to the question.
    """

    id = Column(Integer, primary_key=True)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    question = Column(String(500), nullable=False)

    responses = relationship('SurveyResponse', back_populates='question')

    survey = relationship('Survey', back_populates='questions')

    def __repr__(self):
        return f'<SurveyQuestion {self.question}>'
