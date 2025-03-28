import zipfile, os, tempfile
from fastapi import FastAPI, File, UploadFile
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI()

# Update these with your actual MySQL config
DB_USER = "devuser"
DB_PASS = "devpass"
DB_NAME = "mydatabase"
DB_HOST = "localhost"
DB_PORT = "3306"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

@app.post("/upload_zip/")
async def upload_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return {"error": "File must be a .zip archive"}

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, file.filename)
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        for entry in os.listdir(tmpdir):
            if entry.endswith(".csv"):
                table_name = entry.replace(".csv", "")
                csv_path = os.path.join(tmpdir, entry)
                print(f"Inserting {csv_path} into table {table_name}...")
                try:
                    df = pd.read_csv(csv_path)
                    df.to_sql(table_name, con=engine, if_exists="append", index=False)
                except Exception as e:
                    print(f"Failed to insert {table_name}: {e}")
                    return {"error": str(e)}

    return {"message": "All CSVs imported successfully."}
