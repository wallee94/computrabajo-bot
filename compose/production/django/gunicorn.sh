#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset

/usr/local/bin/gunicorn computrabajo_bot.wsgi -b 0.0.0.0:5000 --chdir=/app
