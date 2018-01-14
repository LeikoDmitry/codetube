#FROM php:7.1-apache
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
 && apt-get install -y git nano curl zlib1g-dev python3-dev libmysqlclient-dev

#RUN apt-get update \
# && apt-get install -y libapache2-mod-wsgi-py3 python3-pip
#ADD codetube.conf /etc/apache2/sites-available/
#RUN a2ensite codetube.conf
RUN mkdir /codetube
WORKDIR /codetube
ADD requirements.txt /codetube/
RUN pip3 install -r requirements.txt
ADD . /codetube/