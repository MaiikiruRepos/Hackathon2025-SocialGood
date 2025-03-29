from pathlib import Path


def get_schema_path() -> Path:
    # Get the root of the project (backend/)
    root_dir = Path(__file__).resolve().parent.parent.parent.parent
    schema_path = root_dir / "Codebase"/ "DB" / "schema.sql"

    return str(schema_path)
