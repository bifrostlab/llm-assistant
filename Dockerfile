FROM python:3.12-slim

WORKDIR /usr/app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.7.1

RUN pip install poetry==${POETRY_VERSION}

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --without dev --no-root --no-directory && rm -rf ${POETRY_CACHE_DIR}

COPY src ./src
RUN poetry install --without dev

CMD ["poetry", "run", "python", "-m", "src.discord_bot.bot"]
