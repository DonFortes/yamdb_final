FROM python:3.8.5

WORKDIR /code

COPY . .

CMD pip install -r /code/requirements.txt

ENTRYPOINT gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

# ["/code/entrypoint.sh"]