FROM python:3.11 as python-base
ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

FROM python-base as poetry-base
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as runtime
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}
ENV PATH="${PATH}:${POETRY_VENV}/bin"
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry check
RUN poetry install --no-interaction --no-cache --without dev
COPY . /app
COPY ./consts_tpl.py /app/consts_secrets.py
EXPOSE 5000
RUN poetry run alembic upgrade heads
CMD [ "poetry", "run", "waitress-serve", "--host", "0.0.0.0", "--port", "5000", "--call", "app:create_app"]