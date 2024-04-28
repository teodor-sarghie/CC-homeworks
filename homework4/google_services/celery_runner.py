import subprocess


def start_celery_worker():
    command = ["celery", "-A", "google_services", "worker", "--loglevel=info"]
    subprocess.Popen(command)
