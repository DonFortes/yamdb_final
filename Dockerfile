FROM python:3.8.5

WORKDIR /code

COPY . /code

RUN ["chmod", "+x", "code/entrypoint.sh"]

ENTRYPOINT ["code/entrypoint.sh"]
