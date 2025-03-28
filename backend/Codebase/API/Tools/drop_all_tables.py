# backend/Codebase/DB/create_database.py
from sqlalchemy import text


def drop_all_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        # Get all table names
        result = conn.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE();"
        ))
        tables = [f"`{row[0]}`" for row in result.fetchall()]

        if tables:
            drop_sql = f"DROP TABLE IF EXISTS {', '.join(tables)};"
            conn.execute(text(drop_sql))

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
