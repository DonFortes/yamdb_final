FROM python:3.8.5

WORKDIR /code

COPY . .

ENTRYPOINT sudo["/code/entrypoint.sh"]
