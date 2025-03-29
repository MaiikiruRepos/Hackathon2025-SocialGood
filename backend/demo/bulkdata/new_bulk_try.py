import os
import re
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

# For "SELECT COUNT(*)" checks
from sqlalchemy import text

# Existing pipeline imports:
from backend.Codebase.API.Tools.Results.compute_results import compute_results
from backend.Codebase.API.Tools.create_database import create_database
from backend.Codebase.API.Tools.drop_user_databases import drop_user_databases
from backend.Codebase.API.Tools.load_enviromental_data import load_environmental_data
from backend.Codebase.API.Tools.verify_csv_matches_table_schema import verify_csv_matches_table_schema
from backend.Codebase.API.config import get_engine

from backend.demo.bulkdata.generate_all_themes import run_all_themes
from backend.demo.heatmap.generate_world_heatmap import generate_world_heatmaps_for_year
from backend.demo.visualize.generate_score_charts import main as generate_charts_main

# ------------------------------------------------------------------
# 1) Constants & “bulk data” helper
# ------------------------------------------------------------------

CSV_ROOT = "bulkdata/all_themes_output"

PRIORITY_ORDER = [
    "Sku.csv",
    "Plant.csv",
    "Item.csv",
    "ProcessDefinition.csv",
    "Process.csv",
    "ItemProcess.csv",
    "PlantSKUQuantity.csv",
    "SkuProcess.csv"
]

THEME_BASE_TIMES = {
    "pcb": datetime(2023, 1, 1, 0, 0),
    "trucking": datetime(2023, 2, 1, 0, 0),
    "insurance": datetime(2023, 3, 1, 0, 0)
}

# Example: generating x “bulk users” and adding them to the newly created DB
def insert_bulk_users(engine, user_count=5):
    """
    Inserts fake 'Plant' records with a unique plant_id for each.
    """
    print(f"[BULK] Inserting {user_count} new fake users...")

    countries = ["US", "CA", "CN", "IN", "GB"]

    with engine.begin() as conn:
        # Get the current max plant_id
        max_query = text("SELECT IFNULL(MAX(plant_id), 0) FROM Plant")
        current_max = conn.execute(max_query).scalar()

        for i in range(user_count):
            user_id = f"bulkUser_{i+1}"
            country_code = random.choice(countries)

            # Generate a new unique plant_id
            next_id = current_max + 1
            current_max = next_id  # increment for next loop

            # Insert record
            insert_sql = text("""
                INSERT INTO Plant (plant_id, country_code)
                VALUES (:pid, :cc)
            """)
            conn.execute(insert_sql, {"pid": next_id, "cc": country_code})
            print(f"[BULK] Inserted Plant {next_id} for {country_code}")

    print("[BULK] Bulk user insertion complete.\n")



# ------------------------------------------------------------------
# 2) DB loading function (creates DB, loads CSV, inserts bulk data, etc.)
# ------------------------------------------------------------------

def upload_theme_folder_to_db(folder_path, google_id, timeinstance, theme, timestamp, include_bulk=False, bulk_user_count=5):
    """
    Creates a new DB for the (theme + timestamp), loads environment data,
    loads CSVs in priority order, optionally inserts bulk user data,
    and then runs compute_results.
    """
    db_name = f"{google_id}-{timeinstance}"
    print(f"[DB] Creating: {db_name}")

    # Create the database
    create_database(google_id, timeinstance=timeinstance)

    # Get an engine for the newly created database
    engine = get_engine(db_name)

    # Check DB connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"[DB CHECK] Successfully connected to {engine.url}\n")
    except Exception as e:
        print(f"[DB ERROR] Could not connect to {db_name}: {e}")
        return

    # Load environmental data (assuming it sets up some baseline tables)
    print(f"[ENV] Loading EnvTable for {db_name}...")
    load_environmental_data(db_name)

    # Import CSVs in the correct order
    print(f"[CSV] Importing from {folder_path}")
    files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".csv")],
        key=lambda x: PRIORITY_ORDER.index(x) if x in PRIORITY_ORDER else 999
    )

    for file in files:
        table = file.replace(".csv", "")
        csv_path = os.path.join(folder_path, file)
        try:
            # Read CSV
            df = pd.read_csv(csv_path)

            # Validate columns match DB schema (existing table) if needed
            verify_csv_matches_table_schema(engine, table, df)

            # Load data into the table (append if_exists)
            df.to_sql(table, engine, if_exists="append", index=False)
            print(f"Loaded {file} into {table}")

            # Check row counts
            with engine.connect() as conn:
                row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"[DB CHECK] Table '{table}' now has {row_count} rows.\n")

        except Exception as e:
            print(f"ERROR loading {file} into table '{table}': {e}")

    # ----------------------------------------------------------------
    # Insert "bulk user" data, now that tables exist
    # (Remove this if you truly want separate DB per user.)
    # ----------------------------------------------------------------
    if include_bulk:
        insert_bulk_users(engine, user_count=bulk_user_count)

    # Compute results for this DB
    print("[✓] Computing results...")
    try:
        compute_results(engine, theme=theme, timeinstance=timestamp)
        print("[✓] compute_results() completed.\n")
    except Exception as e:
        print(f"[ERROR] compute_results failed: {e}")

    print(f"[DONE] {db_name} loaded successfully.\n")


# ------------------------------------------------------------------
# 3) Main pipeline
# ------------------------------------------------------------------

def run_pipeline(include_bulk=False, bulk_user_count=5):
    """
    1. Drop user DBs
    2. Generate new dummy data for all themes
    3. Loop over each theme+set folder
       - Create DB, load CSV, optionally insert bulk user data, compute results
    4. Generate score charts, heatmaps
    """

    print("Purging all user databases...")
    drop_user_databases()

    print("Generating new dummy data for all themes...")
    run_all_themes(base_dir=CSV_ROOT)

    print("Uploading datasets to DBs...")

    for folder in os.listdir(CSV_ROOT):
        path = os.path.join(CSV_ROOT, folder)
        if not os.path.isdir(path):
            continue

        # Folder name typically looks like "pcb_set_1", "pcb_set_2", etc.
        match = re.match(r"(\w+)_set_(\d+)", folder)
        if not match:
            print(f"Skipping folder {folder} (no match)")
            continue

        theme, index_str = match.groups()
        index = int(index_str)

        base_time = THEME_BASE_TIMES.get(theme)
        if not base_time:
            print(f"Skipping unknown theme: {theme}")
            continue

        # Example: each set is ~7 months apart
        time_offset = relativedelta(months=(index - 1) * 7)
        timestamp = (base_time + time_offset).strftime("%Y-%m-%d_%H-%M")

        # Example google_id for the DB name
        google_id = f"{theme}_user"

        # Create the DB, load CSV, optionally insert bulk user data
        upload_theme_folder_to_db(
            folder_path=path,
            google_id=google_id,
            timeinstance=timestamp,
            theme=theme,
            timestamp=timestamp,
            include_bulk=include_bulk,
            bulk_user_count=bulk_user_count
        )

    print("Generating score charts for all databases...")
    generate_charts_main()
    print("Charts generated in 'charts_output/'")

    print("Generating world heatmaps for carbon and water...")
    generate_world_heatmaps_for_year("2023")
    generate_world_heatmaps_for_year("2024")

    print("Heatmaps generated in 'charts_output/'")


# ------------------------------------------------------------------
# 4) Entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Adjust as desired
    run_pipeline(include_bulk=True, bulk_user_count=10)
