from sqlalchemy import text
from datetime import datetime

from .drop_all_tables import drop_all_tables
from ..Pathing.get_schema_path import get_schema_path
from ..config import get_engine

SCRIPT_DIR = get_schema_path()

def create_database(google_id: int) -> str:
    timeinstance = datetime.now().strftime("%Y-%m-%d_%H:%M")
    db_name = f"{google_id}-{timeinstance}"
    print(f"Creating database: {db_name}")

    admin_engine = get_engine("mysql")

    # Step 1: Create the database
    with admin_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE `{db_name}`"))
        print(f"Created database `{db_name}`")

    # Step 2: Read schema
    with open(SCRIPT_DIR, "r") as f:
        schema_sql = f.read()

    user_engine = get_engine(db_name)

    # Step 3: Drop all tables (optional safety)
    drop_all_tables(user_engine)

    # Step 4: Apply schema
    with user_engine.connect() as conn:
        for i, stmt in enumerate(schema_sql.split(";")):
            stmt = stmt.strip()
            if stmt:
                try:
                    conn.execute(text(stmt))
                    print(f"Executed statement [{i}]: {stmt[:60]}...")
                except Exception as e:
                    print(f"Error executing statement [{i}]: {stmt[:60]}...")
                    print(f"   └── {e}")

    # Step 5: Confirm created tables
    with user_engine.connect() as conn:
        tables = conn.execute(text("SHOW TABLES")).fetchall()
        print(f"Tables in `{db_name}`:")
        for table in tables:
            print(f"   └── {table[0]}")

    return timeinstance
