import re
from sqlalchemy import text
from fastapi import APIRouter
from ..config import get_engine
from ..models import OnlyGoogle

router = APIRouter()


@router.post("/get_history_graph/")
def get_history_graph(input_data: OnlyGoogle):
    google_id = str(input_data.googleID)
    result = {"instance": {}}  # Initialize the instance key to an empty dictionary
    pattern = r'^' + re.escape(google_id) + r'-(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})$'

    with get_engine().connect() as conn:
        databases = conn.execute(text("SHOW DATABASES")).fetchall()
        db_names = [row[0] for row in databases]

        for db_name in db_names:
            match = re.match(pattern, db_name)
            if match:
                print("Matched:", db_name)  # Debugging: check the matched database name
                # Access the captured timestamp
                timestamp = match.group(1)

                try:
                    with get_engine(db_name).connect() as user_conn:
                        # Query the database for carbon and water scores
                        score = user_conn.execute(
                            text("SELECT carbon_score, water_score FROM OverallScore LIMIT 1;")
                        ).fetchone()

                        if score:
                            # Add the retrieved scores to the result
                            result["instance"][timestamp] = {
                                "carbon": float(score[0]),
                                "water": float(score[1])
                            }
                except Exception as e:
                    print(f"Error querying {db_name}: {e}")
                    continue  # Continue to the next database if an error occurs
            else:
                print(f"Not a match for {db_name}")  # Debugging: print unmatched database names

    # Return the result with the instance containing the data
    return result
