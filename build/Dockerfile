FROM php:7.4-apache

# Install required PHP extensions and dependencies
RUN apt-get update && apt-get install -y \
    zip \
    libzip-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libonig-dev \
    libicu-dev \
    libxml2-dev \
    libsqlite3-dev \
    libxslt1-dev \
    zlib1g-dev \
    libcurl4-openssl-dev \
    curl \
&& docker-php-ext-configure gd --with-jpeg --with-freetype \
&& docker-php-ext-install gd pdo pdo_mysql intl zip

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Install Node.js 16 and NPM
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
&& apt-get install -y nodejs

# Change ownership of /var/www/html to www-data
RUN chown -R www-data:www-data /var/www/html

