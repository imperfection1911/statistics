#!/bin/bash
set -e
sleep 5
sed -i 's/login =/login = '"$LOGIN"'/g' /app/config.ini
sed -i 's/password =/password = '"$PASSWORD"'/g' /app/config.ini
psql -U postgres -h postgres -p 5432 -d postgres -c "create database statistics;"
# psql -U postgres -h postgres -p 5432 -d postgres -c "create user stat with password '1qaz2wsx';"
psql -U postgres -h postgres -p 5432 -d postgres -c  "grant all on database statistics to postgres;"
psql -U postgres -h postgres -p 5432 -d statistics -c "create table statistics( call_date varchar(64),method varchar(64))"
echo $FROM
echo $TO
exec python /app/statistics.py --from "$FROM" --to "$TO"