#!/bin/bash
set -e

# === Configurable Variables ===
MYSQL_ROOT_PASSWORD="rootpass"
MYSQL_USER="devuser"
MYSQL_USER_PASSWORD="devpass"
MYSQL_DATABASE="mydatabase"
SQL_SCHEMA_FILE="./schema.sql"

# === Install Prerequisites ===
echo "Installing prerequisites..."
sudo apt-get update
sudo apt-get install -y wget gnupg lsb-release

# === Add MySQL APT Repo ===
echo "Adding official MySQL APT repository..."
wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
sudo DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config_0.8.29-1_all.deb

# Refresh package list
sudo apt-get update

# === Install MySQL Server ===
echo "Installing MySQL server..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

# === Start and Enable MySQL Service ===
echo "Starting MySQL service..."
sudo systemctl start mysql
sudo systemctl enable mysql

# === Secure Installation ===
echo "Securing MySQL installation..."
sudo mysql <<EOF
UPDATE mysql.user SET plugin = 'mysql_native_password', authentication_string = PASSWORD('${MYSQL_ROOT_PASSWORD}') WHERE User = 'root' AND Host = 'localhost';
DELETE FROM mysql.user WHERE User='';
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
EOF

# === Create New Database and User ===
echo "Creating new database and user..."
sudo mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_USER_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# === Run SQL Schema ===
if [ -f "${SQL_SCHEMA_FILE}" ]; then
    echo "Deploying schema from ${SQL_SCHEMA_FILE}..."
    mysql -u "${MYSQL_USER}" -p"${MYSQL_USER_PASSWORD}" "${MYSQL_DATABASE}" < "${SQL_SCHEMA_FILE}"
else
    echo "No schema file found at ${SQL_SCHEMA_FILE}. Skipping schema deployment."
fi

echo "MySQL installation and setup complete."
