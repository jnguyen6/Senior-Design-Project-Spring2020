FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
# ENV DATABASE_URL "postgresql://admin:Password1!@localhost/backend"
ENV FLASK_DEBUG True

RUN mkdir /app
WORKDIR /app

COPY Pip* /app/

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pip install supervisor && \
    pipenv install

RUN mkdir -p /var/log/supervisor && mkdir -p /etc/supervisor/conf.d
ADD supervisor.conf /etc/supervisor.conf

EXPOSE 5000

ADD . /app

CMD ["supervisord", "-c", "/etc/supervisor.conf"]
