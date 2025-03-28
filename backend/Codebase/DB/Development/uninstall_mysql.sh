#!/bin/bash
set -e

echo "Stopping MySQL service..."
sudo systemctl stop mysql || true

echo "Removing MySQL packages..."
sudo apt-get remove --purge -y mysql-server mysql-client mysql-common mysql-community-server mysql-community-client

echo "Cleaning up residual config files..."
sudo rm -rf /etc/mysql /var/lib/mysql
sudo rm -rf /var/log/mysql /var/log/mysql.*

echo "Auto-removing dependencies and cleaning cache..."
sudo apt-get autoremove -y
sudo apt-get autoclean

echo "MySQL has been completely removed from this machine."
