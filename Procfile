web: gunicorn --bind 0.0.0.0:$PORT run:app
worker-default: celery -A celery_task worker --loglevel=info 
worker-beat: celery -A celery_task beat --loglevel=info