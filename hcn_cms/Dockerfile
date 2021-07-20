FROM python:3.9.5-slim-buster

ENV PYTHONUNBUFFERED=1
ENV APP_ENV=${APP_ENV:-dev}

WORKDIR /app/hcn_cms/

RUN apt-get update -y; \
    apt-get upgrade -y; \
    apt-get install -y gcc build-essential postgresql-client libpq-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

COPY Pipfile* /app/
COPY docker/docker-entrypoint.sh /usr/bin/docker-entrypoint

RUN chmod a+x /usr/local/bin/docker-entrypoint; \
    cd /app/ && pipenv install -d --system --skip-lock

COPY .. .

EXPOSE 8000

#ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["docker-entrypoint"]
