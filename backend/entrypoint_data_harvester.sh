#!/bin/sh
poetry run alembic -c shared/alembic.ini upgrade heads
poetry run python3 -m harvesting.data_harvesters.data_harversters