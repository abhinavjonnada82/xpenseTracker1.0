FROM alpine:3.7
RUN apk update && apk add python3

USER root

COPY . /opt/parser

WORKDIR /opt/parser

RUN pip3 install --upgrade pip
RUN pip install requirements.txt