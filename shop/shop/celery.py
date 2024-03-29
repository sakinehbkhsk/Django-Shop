from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")
app = Celery("shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.enable_utc = False
app.autodiscover_tasks()

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    "send-ad-mail-every-week": {
        "task": "products.tasks.send_order_status_email",
        "schedule": crontab(day_of_week="6", hour="16", minute="0"),
    }
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


# celery -A shop worker -l info -P solo
# celery -A shop worker -l info -P solo --logfile=celery.log
# celery -A shop beat -l info --logfile=celery.beat.log
# celery -A shop beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
