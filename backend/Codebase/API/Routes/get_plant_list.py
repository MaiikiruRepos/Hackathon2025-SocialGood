from fastapi import APIRouter
from sqlalchemy import text
from ..config import get_engine
from ..models import GoogleTime

router = APIRouter()

@router.post("/get_plant_list/")
def get_plant_list(input_data: GoogleTime) -> dict:
    google_id: str = input_data.googleID
    time_instance: str = input_data.timeInstance
    db_name: str = f"{google_id}-{time_instance}"
    result: dict = {"plants": []}

    try:
        with get_engine(db_name).connect() as conn:
            plants = conn.execute(
                text("SELECT plant_id, location FROM Plant")
            ).fetchall()

            result["plants"] = [
                {"plant_id": row[0], "location": row[1]} for row in plants
            ]
    except Exception as e:
        result = {"error": f"Failed to query database {db_name}: {str(e)}"}

    return result
