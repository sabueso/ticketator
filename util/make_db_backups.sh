#!/usr/bin/env bash
echo "REMEBER run as postgres user..."
pg_dump -d tickets_db --inserts > make_db_backups.sql
