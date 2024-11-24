# pull official image
FROM python:3.12-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apt update \
    && apt install -y gcc g++ python3-dev libpq-dev librdkafka-dev

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
# run flake8
RUN pip install flake8
RUN flake8 --ignore=E501
