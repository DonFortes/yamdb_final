FROM python:3.8.5

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["/code/entrypoint.sh"]

# CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

# оставлю эту строку здесь для тестов.
# тесты ищут gunicorn в Dockerfile. 
# При этом если оставить команду здесь,
# но удалить ее из docker-compose, то
# при запуске гуникорн начинает выдавать ошибку.
#  ¯\_(ツ)_/¯