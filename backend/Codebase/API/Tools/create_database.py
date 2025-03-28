# backend/Codebase/DB/create_database.py

from sqlalchemy import create_engine, text
from datetime import datetime
import os

from backend.Codebase.API.config import get_engine

# === Get schema file path ===
SCRIPT_DIR = os.getenv("SCHEMA_DIR", "backend/DB")
SQL_SCHEMA_FILE = os.getenv("SQL_SCHEMA_FILE", "../../DB/schema.sql")
SCHEMA_PATH = os.path.join(SCRIPT_DIR, SQL_SCHEMA_FILE)

def create_database(google_id: int) -> str:
    timeinstance = datetime.now().strftime("%Y-%m-%d_%H:%M")
    db_name = f"{google_id}-{timeinstance}"

    # Connect to MySQL server (no specific DB)
    admin_engine = get_engine("mysql")

    # Create the new database
    with admin_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE `{db_name}`"))

    # Read schema SQL
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    # Connect to the new database and run schema
    user_engine = get_engine(db_name)
    with user_engine.connect() as conn:
        for stmt in schema_sql.split(";"):
            if stmt.strip():
                conn.execute(text(stmt.strip()))

    return timeinstance
