from fastapi import APIRouter, UploadFile, File, Form
import tempfile, os, zipfile
import pandas as pd
from ..config import get_engine
from ..Tools.create_database import create_database
from ..Tools.load_enviromental_data import load_environmental_data  # <-- Import it

router = APIRouter()

@router.post("/upload_zip/")
async def upload_zip(
    file: UploadFile = File(...),
    googleID: str = Form(...)
):
    if not file.filename.endswith(".zip"):
        return {"error": "File must be a .zip archive"}

    # 1. Create new database for this googleID
    timeinstance = create_database(googleID)
    db_name = f"{googleID}-{timeinstance}"
    engine = get_engine(db_name)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save the uploaded ZIP file
        zip_path = os.path.join(tmpdir, file.filename)
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        # Extract the ZIP file contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        # 2. Loop through CSV files and insert them
        for entry in os.listdir(tmpdir):
            print(f"Found file in tmpdir: {entry}")

            if entry.endswith(".csv"):
                table_name = entry.replace(".csv", "")
                csv_path = os.path.join(tmpdir, entry)
                print(f"Processing CSV: {csv_path} → table {table_name}")

                try:
                    df = pd.read_csv(csv_path)
                    print(f"Read CSV with {len(df)} rows and columns: {df.columns.tolist()}")

                    df.to_sql(table_name, con=engine, if_exists="append", index=False)
                    # print(f"Inserted {len(df)} rows into {table_name}")

                except Exception as e:
                    print(f"Failed to insert {table_name}: {e}")
                    return {"error": str(e)}

    # 3. Load static environmental data into EnvTable
    try:
        load_environmental_data(db_name)
        # print(f"Loaded environmental data into {db_name}")
    except Exception as e:
        print(f"Failed to load environmental data: {e}")
        return {"error": f"Could not load EnvTable: {str(e)}"}

    return {
        "message": "All CSVs imported successfully, EnvTable loaded.",
        "timeinstance": timeinstance,
        "db_name": db_name
    }
