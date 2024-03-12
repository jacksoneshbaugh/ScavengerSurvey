"""
Given a survey name, toggle the survey's active status.
"""

__author__ = "Jackson Eshbaugh"
__version__ = "03/12/2024"

from app import db, app
from models.survey_model import Survey

with app.app_context():
    survey_name = input('Enter the survey name to toggle: ')

    # Only one survey can be active, so don't toggle one off, only toggle on and then all others out.

    survey = db.session.execute(db.select(Survey).where(Survey.name == survey_name)).first()[0]

    if not survey:
        print(f'Survey {survey_name} not found.')
        exit()

    if survey.active:
        print(f'Survey {survey_name} is already active.')
        exit()

    # Deactivate all surveys
    db.session.execute(db.update(Survey).values(active=False))

    # Activate the selected survey
    survey.active = True
    db.session.commit()

print(f'Survey {survey_name} is now the active survey.')
