#!/bin/bash

celery -A google_services worker --loglevel=info
