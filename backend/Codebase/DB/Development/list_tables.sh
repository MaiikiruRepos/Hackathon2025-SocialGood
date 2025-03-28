#!/bin/bash
set -e

# === Configurable Variables ===
MYSQL_USER="devuser"
MYSQL_PASSWORD="devpass"
MYSQL_DATABASE="mydatabase"

# === List all tables ===
echo "Listing all tables in database: $MYSQL_DATABASE"
mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SHOW TABLES;" "$MYSQL_DATABASE"
