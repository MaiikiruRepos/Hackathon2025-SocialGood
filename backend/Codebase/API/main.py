import zipfile
import tempfile
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from sqlalchemy import create_engine
from dotenv import load_dotenv

import os

# === Load .env from project root ===
print("Loaded DB name:", os.getenv("MYSQL_DATABASE"))
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_USER_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")

# === Create SQLAlchemy engine ===
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

app = FastAPI()

@app.post("/upload_zip/")
async def upload_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return {"error": "File must be a .zip archive"}

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path:str = os.path.join(tmpdir, file.filename)
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        for entry in os.listdir(tmpdir):
            if entry.endswith(".csv"):
                table_name:str = entry.replace(".csv", "")
                csv_path:str = os.path.join(tmpdir, entry)
                print(f"Inserting {csv_path} into table {table_name}...")
                try:
                    df:pd.DataFrame = pd.read_csv(csv_path)
                    df.to_sql(table_name, con=engine, if_exists="append", index=False)
                except Exception as e:
                    print(f"Failed to insert {table_name}: {e}")
                    return {"error": str(e)}

    return {"message": "All CSVs imported successfully."}

@app.get("/plantwater/")
def plant_water() -> None:
    pass

@app.get("/plantcarbon")
def plant_carbon() -> None:
    pass

@app.get("Dosomething")
def do_something() -> None:
    pass