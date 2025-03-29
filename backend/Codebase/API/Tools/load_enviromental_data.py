import csv
import os
from sqlalchemy import text
from ..config import get_engine

def load_environmental_data(database_name: str):
    engine = get_engine(database_name)
    print(f"[DEBUG] Engine created for DB: {database_name}")

    # Path to environment data CSV
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "DB", "enviromentData.csv")
    csv_path = os.path.abspath(csv_path)
    print(f"[DEBUG] Loading CSV from: {csv_path}")

    if not os.path.exists(csv_path):
        print("[ERROR] CSV file does not exist.")
        return

    with engine.begin() as conn:
        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [col.strip().replace('\ufeff', '') for col in reader.fieldnames]

            for row in reader:
                print(f"[DEBUG] Inserting row: {row}")
                try:
                    mapped_row = {
                        "country_code": row["country_code"],
                        "country_name": row["country_name"],
                        "continent": row["continent"],
                        "gas_cr": row["gas_cr"],
                        "gas_wr": row["gas_wr"],
                        "diesel_cr": row["diesel_cr"],
                        "diesel_wr": row["diesel_wr"],
                        "elec_cr": row["elec_cr"],
                        "elec_wr": row["elec_wr"],
                        "employee_cr": row["employee_cr"],
                        "employee_wr": row["employee_wr"]
                    }

                    insert_sql = text("""
                        INSERT INTO EnvTable (
                            country_code, country_name, continent,
                            gas_cr, gas_wr,
                            diesel_cr, diesel_wr,
                            elec_cr, elec_wr,
                            employee_cr, employee_wr
                        ) VALUES (
                            :country_code, :country_name, :continent,
                            :gas_cr, :gas_wr,
                            :diesel_cr, :diesel_wr,
                            :elec_cr, :elec_wr,
                            :employee_cr, :employee_wr
                        )
                    """)

                    conn.execute(insert_sql, mapped_row)
                except Exception as e:
                    print(f"[ERROR] Failed to insert row: {row}")
                    print(f"[ERROR] Exception: {e}")
