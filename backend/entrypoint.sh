#!/bin/sh
poetry run alembic upgrade heads
potery run waitress-serve --host 0.0.0.0 --port 5000 --call app:create_app