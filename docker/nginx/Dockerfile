FROM nginx

RUN apt-get update \
 && apt-get install -y git nano curl zlib1g-dev

COPY codetube.conf /etc/nginx/sites-available/

RUN ln /etc/nginx/sites-available/codetube.conf /etc/nginx/conf.d/

RUN mkdir /codetube

WORKDIR /codetube