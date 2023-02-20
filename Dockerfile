# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /app

COPY . /app/

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --user

CMD [ "python3", "main.py" ]
