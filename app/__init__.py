# -*- coding: utf-8 -*
from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

JOB_DEFAULTS = {
    'coalesce': True,
    'max_instances': 1
}

app = Flask(__name__)

scheduler = APScheduler(scheduler=BackgroundScheduler(job_defaults=JOB_DEFAULTS))
scheduler.init_app(app=app)
scheduler.start()
app.app_context().push()
