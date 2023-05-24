FROM python:3.10-alpine

WORKDIR /usr/scr/trucklocator
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN adduser --disabled-password trucklocator-user

USER trucklocator-user

COPY . .