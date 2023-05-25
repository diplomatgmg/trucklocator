FROM python:3.10-alpine

WORKDIR /usr/src/trucklocator
EXPOSE 8000
EXPOSE 5555
EXPOSE 6379
EXPOSE 45484

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN adduser --disabled-password trucklocator-user
RUN chown -R trucklocator-user:trucklocator-user /usr/src/trucklocator

USER trucklocator-user

COPY . .
