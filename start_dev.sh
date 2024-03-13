#!/usr/bin/env bash

# This script is used to start BingoSurvey in development mode.

# Define the location of the flask app
export FLASK_APP=bingo_survey

# Make sure the environment is set up (.env file defines all the environment variables)
source /.env

# check that the required environment variables are set
if [ -z "$SECRET_KEY" ]; then
  echo "SECRET_KEY is not set. Please set it in the .env file."
  exit 1
fi

if [ -z "$SESSION_COOKIE_SECURE" ]; then
  echo "SESSION_COOKIE_SECURE is not set. Please set it in the .env file."
  exit 1
fi

if [ -z "$SESSION_COOKIE_HTTPONLY" ]; then
  echo "SESSION_COOKIE_HTTPONLY is not set. Please set it in the .env file."
  exit 1
fi

if [ -z "$SESSION_COOKIE_SAMESITE" ]; then
  echo "SESSION_COOKIE_SAMESITE is not set. Please set it in the .env file."
  exit 1
fi

if [ -z "$DATABASE_URI" ]; then
  echo "DATABASE_URI is not set. Please set it in the .env file."
  exit 1
fi

# Make sure the database is up to date
echo "Applying any new database migrations..."
flask db upgrade

# Start the app (in development mode)
flask run