FROM python:3.8.5

WORKDIR /code

COPY requirements.txt /code

RUN python -m pip install --upgrade pip && \
    pip install -r /code/requirements.txt      

COPY . /code

ENTRYPOINT ["code/entrypoint.sh"]
