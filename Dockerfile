FROM python:3.8.5

WORKDIR /code

COPY . .

ENTRYPOINT ["/code/entrypoint.sh"]
