# -------------------------------------------------
# Base image
# -------------------------------------------------
FROM python:3.13-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.3.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYSETUP_PATH="/opt/pysetup" \
    POETRY_NO_INTERACTION=1 \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# -------------------------------------------------
# Builder stage
# -------------------------------------------------
FROM python-base as builder-base

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    git \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root

# RUN poetry config virtualenvs.create false \
    # && poetry install --no-root

# -------------------------------------------------
# Test image
# -------------------------------------------------
FROM python-base as test

# Copy the venv and poetry from builder
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME

# Install the 'test' group specifically
WORKDIR $PYSETUP_PATH
RUN poetry install --with integ-test --no-root

# Copy your application and your features folder
WORKDIR /app
COPY ./integration_tests /app/integration_tests
WORKDIR /app/integration_tests/
# Default command for the test image
CMD ["behave"]

# -------------------------------------------------
# Development image
# -------------------------------------------------
FROM python-base as development
ENV FASTAPI_ENV=development

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
RUN poetry install

WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "fermentation_station.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


# -------------------------------------------------
# Production image
# -------------------------------------------------
FROM python-base as production
ENV FASTAPI_ENV=production

ENV FASTAPI_ENV=production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./fermentation_station /app/fermentation_station
WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "fermentation_station.main:app", "--host", "0.0.0.0", "--port", "8000"]
