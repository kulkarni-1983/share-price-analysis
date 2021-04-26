FROM python:3.8-alpine

RUN apk add --no-cache --virtual builddeps gcc musl-dev && \
   pip --no-cache-dir install aws-sam-cli awscli autopep8 && \
   apk del builddeps
