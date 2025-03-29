import csv
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from ..config import get_engine

# Load environment variables from .env
load_dotenv()

def load_environmental_data(database_name: str):
    # Set up the SQLAlchemy engine
    # user = os.getenv("MYSQL_USER")
    # password = os.getenv("MYSQL_PASSWORD")
    # host = os.getenv("MYSQL_HOST", "localhost")
    # port = os.getenv("MYSQL_PORT", "3306")

    # db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"
    # engine = create_engine(db_url)

    engine = get_engine(database_name)

    # CSV path (relative to this script)
    csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "DB", "enviromentData.csv")

    # Read CSV and insert data
    with engine.connect() as conn:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
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

    print(f"Environmental data successfully loaded into '{database_name}'.")
