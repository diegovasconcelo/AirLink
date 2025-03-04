#!/bin/sh

# if any of the commands fails, the entire script fails.
set -o errexit
# exits if any variable is not set.
set -o nounset

python manage.py migrate
python manage.py collectstatic --noinput

python -m gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker -b=0.0.0.0:8000