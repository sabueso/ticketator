#!/usr/bin/env sh

set -u

false
while [ ! $? -eq 0 ]
do
    sleep 2
    nc -z "${DB_HOST}" "${DB_PORT}"
done
sleep 2

set -e

./ticketatorapp/manage.py migrate --noinput
./ticketatorapp/manage.py collectstatic --noinput
./ticketatorapp/manage.py loaddata ticketatorapp/fixtures/*.json
./ticketatorapp/manage.py runserver "0.0.0.0:${TICKETATOR_PORT}"
