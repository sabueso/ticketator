#!/usr/bin/env bash

set -u

false
while [ ! $? -eq 0 ]
do
    sleep 2
    nc -z "${DB_HOST}" "${DB_PORT}"
done
sleep 2

set -e

./manage.py migrate --noinput
./manage.py collectstatic --noinput
./manage.py loaddata fixtures/*.json
./manage.py runserver "0.0.0.0:${TICKETATOR_PORT}"
