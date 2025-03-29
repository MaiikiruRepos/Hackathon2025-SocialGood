from fastapi import APIRouter, UploadFile, File, Form
import tempfile, os, zipfile
import pandas as pd

from ..Tools.verify_csv_matches_table_schema import verify_csv_matches_table_schema
from ..config import get_engine
from ..Tools.create_database import create_database
from ..Tools.load_enviromental_data import load_environmental_data

router = APIRouter()

@router.post("/upload_zip/")
async def upload_zip(
    file: UploadFile = File(...),
    googleID: str = Form(...)
):
    if not file.filename.endswith(".zip"):
        return {"error": "File must be a .zip archive"}

    # 1. Create new database
    timeinstance = create_database(googleID)
    db_name = f"{googleID}-{timeinstance}"
    engine = get_engine(db_name)

    # 2. Load static environmental data
    try:
        load_environmental_data(db_name)
    except Exception as e:
        return {"error": f"Could not load EnvTable: {str(e)}"}

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded ZIP file
        zip_path = os.path.join(tmpdir, file.filename)
        with open(zip_path, "wb") as f:
            f.write(await file.read())

        # Extract contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        # 3. Define priority order (excluding EnvTable.csv)
        priority_order = [
            "Sku.csv",
            "Plant.csv",
            "Item.csv",
            "ProcessDefinition.csv",
            "Process.csv",
            "ItemProcess.csv",
            "PlantSKUQuantity.csv",
            "SkuProcess.csv"
        ]

        # 4. Sort files according to priority
        csv_files = sorted(
            [f for f in os.listdir(tmpdir) if f.endswith(".csv")],
            key=lambda x: priority_order.index(x) if x in priority_order else 999
        )

        # 5. Loop through and process in order
        for entry in csv_files:
            table_name = entry.replace(".csv", "")
            csv_path = os.path.join(tmpdir, entry)

            try:
                df = pd.read_csv(csv_path)
                verify_csv_matches_table_schema(engine, table_name, df)
                df.to_sql(table_name, con=engine, if_exists="append", index=False)

            except Exception as e:
                return {"error": f"{entry}: {str(e)}"}

    return {
        "message": "All CSVs imported successfully, EnvTable loaded.",
        "timeinstance": timeinstance,
        "db_name": db_name
    }
