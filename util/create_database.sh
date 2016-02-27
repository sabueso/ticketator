createdb tickets_db
createuser ticket_user_db

#Needed privileges
echo 'REVOKE CONNECT ON DATABASE tickets_db FROM PUBLIC' | psql
echo 'GRANT CONNECT ON DATABASE tickets_db TO ticket_user_db' |psql
echo 'ALTER USER ticket_user_db WITH PASSWORD 'ticket4everyone' |psql

