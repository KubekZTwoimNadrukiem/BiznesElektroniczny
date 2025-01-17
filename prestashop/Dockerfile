FROM prestashop/prestashop:1.7.8.8

COPY . /var/www/html

RUN rm -rf /var/www/html/app/config/parameters.php
RUN rm -rf /var/www/html/var/cache
RUN rm -rf /var/www/html/install
RUN rm -rf install/

RUN mv /var/www/html/app/config/parameters.php.alt /var/www/html/app/config/parameters.php

RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

EXPOSE 80