#!/bin/sh
poetry run alembic -c shared/alembic.ini upgrade heads
poetry run gunicorn -b :5000 -k eventlet api.app:gunicorn_create