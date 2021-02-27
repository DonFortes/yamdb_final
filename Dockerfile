FROM python:3.8.5

WORKDIR /code

COPY . /code

RUN chmod u+x entrypoint.sh

ENTRYPOINT ["code/entrypoint.sh"]
