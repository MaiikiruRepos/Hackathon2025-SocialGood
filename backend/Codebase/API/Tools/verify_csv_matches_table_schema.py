from sqlalchemy import inspect

def verify_csv_matches_table_schema(engine, table_name, df):
    inspector = inspect(engine)
    if table_name not in inspector.get_table_names():
        raise ValueError(f"Table '{table_name}' does not exist in the database.")

    # Get expected column names from the table
    columns_info = inspector.get_columns(table_name)
    expected_columns = [col['name'] for col in columns_info]

    # Compare with CSV columns
    if set(df.columns) != set(expected_columns):
        raise ValueError(
            f"Column mismatch for table '{table_name}'.\n"
            f"Expected: {expected_columns}\n"
            f"Found in CSV: {df.columns.tolist()}"
        )