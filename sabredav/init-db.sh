#!/usr/bin/env bash
set -euo pipefail

psql -c "create user \"sabredav\" with encrypted password 'a';"
psql -c "create database \"sabredav\";"
psql -c "alter database \"sabredav\" owner to \"sabredav\";"

mkdir -p /tmp/sabredav/
{% for name in ["addressbooks", "calendars", "locks", "principals", "propertystorage", "users"] %}
wget https://raw.githubusercontent.com/sabre-io/dav/4.4.0/examples/sql/pgsql.{{ name }}.sql -O /tmp/sabredav/pgsql.{{ name }}.sql
{% endfor %}

sed -i "s/admin/{{ sabredav_backup_client_username }}/g" /tmp/sabredav/pgsql.users.sql
sed -i "s/87fd274b7b6c01e48d7c2f965da8ddf7/{{ sabredav_backup_client_password }}/g" /tmp/sabredav/pgsql.users.sql
sed -i "s/Administrator/{{ sabredav_backup_client_username }}/g" /tmp/sabredav/pgsql.principals.sql
sed -i "s/admin@example.org/{{ sabredav_backup_client_email }}/g" /tmp/sabredav/pgsql.principals.sql
sed -i "s/admin/{{ sabredav_backup_client_username }}/g" /tmp/sabredav/pgsql.principals.sql

export PGPASSWORD="{{ sabredav_backup_client_password }}"
for f in /tmp/sabredav/pgsql.*; do psql -d sabredav -U sabredav -a -f $f; done

rm -rf /tmp/sabredav
