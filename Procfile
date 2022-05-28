web: gunicorn django_movies.wsgi
worker: python3 manage.py celery worker --logleverl=info
celery_beat: python3 manage.py celery beat --loglevel=info