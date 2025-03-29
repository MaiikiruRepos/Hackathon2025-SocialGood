import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from backend.Codebase.API.Tools.Results.compute_results import compute_results
from backend.Codebase.API.Tools.create_database import create_database
from backend.Codebase.API.Tools.drop_user_databases import drop_user_databases
from backend.Codebase.API.Tools.load_enviromental_data import load_environmental_data
from backend.Codebase.API.Tools.verify_csv_matches_table_schema import verify_csv_matches_table_schema
from backend.Codebase.API.config import get_engine
from backend.demo.bulkdata.generate_all_themes import run_all_themes

from backend.demo.visualize.generate_score_charts import main as generate_charts_main

# Constants
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

# Timestamps spaced ~7 months apart
THEME_BASE_TIMES = {
    "pcb": datetime(2023, 1, 1, 0, 0),
    "trucking": datetime(2023, 2, 1, 0, 0),
    "insurance": datetime(2023, 3, 1, 0, 0)
}
NUM_SETS = 4

def upload_theme_folder_to_db(folder_path, db_label, google_id, timeinstance, theme, timestamp):
    db_name = f"{google_id}-{timeinstance}"
    print(f"[DB] Creating: {db_name}")

    create_database(google_id, timeinstance=timeinstance)
    engine = get_engine(db_name)

    print(f"[ENV] Loading EnvTable for {db_name}...")
    load_environmental_data(db_name)

    print(f"[CSV] Importing from {folder_path}")
    files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(".csv")],
        key=lambda x: PRIORITY_ORDER.index(x) if x in PRIORITY_ORDER else 999
    )

    for file in files:
        table = file.replace(".csv", "")
        path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(path)
            verify_csv_matches_table_schema(engine, table, df)
            df.to_sql(table, engine, if_exists="append", index=False)
            print(f"Loaded {file} into {table}")
        except Exception as e:
            print(f"ERROR loading {file}: {e}")

    print("[✓] Computing results...")
    compute_results(engine, theme=theme, timeinstance=timestamp)
    print(f"[DONE] {db_name} loaded successfully.\n")

def main():
    print("Purging all user databases...")
    drop_user_databases()

    print("Generating new dummy data for all themes...")
    run_all_themes(base_dir=CSV_ROOT)

    print("Uploading datasets to DBs...")
    for folder in os.listdir(CSV_ROOT):
        path = os.path.join(CSV_ROOT, folder)
        if not os.path.isdir(path):
            continue

        match = re.match(r"(\w+)_set_(\d+)", folder)
        if not match:
            continue

        theme, index = match.groups()
        index = int(index)
        base_time = THEME_BASE_TIMES.get(theme)
        if not base_time:
            print(f"Skipping unknown theme: {theme}")
            continue

        time_offset = relativedelta(months=(index - 1) * 7)
        timestamp = (base_time + time_offset).strftime("%Y-%m-%d_%H-%M")
        google_id = f"{theme}_user"

        upload_theme_folder_to_db(
            path,
            db_label=folder,
            google_id=google_id,
            timeinstance=timestamp,
            theme=theme,
            timestamp=timestamp
        )

    print("Generating score charts for all databases...")
    generate_charts_main()
    print("Charts generated in 'charts_output/'")

if __name__ == "__main__":
    main()
