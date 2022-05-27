release: python3 manage.py makemigrations
release: python3 manage.py migrate
web: gunicorn django_movies.wsgi
worker: celery -A django_movies worker --beat