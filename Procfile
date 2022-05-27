release: python manage.py migrate
web: gunicorn django_movies.wsgi
worker: celery -A FakeDataGenerator worker --beat