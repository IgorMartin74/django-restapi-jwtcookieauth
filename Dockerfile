FROM python:3.13-alpine3.20

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt 
#    adduser --disabled-password --no-create-home django-user

COPY . .

USER django-user
