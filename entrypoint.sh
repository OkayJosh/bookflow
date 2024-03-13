#!/usr/bin/env bash
pdm run manage.py collectstatic --noinput
pdm run manage.py migrate --noinput
pdm run gunicorn -b :8000 Bookflow.wsgi