#!/bin/sh

# exit from script immediately if command fails 
# (i.e. returns a non-zero status)
set -e

# migrate the database
python manage.py migrate

# collect static files
python manage.py collectstatic --noinput

# execute the command passed as arguments to script
# e.g. CMD instruction of Dockerfile
exec "$@"
