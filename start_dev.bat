@echo off
REM This script is used to start BingoSurvey in development mode.

REM Define the location of the flask app
set FLASK_APP=bingo_survey

REM The .env file needs to be manually loaded or its variables set here or in the system.
REM We can't check that the file is complete due to batch limitations, so we'll just assume it's there.

REM Make sure the database is up to date
echo Applying any new database migrations...
flask db upgrade

REM Start the app (in development mode)
flask run