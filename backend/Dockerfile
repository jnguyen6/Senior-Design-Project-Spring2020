FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
# ENV DATABASE_URL "postgresql://admin:Password1!@localhost/backend"
ENV FLASK_DEBUG True

RUN mkdir /app
WORKDIR /app

COPY Pip* /app/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy --ignore-pipfile

ADD . /app
