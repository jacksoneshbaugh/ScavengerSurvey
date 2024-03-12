"""
A separate script to create a survey and add questions to it.
"""

__author__ = "Jackson Eshbaugh"
__version__ = "03/12/2024"

from app import db, app
from models.survey_model import Survey
from models.survey_question_model import SurveyQuestion

print('Creating a survey...')

with app.app_context():
    # Prompt the user for the survey's name.
    survey_name = input('Enter the survey name: ')
    survey = Survey(name=survey_name, active=False)
    db.session.add(survey)
    db.session.commit()

    print(f'Survey {survey_name} created.')

    # Load with questions
    while True:
        # Prompt the user for the question.
        question_text = input('Enter a question for the survey (or "q" to quit): ')
        if question_text == 'q':
            break

        # Create the question and add it to the survey.
        question = SurveyQuestion(survey_id=survey.id, question=question_text)
        db.session.add(question)
        db.session.commit()

        print(f'Question "{question_text}" added to survey {survey_name}.')

print('Survey creation complete.')
