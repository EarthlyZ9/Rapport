FROM python:3.10

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  # pip:
  PIP_NO_CACHE_DIR=on \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.5.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version

# Copy project
COPY ./ /home/rapport/

# Set working directory
WORKDIR /home/rapport/

# Make django log file
RUN mkdir -p config/logs
RUN touch config/logs/rapport.log

# Install dependencies:
RUN poetry install

# Entrypoint for django app and celery workers
COPY ./entrypoint.sh /
RUN chmod 747 /entrypoint.sh

COPY ./infra/scripts/celery_entrypoint.sh /
RUN chmod 747 /celery_entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
