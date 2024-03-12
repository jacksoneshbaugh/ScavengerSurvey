"""
A model of a survey, which contains a list of questions.
"""

__author__ = "Jackson Eshbaugh"
__version__ = "03/12/2024"

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app import db


class Survey(db.Model):
    """
    Survey model to hold a list of questions.
    :param id: The survey's id.
    :param name: The survey's name.
    :param questions: The survey's questions.
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    questions = relationship('SurveyQuestion', back_populates='survey')

    def __repr__(self):
        return f'<Survey {self.name}>'
