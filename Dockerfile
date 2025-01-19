FROM prestashop/prestashop:1.7.8.8

RUN a2enmod ssl
RUN a2ensite default-ssl.conf

RUN apt-get update && apt-get install -y \
    libmemcached-dev \
    zlib1g-dev \
    && pecl install memcached \
    && docker-php-ext-enable memcached

COPY deploy/certs/yarn.local.crt /etc/ssl/certs/
RUN chmod 755 -R /etc/ssl/certs/
COPY deploy/certs/yarn.local.key /etc/ssl/private/
RUN chmod 755 -R /etc/ssl/private/

COPY deploy/apache/000-default.conf /etc/apache2/sites-available
COPY deploy/apache/default-ssl.conf /etc/apache2/sites-available
RUN chmod 755 -R /etc/apache2/sites-available

COPY /prestashop /var/www/html

RUN rm -rf /var/www/html/var/cache
RUN rm -rf /var/www/html/install
RUN rm -rf install/

# RUN rm -rf /var/www/html/app/config/parameters.php
# RUN mv /var/www/html/app/config/parameters.php.alt /var/www/html/app/config/parameters.php

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

EXPOSE 80
EXPOSE 443