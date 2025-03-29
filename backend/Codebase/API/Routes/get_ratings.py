from fastapi import APIRouter
from sqlalchemy import text
from ..config import get_engine
from ..models import SingleInput

router = APIRouter()

@router.post("/get_ratings/")
def get_ratings(input_data: SingleInput):
    google_id: str = str(input_data.googleID)
    time_instance: str = input_data.timeInstance
    db_name: str = f"{google_id}-{time_instance}"
    result:dict = {}

    try:
        with get_engine(db_name).connect() as conn:
            score = conn.execute(
                text("SELECT carbonScore, waterScore FROM OverallScore LIMIT 1")
            ).fetchone()
            if score:
                result["carbon"] = float(score[0])
                result["water"] = float(score[1])
            else:
                result = {"error": "No score found in OverallScore"}
    except Exception as e:
        result = {"error": f"Failed to query database {db_name}: {str(e)}"}

    return result
