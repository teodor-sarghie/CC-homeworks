"""
WSGI config for google_services project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import threading
from django.core.wsgi import get_wsgi_application
from google_services.celery_runner import (
    start_celery_worker,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "google_services.settings")

threading.Thread(target=start_celery_worker, daemon=True).start()


application = get_wsgi_application()
