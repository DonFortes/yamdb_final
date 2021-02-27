FROM python:3.8.5

WORKDIR /code

COPY . /code

RUN sudo chmod u+x entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
