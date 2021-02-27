#!/bin/sh
python3 -m pip install --upgrade pip
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic  --noinput
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000


exec "$@"
