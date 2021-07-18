#!/usr/bin/env sh

set -e

APP_DIR=/app/hcn_cms

cd $APP_DIR


if [ "$APP_ENV" != "prod" ]; then
  echo "Waiting for database..."
  echo "MySQL started"

  python manage.py migrate
  python manage.py collectstatic --no-input --clear
fi

exec "$@"
