import csv
import os
from sqlalchemy import text
from ..config import get_engine  # <-- Use your shared config function

def load_environmental_data(database_name: str):
    engine = get_engine(database_name)  # <-- Get engine using shared method
    print(f"[DEBUG] Engine created for DB: {database_name}")

    # Corrected path to match your actual CSV
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "DB", "enviromentData.csv")
    csv_path = os.path.abspath(csv_path)
    print(f"[DEBUG] Loading CSV from: {csv_path}")

    if not os.path.exists(csv_path):
        print("[ERROR] CSV file does not exist.")
        return

    with engine.begin() as conn:  # automatically commits at end
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [col.strip().replace('\ufeff', '') for col in reader.fieldnames]

            for row in reader:
                print(f"[DEBUG] Inserting row: {row}")
                try:
                    insert_sql = text("""
                        INSERT INTO EnvTable (
                            countryCode, countryName, continent,
                            gasCarbonLbPerGal, gasWaterGalPerGal,
                            dieselCarbonLbPerGal, dieselWaterLbPerGal,
                            elecCarbonLbPerKwh, elecWaterGalPerKwh,
                            employeeCarbonLbPer, employeeWaterGalPer
                        ) VALUES (
                            :countryCode, :countryName, :continent,
                            :gasCarbonLbPerGal, :gasWaterGalPerGal,
                            :dieselCarbonLbPerGal, :dieselWaterLbPerGal,
                            :elecCarbonLbPerKwh, :elecWaterGalPerKwh,
                            :employeeCarbonLbPer, :employeeWaterGalPer
                        )
                    """)
                    conn.execute(insert_sql, row)
                except Exception as e:
                    print(f"[ERROR] Failed to insert row: {row}")
                    print(f"[ERROR] Exception: {e}")
