# `python-base` sets up all our shared environment variables
FROM python:3.13-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.3.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# -------------------------------------------------
# Builder stage
# -------------------------------------------------
FROM python-base as builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        git

RUN curl -sSL https://install.python-poetry.org | python3 -

# This requires a local copy of files, for now until CI/CD is implemented its
# commented out to allow cloning from git directly.
# WORKDIR $PYSETUP_PATH


# COPY poetry.lock pyproject.toml ./ 

# clone application source
WORKDIR /app
RUN git clone https://github.com/lukasb27/fermentation-station-agent.git .

RUN --mount=type=cache,target=/root/.cache \
    poetry install 

# # clone application source
# WORKDIR /app
# RUN git clone https://github.com/lukasb27/fermentation-station-agent.git .


# -------------------------------------------------
# Development image
# -------------------------------------------------
FROM python-base as development
ENV FASTAPI_ENV=development

WORKDIR $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install

WORKDIR /app
COPY --from=builder-base /app /app

EXPOSE 8000
CMD ["uvicorn", "--reload", "main:app"]


# -------------------------------------------------
# Production image
# -------------------------------------------------
FROM python-base as production
ENV FASTAPI_ENV=production

# COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY --from=builder-base /app /app

WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
