FROM python:3.13-alpine

# Python
ENV PYTHONFAULTHANDLER=1 \
PYTHONUNBUFFERED=1 \
PYTHONHASHSEED=random \
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=100

# Poetry
ENV POETRY_NO_INTERACTION=1 \
POETRY_VIRTUALENVS_CREATE=false \
POETRY_CACHE_DIR='/var/cache/pypoetry' \
POETRY_HOME='/opt/poetry' \
POETRY_VERSION=2.1.2 \
PATH="/opt/poetry/bin:$PATH"

RUN apk update \
    && apk add --no-cache \
        curl

# Install Poetry
RUN curl -SL https://install.python-poetry.org | python3 -

# Configure Poetry to not create virtualenvs inside container
RUN poetry config virtualenvs.create false


COPY pyproject.toml poetry.lock* ./

# Set working directory
WORKDIR /app

# Install project dependencies
RUN poetry install --no-interaction --no-ansi --no-root

COPY ./app .

RUN curl -X POST http://backend:7013/init


