FROM php:8.0-apache

RUN apt-get update && \
    apt-get install -y \
        libzip-dev \
        unzip \
        && \
    docker-php-ext-install pdo_mysql && \
    a2enmod rewrite && \
    service apache2 restart

WORKDIR /var/www/html

COPY ./src ./
EXPOSE 80