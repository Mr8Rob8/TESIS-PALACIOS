#!/bin/sh
set -e

if [ ! -f /var/www/html/.env ]; then
  cp /var/www/html/.env.example /var/www/html/.env
fi

# Compose proporciona DB_* explícitos. Las sustituciones conservan la
# configuración local cuando las claves están presentes en .env.
sed -i \
  -e "s/^DB_CONNECTION=.*/DB_CONNECTION=mysql/" \
  -e "s/^DB_HOST=.*/DB_HOST=db/" \
  -e "s/^DB_PORT=.*/DB_PORT=3306/" \
  -e "s/^DB_DATABASE=.*/DB_DATABASE=laravel/" \
  -e "s/^DB_USERNAME=.*/DB_USERNAME=laravel/" \
  -e "s/^DB_PASSWORD=.*/DB_PASSWORD=test-lv-pw/" \
  /var/www/html/.env

php artisan key:generate --force

# Espera a que la base de datos este lista antes de migrar.
for i in $(seq 1 30); do
  if php artisan migrate --force > /tmp/migrate.log 2>&1; then
    break
  fi
  sleep 2
done

exec "$@"
