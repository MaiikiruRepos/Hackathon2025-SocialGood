#!/bin/sh
docker compose down
docker volume remove hackathon2025-socialgood_db_data
docker compose up -d