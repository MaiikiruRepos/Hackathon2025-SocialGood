#!/bin/bash
set -e

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "${SCRIPT_DIR%%/backend*}/backend/.env"

# === List all tables ===
echo "Listing all tables in database: $MYSQL_DATABASE"
mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "SHOW TABLES;" "$MYSQL_DATABASE"
