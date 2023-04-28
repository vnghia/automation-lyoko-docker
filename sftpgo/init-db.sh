#!/usr/bin/env bash
set -euo pipefail

psql -c "create user \"sftpgo\" with encrypted password '{{ sftpgo_dataprovider_password }}';"
psql -c "create database \"sftpgo\";"
psql -c "alter database \"sftpgo\" owner to \"sftpgo\";"
