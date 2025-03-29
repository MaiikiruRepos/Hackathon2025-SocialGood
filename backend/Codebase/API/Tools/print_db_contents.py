# backend/Codebase/DB/print_user_database_contents.py

from sqlalchemy import text, inspect
from ..config import get_engine

def print_db_contents(db_name):
    print(f"Connecting to database: {db_name}")
    engine = get_engine(db_name)

    with engine.connect() as conn:
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if not tables:
            print("No tables found in the database.")
            return

        for table in tables:
            print(f"\nTable: {table}")
            try:
                result = conn.execute(text(f"SELECT * FROM `{table}` LIMIT 100;"))
                rows = result.fetchall()
                columns = result.keys()

                print(" | ".join(columns))
                print("-" * 60)

                for row in rows:
                    print(" | ".join(str(val) for val in row))

            except Exception as e:
                print(f"Error reading table {table}: {e}")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python print_user_database_contents.py <db_name>")
    else:
        print_db_contents(sys.argv[1])
