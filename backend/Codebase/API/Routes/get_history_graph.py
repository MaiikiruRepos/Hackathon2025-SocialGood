# app/routes/history_graph.py
import re
from sqlalchemy import text
from app.config import get_engine
from fastapi import APIRouter
from app.models import HistoryInput

router = APIRouter()

@router.post("/get_history_graph/")
def get_history_graph(input_data: HistoryInput):
    google_id = str(input_data.googleID)
    result = {"plant": {}}
    pattern = re.compile(f"^{google_id}-(\\d{{4}}-\\d{{2}}-\\d{{2}}_\\d{{2}}:\\d{{2}})$")

    with get_engine().connect() as conn:
        databases = conn.execute(text("SHOW DATABASES")).fetchall()
        db_names = [row[0] for row in databases]

        for db_name in db_names:
            match = pattern.match(db_name)
            if not match:
                continue

            timestamp = match.group(1)

            try:
                with get_engine(db_name).connect() as user_conn:
                    score = user_conn.execute(
                        text("SELECT carbonScore, waterScore FROM OverallScore LIMIT 1")).fetchone()
                    if score:
                        result["plant"][timestamp] = {
                            "carbon": float(score[0]),
                            "water": float(score[1])
                        }
            except Exception as e:
                print(f"Error querying {db_name}: {e}")
                continue

    return result
