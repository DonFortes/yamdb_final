FROM python:3.8.5

WORKDIR /code

COPY . .

CMD pip install -r /code/requirements.txt

ENTRYPOINT ["/code/entrypoint.sh"]
