web: gunicorn tweetme.wsgi --log-file -

release: django-admin migrate --no-input && django-admin collectstatic --no-input
