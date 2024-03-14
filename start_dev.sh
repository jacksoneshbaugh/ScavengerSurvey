#!/usr/bin/env bash

# This script is used to start BingoSurvey in development mode.

# Define the location of the flask app
export FLASK_APP=bingo_survey

# Make sure the database is up to date
echo "Applying any new database migrations..."
flask db upgrade

# Start the app (in development mode)
flask run