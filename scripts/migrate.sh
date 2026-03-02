#!/bin/sh
echo 'Running migrate.sh'
makemigrations.sh
python manage.py migrate --noinput
