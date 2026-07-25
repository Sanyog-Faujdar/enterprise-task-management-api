#!/bin/sh

set -e

echo "Running migrations..."
flask --app run.py db upgrade

echo "Running seed..."
python seed.py

echo "Starting application..."
python run.py