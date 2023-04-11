#!/bin/sh

set -e

echo "Start project"

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

python manage.py migrate --noinput
python sqlite_to_postgres/load_data.py

gunicorn config.wsgi:application --bind 0.0.0.0:8000

