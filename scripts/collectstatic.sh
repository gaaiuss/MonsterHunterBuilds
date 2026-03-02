#!/bin/sh
echo 'Running collectstatic.sh'
python manage.py collectstatic --noinput
