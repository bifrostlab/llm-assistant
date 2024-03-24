FROM python:3.12 as build

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.7.1

RUN pip install poetry==${POETRY_VERSION}

COPY pyproject.toml poetry.lock README.md ./
COPY src ./src

RUN poetry install --compile --without dev
RUN poetry build && poetry run pip install /app/dist/*.whl

FROM python:3.12-slim as runtime

COPY --from=build /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

CMD ["llm-bot"]
