# syntax=docker/dockerfile:1

FROM python:3.13-slim-bookworm

ENV POETRY_VERSION=2.4.1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry install --no-interaction --no-ansi --no-root --without dev

# Copy Python code to the Docker image
COPY pygeosimplify /code/pygeosimplify/
