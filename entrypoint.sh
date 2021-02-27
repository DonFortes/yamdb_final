#!/bin/sh
pip install -r /code/requirements.txt
python3 -m pip install --upgrade pip
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py collectstatic  --noinput
exec "$@"
