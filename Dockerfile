FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
