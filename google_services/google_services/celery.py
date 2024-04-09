from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_services.settings")


GOOGLE_REDIS = os.getenv("REDISGOOGLE", None)
GOOGLE_REDIS_PORT = os.getenv("REDISPORTGOOGLE", None)

if GOOGLE_REDIS is not None:
    app = Celery(
        "google_services",
        broker=f"redis://{GOOGLE_REDIS}:{GOOGLE_REDIS_PORT}/0",
        backend=f"redis://{GOOGLE_REDIS}:{GOOGLE_REDIS_PORT}/0",
    )
else:
    app = Celery("google_services")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
