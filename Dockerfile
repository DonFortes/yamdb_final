FROM python:3.8.5

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . .

RUN pip install -r /code/requirements.txt
