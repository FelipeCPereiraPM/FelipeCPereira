#!/usr/bin/env bash
set -euo pipefail

python manage.py makemigrations crm --noinput || true
python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "${DJANGO_SUPERUSER_USERNAME:-}" != "" ]; then
  python manage.py createsuperuser --noinput || true
fi

exec python manage.py runserver 0.0.0.0:8000