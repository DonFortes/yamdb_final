#!/bin/sh
sudo python manage.py makemigrations
sudo python manage.py migrate
sudo python manage.py collectstatic  --noinput
exec "$@"
