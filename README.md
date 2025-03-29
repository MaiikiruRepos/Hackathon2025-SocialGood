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



(venv) root@Hackathon:~/Hackathon2025-SocialGood/backend/Codebase/API# PYTHONPATH=. fastapi dev main.py




----
docker notes

docker compose up



docker compose up -d
(runs in background)


docker container list
(lists docker instances, pay attenton to name)

docker container inspect replaceWITHNAME
(get IPaddress from here)






(to remove)
docker compose down

docker volume list
(get the name)


docker volume remove replaceWITHNAME