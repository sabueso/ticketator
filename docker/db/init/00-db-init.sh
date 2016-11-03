#!/usr/bin/env bash

set -e
set -u

echo "Creating \"${DB_NAME}\" database..."

gosu postgres psql -c "CREATE USER ${DB_USER} CREATEDB NOSUPERUSER NOCREATEROLE INHERIT LOGIN UNENCRYPTED PASSWORD '"${DB_PASS}"';"
gosu postgres createdb --owner ${DB_USER} \
                       --template template0 \
                       --encoding=UTF8 \
                       --lc-ctype=en_US.UTF-8 \
                       --lc-collate=en_US.UTF-8 \
                       ${DB_NAME}

if [ $(find /docker-entrypoint-initdb.d/ -maxdepth 0 -type d -empty 2>/dev/null) ]
then
    echo "Restoring database dump..."
    gosu postgres pg_restore -n public \
                             --dbname=${DB_NAME} \
                             --username=${DB_USER} \
                             /docker-entrypoint-initdb.d/*-db.pgdump
    echo "Database dump restored"
fi

echo "Database \"${DB_NAME}\" created"
