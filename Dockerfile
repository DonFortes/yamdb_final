FROM python:3.8.5

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . .

RUN pip install -r /code/requirements.txt 

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

# ENTRYPOINT gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

# ["/code/entrypoint.sh"]