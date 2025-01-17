FROM prestashop/prestashop:1.7.8.8

COPY . /var/www/html

RUN mv /var/www/html/config/parameters.php.alt /var/www/html/config/parameters.php

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

EXPOSE 80