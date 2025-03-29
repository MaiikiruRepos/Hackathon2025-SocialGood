from ..config import get_engine
from sqlalchemy import insert, text

def compute_piechartdata():
    pass


def load_overall_score(db_name: str,carbonScore: float, waterScore: float) -> None:
    """
    This method will load the overall score of the database given the values to load.
    You should only call this method once per database.

    params:
        db_name: the database in question. This should be of the form googleid-timeinstance
            where timeinstance is the time formatted as "%Y-%m-%d_%H:%M"
        carbonScore: float. The total carbon score of the entire database.
        waterScore: float. The total water score of the entire database.
    """
    try:
        with get_engine(db_name).connect() as conn:
            stmt = insert("OverallScore").values(carbonScore=carbonScore, waterScore=waterScore)
            conn.execute(stmt)

    except Exception as e:
        print({"error": f"Failed to query database {db_name}: {str(e)}"})
