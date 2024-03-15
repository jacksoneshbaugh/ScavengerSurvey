#!/usr/bin/env bash

# This script is used to start BingoSurvey in production mode.
# This should ONLY run inside the Docker container built for production.

# Change directory in case this is run manually
cd /usr/src/app/

# Define the location of the flask app
export FLASK_APP=bingo_survey

# check that the required environment variables are set
if [ -z "$SECRET_KEY" ]; then
  echo "SECRET_KEY is not set."
  exit 1
fi

if [ -z "$SESSION_COOKIE_SECURE" ]; then
  echo "SESSION_COOKIE_SECURE is not set."
  exit 1
fi

if [ -z "$SESSION_COOKIE_HTTPONLY" ]; then
  echo "SESSION_COOKIE_HTTPONLY is not set."
  exit 1
fi

if [ -z "$SESSION_COOKIE_SAMESITE" ]; then
  echo "SESSION_COOKIE_SAMESITE is not set."
  exit 1
fi

if [ -z "$DATABASE_URI" ]; then
  echo "DATABASE_URI is not set."
  exit 1
fi

# Make sure the database is up to date -
#  This must be done here and not in the image build because
#  this container could be swapped while retaining the old
#  database volume.
echo "Applying any new database migrations..."
flask db upgrade

# Start the app (in development mode)
python -m gunicorn bingo_survey:app -c gunicorn.conf.py
