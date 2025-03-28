from fastapi import APIRouter
from sqlalchemy import text
from config import get_engine
from models import HistoryInput

router = APIRouter()

@router.post("/get_plant_water/")
def get_plant_water(input_data: HistoryInput):
    google_id = str(input_data.googleID)
    time_instance = input_data.timeInstance
    db_name = f"{google_id}-{time_instance}"
    result = {"plant": {}}

    try:
        with get_engine(db_name).connect() as conn:
            rows = conn.execute(
                text("SELECT plant_id, water_percent FROM PieChartData")
            ).fetchall()

            result["plant"] = {
                str(row[0]).zfill(5): float(row[1]) for row in rows
            }

    except Exception as e:
        result = {"error": f"Failed to query database {db_name}: {str(e)}"}

    return result
