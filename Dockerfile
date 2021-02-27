FROM python:3.8.5

WORKDIR /code

COPY requirements.txt /code

RUN python -m pip install --upgrade pip && \
    pip install -r /code/requirements.txt

COPY . /code

ENTRYPOINT sudo["/code/entrypoint.sh"]

# зачем мы делаем copy дважды? почему нельзя скопировать все выше
# а затем установить requirements


# CMD python manage.py makemigrations, python manage.py migrate, python manage.py collectstatic  --noinput

