FROM python:3.8.5

WORKDIR /code

COPY requirements.txt /code

RUN python -m pip install --upgrade pip && \
    pip install -r /code/requirements.txt      
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic  --noinput

COPY . /code

# ENTRYPOINT ["code/entrypoint.sh"]
