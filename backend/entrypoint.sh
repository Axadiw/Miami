#!/bin/sh
poetry run alembic upgrade heads
poetry run waitress-serve --host 0.0.0.0 --port 5000 --call app:create_app