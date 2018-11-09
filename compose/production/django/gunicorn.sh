#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py collectstatic --noinput
gunicorn 0.0.0.0 -p 5000 computrabajo_bot.asgi:application
