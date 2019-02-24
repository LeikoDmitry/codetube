FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
 && apt-get install -y git nano curl zlib1g-dev python3-dev default-libmysqlclient-dev

RUN mkdir /codetube
WORKDIR /codetube
ADD requirements.txt /codetube/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt