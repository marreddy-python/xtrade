from __future__ import absolute_import, unicode_literals
from flask import Flask
from celery import Celery
from celery_config import make_celery,create_db,check_database
from datetime import timedelta
from celery.schedules import crontab


app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERYBEAT_SCHEDULE = {
        'periodic_task-every-minute': {
            'task': 'periodic_task',
            'schedule': crontab(minute=0, hour=0,day_of_week="mon,tue,wed,thu,fri")
        }}
)


celery = make_celery(app)

db = create_db(app)

from models_celery.tables import price_data,Strategy_features,Market_data_audit_log

check_database(db)

from startup import main

@celery.task(name ="periodic_task")

def send_async_email():
    
    main() 


