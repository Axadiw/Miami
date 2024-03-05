#!/bin/sh
poetry run alembic -c shared/alembic.ini upgrade heads
sleep 3600
#poetry run waitress-serve --host 0.0.0.0 --port 5000 --call api.app:create_app