#!/bin/sh

set -e

mkdir -p /socket
chown -R www-data:www-data /socket

exec /code/wait-for-it.sh db:5432 -- uwsgi --ini /code/config/uwsgi/uwsgi.ini