# Entorno de prueba Laravel — proyecto limpio generado en build time, sin datos
# sensibles reales. No existe imagen oficial de Laravel en Docker Hub, así que se
# construye sobre PHP + Apache instalando el framework vía Composer.
FROM php:8.2-apache

RUN apt-get update && apt-get install -y \
    git unzip libzip-dev libpng-dev libonig-dev default-mysql-client \
    && docker-php-ext-install pdo_mysql mbstring zip gd bcmath \
    && a2enmod rewrite \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

# Proyecto limpio de Laravel 12.x (sin código propio del tesista, solo el
# esqueleto oficial — sirve como objetivo de fingerprinting para el módulo recon).
RUN composer create-project --prefer-dist "laravel/laravel:^12.0" . \
    && chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache

COPY apache-laravel.conf /etc/apache2/sites-available/000-default.conf
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 80
ENTRYPOINT ["entrypoint.sh"]
CMD ["apache2-foreground"]
