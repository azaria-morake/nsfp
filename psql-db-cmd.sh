#!/bin/bash

# Prompt for input
read -p "Enter new database name: " DB_NAME
read -p "Enter new username: " DB_USER
read -s -p "Enter password for new user: " DB_PASS
echo
read -p "Enter default timezone (e.g. UTC): " TIMEZONE

# Execute as the postgres system user
sudo -u postgres psql <<EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO '$TIMEZONE';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF
