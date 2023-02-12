from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = 'America/Argentina/Buenos_Aires'
app.autodiscover_tasks()
# app.conf.beat_schedule = {
#     'groot-every-morning-check_profile_expiration_date': {
#         'task': 'accounts.tasks.check_profile_expiration_date',
#         'schedule': crontab(hour='8', minute='15'),
#         'args': (),
#     },
#     'groot-every-morning-handle_accounts_not_completed': {
#         'task': 'accounts.tasks.handle_accounts_not_completed',
#         'schedule': crontab(hour='8', minute='15'),
#         'args': (),
#     },
# }


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s('Hola Soy Groot cada 10 seg'), name='add every 10')
    # sender.add_periodic_task(30.0, test.s('Hola Invera cada 30 seg'), expires=10)
    sender.add_periodic_task(
        crontab(hour=9, minute=30, day_of_week=4),
        test.s('Feliz Jueves!'),
    )
    

@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    z = x + y
    print(z)


@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
