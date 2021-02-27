FROM python:3.8.5

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . .

RUN pip install -r /code/requirements.txt 

CMD ls -l

# ENTRYPOINT gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

# ["/code/entrypoint.sh"]