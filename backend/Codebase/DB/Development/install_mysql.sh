#!/bin/bash
set -e

# === Configurable Variables ===
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source "${SCRIPT_DIR%%/backend*}/backend/.env"

# === Install Prerequisites ===
echo "Installing prerequisites..."
sudo apt-get update
sudo apt-get install -y wget gnupg lsb-release ufw

# === Add MySQL APT Repo (only if missing) ===
if ! dpkg -s mysql-apt-config >/dev/null 2>&1; then
  echo "Adding official MySQL APT repository..."
  wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb
  sudo DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config_0.8.29-1_all.deb
  sudo apt-get update
fi

# === Install MySQL Server ===
echo "Installing MySQL server..."
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server

# === Enable LAN access ===
echo "Configuring MySQL to allow LAN connections..."
MYSQL_CNF="/etc/mysql/mysql.conf.d/mysqld.cnf"
sudo sed -i "s/^bind-address.*/bind-address = 0.0.0.0/" "$MYSQL_CNF"

# === Start and Enable MySQL Service ===
echo "Starting MySQL service..."
sudo systemctl restart mysql
sudo systemctl enable mysql

# === Test root login ===
echo "Testing MySQL root login..."
if ! mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e ";" 2>/dev/null; then
  echo "Root login failed — attempting forced root password reset..."

  echo "Stopping MySQL service..."
  sudo systemctl stop mysql

  echo "Starting MySQL in --skip-grant-tables mode..."
  sudo mysqld_safe --skip-grant-tables --skip-networking &
  sleep 5

  echo "Resetting root password and plugin..."
  mysql -u root <<EOF
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${MYSQL_ROOT_PASSWORD}';
FLUSH PRIVILEGES;
EOF

  echo "Killing mysqld_safe..."
  sudo killall mysqld || true
  sleep 3

  echo "Restarting MySQL service..."
  sudo systemctl start mysql
fi

# === Secure Installation ===
echo "Securing MySQL installation..."
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<EOF
DELETE FROM mysql.user WHERE User='';
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
EOF

# === Create New Database and User ===
echo "Creating new database and user (local + LAN access)..."
mysql -u root -p"${MYSQL_ROOT_PASSWORD}" <<EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';
FLUSH PRIVILEGES;
EOF

# === Run SQL Schema ===
if [ -f "${SQL_SCHEMA_FILE}" ]; then
    echo "Deploying schema from ${SQL_SCHEMA_FILE}..."
    mysql -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}" "${MYSQL_DATABASE}" < "${SQL_SCHEMA_FILE}"
else
    echo "No schema file found at ${SQL_SCHEMA_FILE}. Skipping schema deployment."
fi

# === Allow MySQL Port on Firewall ===
echo "Allowing MySQL port 3306 on firewall..."
sudo ufw allow 3306/tcp

echo "MySQL installation and LAN access setup complete."
