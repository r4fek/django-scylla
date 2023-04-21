FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y postgresql-client

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python

COPY . /app
WORKDIR /app
RUN poetry install
