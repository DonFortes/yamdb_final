FROM python:3.8.5

WORKDIR /code

COPY . .

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

ENTRYPOINT ["/code/entrypoint.sh"]
