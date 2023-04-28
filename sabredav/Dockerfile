FROM php:8.2.5-fpm-bullseye

RUN curl -sSL https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions -o - | sh -s @composer sockets 
COPY php-fpm.conf /usr/local/etc/php-fpm.d/zz-docker.conf

RUN pecl install redis-5.3.7 \
  && pecl install xdebug-3.2.1 \
  && docker-php-ext-enable redis xdebug

RUN apt update && apt-get install -y --no-install-recommends libpq-dev \
  && docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql \
  && docker-php-ext-install pdo pdo_pgsql pgsql

WORKDIR /sabredav
RUN composer require sabre/dav ~4.4.0

COPY index.php index.php
