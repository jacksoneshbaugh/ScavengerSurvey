"""
Top-level Admin script to manage the application.
Allows the user to create, update, toggle and delete surveys.
"""

import sys
import os
from datetime import datetime
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bingo_survey.models import Survey, SurveyQuestion, SurveyResponse
from bingo_survey import app, db

__author__ = "Jackson Eshbaugh"
__version__ = "03/12/2024"


# ANSI escape sequences for colors
class Colors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def list_surveys():
    """
    List all surveys, printing them out to the console.
    """
    surveys = db.session.execute(db.select(Survey)).all()
    print(Colors.HEADER + '+----------------------------------+' + Colors.ENDC)
    print(Colors.HEADER + '| All surveys:                     |' + Colors.ENDC)
    for survey in surveys:
        survey = survey[0]
        active = Colors.OKGREEN + '[Active]' + Colors.HEADER if survey.active else (Colors.WARNING + '[Inactive]' +
                                                                                    Colors.HEADER)
        print(Colors.HEADER + f'| {survey.id}. {survey.name} {active}            |' + Colors.ENDC)

    print(Colors.HEADER + '+----------------------------------+\n' + Colors.ENDC)


def list_questions(survey):
    """
    Given a survey, print out all of its questions.
    :param survey: the survey to select a question from
    """

    questions = db.session.execute(db.select(SurveyQuestion).where(SurveyQuestion.survey_id == survey.id)).all()

    if not questions:
        print(Colors.WARNING + 'No questions found for this survey. Start by adding some questions.' + Colors.ENDC)
        return

    print(Colors.HEADER + '+----------------------------------+' + Colors.ENDC)
    print(Colors.HEADER + f'| Questions for {survey.name}:     |' + Colors.ENDC)
    print(Colors.HEADER + '+----------------------------------+' + Colors.ENDC)

    for question in questions:
        question = question[0]
        print(f'{question.id}: {question.question}')


def select_survey(task_verb):
    """
    Select a survey by ID.
    :param task_verb: the verb to use in the prompt
    :return: the selected survey
    """
    list_surveys()

    selection = input(
        f'Enter the ID of the survey you\'d like to {task_verb} (or press Enter to return to the main menu): ')

    if selection == '':
        return None

    survey = db.session.execute(db.select(Survey).where(Survey.id == selection)).first()

    if not survey:
        print(Colors.FAIL + f'Survey with ID {selection} not found. Please try again.' + Colors.ENDC)
        return select_survey(task_verb)

    return survey[0]


def select_question(survey, action_verb):
    """
    Given a survey, select a question by ID.
    :param survey: the survey to select a question from
    :param action_verb: the action verb to use in the prompt
    :return: the selected question
    """

    list_questions(survey)

    question_id = input(
        f'Enter the ID of the question you\'d like to {action_verb} (or press Enter to return to the update menu): ')

    if question_id == '':
        return None

    question = db.session.execute(db.select(SurveyQuestion).where(SurveyQuestion.id == question_id)).first()[0]

    if not question:
        print(Colors.FAIL + f'Question with ID {question_id} not found. Please try again.' + Colors.ENDC)
        return select_question(survey, action_verb)

    return question


def update_survey():
    """
    Update a survey and its questions.
    """

    print('Let\'s update a survey.')

    # Select a survey
    survey = select_survey('update')

    if not survey:
        # User chose to return to the main menu
        return

    while True:
        print(Colors.HEADER + '+----------------------------------+' + Colors.ENDC)
        print(Colors.HEADER + f'| Updating {survey.name}.     |' + Colors.ENDC)
        print(Colors.HEADER + '| 1. Update survey [n]ame          |' + Colors.ENDC)
        print(Colors.HEADER + '| 2. [A]dd survey questions        |' + Colors.ENDC)
        print(Colors.HEADER + '| 3. [L]ist survey questions       |' + Colors.ENDC)
        print(Colors.HEADER + '| 4. [E]dit a survey question      |' + Colors.ENDC)
        print(Colors.HEADER + '| 5. [R]emove survey questions     |' + Colors.ENDC)
        print(Colors.HEADER + '| 6. Return to [m]ain menu         |' + Colors.ENDC)
        print(Colors.HEADER + '+----------------------------------+' + Colors.ENDC)

        choice = input('Enter a choice: ').lower()

        if choice == 'n' or choice == '1':
            new_name = input(f'Enter a new name for {survey.name} (or press Enter to return to the update menu): ')

            if new_name == '':
                continue

            old_name = survey.name
            survey.name = new_name
            db.session.commit()
            print(f'Survey name updated: "{old_name}" -> "{new_name}".')

        elif choice == 'a' or choice == '2':
            # Add survey questions
            while True:
                question_text = input('Enter a question for the survey (or press Enter to return to the update menu): ')
                if question_text == '':
                    break

                question = SurveyQuestion(survey_id=survey.id, question=question_text)
                db.session.add(question)
                db.session.commit()

                print(f'Question "{question_text}" added to survey {survey.name}.')
        elif choice == 'l' or choice == '3':
            # List survey questions
            list_questions(survey)
        elif choice == 'e' or choice == '4':
            # Edit a survey question

            question = select_question(survey, 'edit')

            if not question:
                # User chose to return to the update menu
                continue

            new_question = input(
                f'Enter the new question for the survey (or press Enter to keep "{question.question}"): ')

            if new_question:
                question.question = new_question
                db.session.commit()
                print(f'Question updated to "{new_question}".')
            else:
                print('No changes made.')

        elif choice == 'r' or choice == '5':
            # Remove survey questions

            question = select_question(survey, 'remove')

            if not question:
                # User chose to return to the update menu
                continue

            db.session.delete(question)
            db.session.commit()
            print(Colors.OKGREEN + f'Question "{question.question}" removed from survey {survey.name}.' + Colors.ENDC)

        elif choice == 'm' or choice == '6':
            print('Returning to the main menu.')
            break
        else:
            print('Invalid choice. Please try again.')


def create_survey():
    """
    Create a survey and add questions to it.
    """

    print('OK, let\'s create a survey.')
    print('Firstly, we need a name for the survey.')

    survey_name = input('Survey Name (this can be changed later): ')
    survey = Survey(name=survey_name, active=False)
    db.session.add(survey)
    db.session.commit()

    print(Colors.OKGREEN + f'Survey {survey_name} created and added to the database.' + Colors.ENDC)
    print(Colors.OKGREEN + f'Now, let\'s add some questions to {survey_name}.' + Colors.ENDC)

    while True:
        question_text = input('Enter a question for the survey (or press Enter to return to the main menu): ')
        if question_text == '':
            break

        question = SurveyQuestion(survey_id=survey.id, question=question_text)
        db.session.add(question)
        db.session.commit()

        print(Colors.OKGREEN + f'Question "{question_text}" added to survey {survey_name}.' + Colors.ENDC)

    print(
        Colors.OKGREEN + 'Survey creation complete. Remember, you\'ll need to activate this survey to accept '
                         'responses.' + Colors.ENDC)


def toggle_survey():
    """
    Toggles a survey's active status.
    """

    survey = select_survey('toggle')

    if not survey:
        # User chose to return to the main menu
        return

    # Toggle the survey's active status
    survey.active = not survey.active
    new_status = 'active' if survey.active else 'inactive'
    db.session.commit()

    print(Colors.OKGREEN + f'Survey {survey.name} is now {new_status}.' + Colors.ENDC)


def delete_survey():
    """
    Delete a survey and its questions. The active survey cannot be deleted.
    """

    survey = select_survey('delete')

    if not survey:
        # User chose to return to the main menu
        return

    if survey.active:
        print(Colors.FAIL + f'Survey {survey.name} is the active survey and cannot be deleted.' + Colors.ENDC)
        return

    # Confirm the user wants to delete the survey
    confirm = input(
        Colors.WARNING + f'Are you sure you want to delete survey {survey.name}? [y/n]: ' + Colors.ENDC).lower()

    if confirm != 'y':
        print('Survey deletion cancelled.')
        return

    # Delete the survey's questions
    for question in survey.questions:
        db.session.delete(question)

    # Delete the survey
    db.session.delete(survey)
    db.session.commit()
    print(Colors.OKGREEN + f'Survey {survey.name} deleted.' + Colors.ENDC)


def export_results():
    """
    Export the results of a survey to a CSV file. Only inactive surveys can have their data exported.
    """

    print('OK, let\'s export the results of a survey.')
    print('Firstly, we need to select a survey.')

    survey = select_survey('export')

    if not survey:
        # User chose to return to the main menu
        return

    if survey.active:
        print(Colors.FAIL + f'Survey {survey.name} is active and cannot have its results exported. Deactivate it to '
                            f'export its results.' + Colors.ENDC)
        return

    print(Colors.OKGREEN + f'Exporting results for survey {survey.name}.' + Colors.ENDC)

    questions = db.session.execute(db.select(SurveyQuestion).where(SurveyQuestion.survey_id == survey.id)).all()

    if not questions:
        print(Colors.WARNING + 'No questions found for this survey. Start by adding some questions.' + Colors.ENDC)
        return

    if not os.path.exists(f'results/{survey.name}'):
        os.makedirs(f'results/{survey.name}')

    with open(f'results/{survey.name}/{survey.name}_results_{datetime.now()}.csv', 'w') as file:
        writer = csv.writer(file)

        # Header
        writer.writerow(['User ID', 'Question ID', 'Question', 'Response'])

        for question in questions:
            question = question[0]

            # find all responses for this question
            responses = db.session.execute(db.select(SurveyResponse).where(SurveyResponse.question_id == question.id)).all()

            for response in responses:
                response = response[0]
                writer.writerow([response.user_id, response.question_id, question.question, response.response])

    print(Colors.OKGREEN + f'Results exported to admin/results/{survey.name}/{survey.name}_results_{datetime.now()}.csv'
          + Colors.ENDC)


with app.app_context():
    print('           ADMIN CONSOLE')
    print(Colors.HEADER + '+----------------------------------+' + Colors.ENDC)
    print(Colors.HEADER + '| Welcome to the BingoSurvey Admin |' + Colors.ENDC)
    print(Colors.HEADER + '| console. You can manage surveys  |' + Colors.ENDC)
    print(Colors.HEADER + '| here.                            |' + Colors.ENDC)
    print(Colors.HEADER + '+----------------------------------+\n' + Colors.ENDC)

    while True:
        print(Colors.HEADER + '+--------------------------------+' + Colors.ENDC)
        print(Colors.HEADER + '|          MAIN MENU             |' + Colors.ENDC)
        print(Colors.HEADER + '| 1. [C]reate a survey           |' + Colors.ENDC)
        print(Colors.HEADER + '| 2. [U]pdate a survey           |' + Colors.ENDC)
        print(Colors.HEADER + '| 3. [T]oggle a survey\'s status  |' + Colors.ENDC)
        print(Colors.HEADER + '| 4. [D]elete a survey           |' + Colors.ENDC)
        print(Colors.HEADER + '| 5. [L]ist all surveys          |' + Colors.ENDC)
        print(Colors.HEADER + '| 6. [E]xport results            |' + Colors.ENDC)
        print(Colors.HEADER + '| 7. [Q]uit                      |' + Colors.ENDC)
        print(Colors.HEADER + '+--------------------------------+' + Colors.ENDC)

        choice = input('Enter a choice: ').lower()

        if choice == 'c' or choice == '1':
            create_survey()
        elif choice == 'u' or choice == '2':
            update_survey()
        elif choice == 't' or choice == '3':
            toggle_survey()
        elif choice == 'd' or choice == '4':
            delete_survey()
        elif choice == 'l' or choice == '5':
            list_surveys()
        elif choice == 'e' or choice == '6':
            export_results()
        elif choice == 'q' or choice == '7':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Please try again.')
