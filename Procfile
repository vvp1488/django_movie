release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn django_movies.wsgi
worker: celery -A django_movies worker --beat