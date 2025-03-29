# backend/Codebase/DB/wipe_user_databases.py

import re
from sqlalchemy import text
from backend.Codebase.API.config import get_engine

# Match anything like <anything>-YYYY-MM-DD_HH-MM
db_pattern = re.compile(r'^.+-\d{4}-\d{2}-\d{2}_\d{2}-\d{2}$')

def drop_user_databases():
    engine = get_engine("mysql")
    dropped = []

    with engine.connect() as conn:
        result = conn.execute(text("SHOW DATABASES;"))
        all_dbs = [row[0] for row in result.fetchall()]

        for db_name in all_dbs:
            if db_pattern.match(db_name):
                print(f"🗑 Dropping database: {db_name}")
                conn.execute(text(f"DROP DATABASE `{db_name}`"))
                dropped.append(db_name)

    print(f"[✓] Dropped {len(dropped)} user databases.")
    return dropped

if __name__ == "__main__":
    drop_user_databases()
