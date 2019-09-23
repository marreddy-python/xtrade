from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

import sys
sys.dont_write_bytecode=True

def make_celery(app):
    celery = Celery(app.import_name, 
    backend=app.config['CELERY_RESULT_BACKEND'], 
    broker=app.config['CELERY_BROKER_URL']

    )

    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
       

def create_db(app):

    DEBUG = False
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/flask?user=marreddy&password=BECKNF79" 

    db = SQLAlchemy(app)
       
    return db


# Checking if table exist in database or not
def check_database(db):

    engine = create_engine('postgresql://localhost/flask?user=marreddy&password=BECKNF79')

    if ('price_data'in engine.table_names()): 
        pass
    else:
        db.create_all()

