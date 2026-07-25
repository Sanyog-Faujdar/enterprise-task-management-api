#!/bin/sh

set -e

echo "Running migrations..."
flask --app run.py db upgrade

echo "Running seed..."
python seed.py

echo "Starting Gunicorn..."
exec gunicorn -w 2 -b 0.0.0.0:$PORT run:app