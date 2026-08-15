#!/bin/sh
set -eu

python manage.py migrate --noinput

# No ambiente público, cria/atualiza apenas contas e dados fictícios.
# O comando é idempotente e só roda quando DEMO_MODE está ativado.
case "${DEMO_MODE:-false}" in
  [Tt][Rr][Uu][Ee])
    python manage.py seed_demo
    ;;
esac

python manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers "${GUNICORN_WORKERS:-3}" --timeout "${GUNICORN_TIMEOUT:-60}" --access-logfile - --error-logfile -
