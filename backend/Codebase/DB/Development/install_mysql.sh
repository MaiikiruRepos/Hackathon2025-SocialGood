#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# === Configurable Variables ===
MYSQL_ROOT_PASSWORD="rootpass"
MYSQL_USER="devuser"
MYSQL_USER_PASSWORD="devpass"
MYSQL_DATABASE="mydatabase"
SQL_SCHEMA_FILE="./schema.sql"

# === Install MySQL Server ===
echo "Updating package list and installing MySQL server..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

# === Start MySQL Service ===
echo "Starting MySQL service..."
sudo systemctl start mysql
sudo systemctl enable mysql

# === Secure Installation ===
echo "Securing MySQL installation..."
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';"
sudo mysql -e "DELETE FROM mysql.user WHERE User='';"
sudo mysql -e "DROP DATABASE IF EXISTS test;"
sudo mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
sudo mysql -e "FLUSH PRIVILEGES;"

# === Create New Database and User ===
echo "Creating new database and user..."
sudo mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};"
sudo mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_USER_PASSWORD}';"
sudo mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';"
sudo mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES;"

# === Run SQL Schema ===
if [ -f "${SQL_SCHEMA_FILE}" ]; then
    echo "Deploying schema from ${SQL_SCHEMA_FILE}..."
    mysql -u "${MYSQL_USER}" -p"${MYSQL_USER_PASSWORD}" "${MYSQL_DATABASE}" < "${SQL_SCHEMA_FILE}"
else
    echo "No schema file found at ${SQL_SCHEMA_FILE}. Skipping schema deployment."
fi

echo "✅ MySQL installation and setup complete."
