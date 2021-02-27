FROM python:3.8.5

WORKDIR /code

COPY requirements.txt /code

RUN ["chmod", "+x", "code/entrypoint.sh"]

COPY . /code
