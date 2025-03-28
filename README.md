# Hackathon2025-SocialGood

Assuming that you are on the root of this repo, the instructions to it all is:

## Run the FastAPI Locally:
`fastapi dev backend/Codebase/API/main.py`

## Run the database using Docker:
`docker compose up -d`

## Run the Frontend
npm run dev


----
backend ".env" file to be saved at   
/Backend/.env
and of the form 
```angular2html
MYSQL_ROOT_PASSWORD=""
MYSQL_USER=""
MYSQL_USER_PASSWORD=""
MYSQL_DATABASE=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_SCHEMA_FILE="${SCRIPT_DIR}/schema.sql"

SCHEMA_DIR=backend/DB
SQL_SCHEMA_FILE=schema.sql
```