FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry config virtualenvs.create false --local

RUN poetry install
