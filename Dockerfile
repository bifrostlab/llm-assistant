FROM python:3.12-slim

WORKDIR /usr/app

RUN pip install poetry

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install --without dev --no-root --no-directory

COPY src ./src
RUN poetry install --without dev

CMD ["poetry", "run", "python", "-m", "src.discord_bot.bot"]
