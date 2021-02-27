FROM python:3.8.5

WORKDIR /code

COPY requirements.txt /code

RUN python -m pip install --upgrade pip && \
    pip install -r /code/requirements.txt      
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic  --noinput

COPY . /code

# ENTRYPOINT ["code/entrypoint.sh"]
