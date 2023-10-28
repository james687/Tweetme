#!/bin/sh
python manage.py migrate && python manage.py collectstatic
exec gunicorn tweetme.wsgi:application --bind 0.0.0.0:8080
