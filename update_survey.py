"""
External script to update a survey and its questions.
"""

__author__ = "Jackson Eshbaugh"
__version__ = "03/12/2024"

from app import db, app
from models.survey_model import Survey
from models.survey_question_model import SurveyQuestion

print('Updating a survey...')

with app.app_context():
    # Prompt the user for the survey's name.
    survey_name = input('Enter the survey name to update: ')
    survey = db.session.execute(db.select(Survey).where(Survey.name == survey_name)).first()

    if not survey:
        print(f'Survey {survey_name} not found.')
        exit()

    survey = survey[0]

    # Prompt the user for the survey's name.
    new_survey_name = input(f'Enter the new name for the survey (or press Enter to keep "{survey_name}"): ')
    if new_survey_name:
        survey.name = new_survey_name
        db.session.commit()
        print(f'Survey name updated to "{new_survey_name}".')

    # Load with questions
    while True:
        # Prompt the user for the question.
        question_text = input('Enter a question for the survey (or press Enter to skip): ')
        if question_text == '':
            break

        # Create the question and add it to the survey.
        question = SurveyQuestion(survey_id=survey.id, question=question_text)
        db.session.add(question)
        db.session.commit()

        print(f'Question "{question_text}" added to survey {survey_name}.')

    # Print all questions and their ids
    print('Current questions:')
    for question in survey.questions:
        print(f'  {question.id}: {question.question}')

    # Prompt the user for a question id to delete.
    while True:
        question_id = input('Enter a question id to delete (or press Enter to skip): ')

        if question_id == '':
            break

        question = db.session.execute(db.select(SurveyQuestion).where(SurveyQuestion.id == question_id)).first()
        if not question:
            print(f'Question {question_id} not found.')
            continue

        db.session.delete(question[0])
        db.session.commit()
        print(f'Question {question_id} deleted.')
