FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

COPY create_superuser.py /app/create_superuser.py

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python /app/create_superuser.py