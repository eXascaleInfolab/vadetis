# pull the official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /usr/src/app

RUN apk add --no-cache postgresql-dev
RUN apk add --no-cache build-base
RUN apk add --no-cache gfortran openblas-dev lapack-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache libffi-dev openssl-dev python3-dev
RUN apk add --no-cache zeromq zeromq-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements_slow.txt /usr/src/app
RUN pip install -r requirements_slow.txt

COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

RUN apk add --no-cache bash
RUN python3 setup.py build_ext --inplace
