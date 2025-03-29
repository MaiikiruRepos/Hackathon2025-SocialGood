from fastapi import APIRouter
from sqlalchemy import text
from ..config import get_engine
from ..models import OnlyGoogle

router = APIRouter()

@router.post("/get_all_timestamps/")
def get_all_timestamps(input_data: OnlyGoogle) -> dict:
    google_id: str = str(input_data.googleID)
    result: dict = {"timestamps": []}

    try:
        # Connect to the default MySQL system database to get all schemas
        with get_engine("information_schema").connect() as conn:
            databases = conn.execute(text("SELECT SCHEMA_NAME FROM SCHEMATA")).fetchall()

        # Filter those matching our pattern
        prefix = f"{google_id}-"
        for db in databases:
            schema_name = db[0]
            if schema_name.startswith(prefix):
                timestamp = schema_name[len(prefix):]
                result["timestamps"].append(timestamp)

    except Exception as e:
        result = {"error": f"Failed to list timestamps for google_id {google_id}: {str(e)}"}

    return result
