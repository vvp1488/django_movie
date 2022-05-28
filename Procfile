web: gunicorn django_movies.wsgi
worker: celery -A django_movies worker -l info
worker: celery worker django_movies