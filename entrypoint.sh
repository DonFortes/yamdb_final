#!/bin/sh
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py collectstatic  --noinput
exec "$@"
