# Results/compute_results.py

import os
from .. import get_engine
from sqlalchemy import text,insert

def compute_results(engine):
    result_dir = os.path.dirname(__file__)  # This folder (Results/)
    print("Running sustainability metrics...\n")

    with engine.connect() as conn:
        # Run all three SQL scripts
        for file in ["sku_score.sql", "overall_score.sql", "pie_chart.sql"]:
            sql_path = os.path.join(result_dir, file)
            if not os.path.exists(sql_path):
                print(f"Missing SQL file: {file}")
                continue

            print(f"→ Executing: {file}")
            with open(sql_path, "r") as f:
                sql_script = f.read()

            for statement in sql_script.strip().split(";"):
                stmt = statement.strip()
                if stmt:
                    conn.execute(text(stmt))

        print("\nMetrics updated successfully.\n")

        # SkuScore
        result = conn.execute(text("SELECT * FROM SkuScore LIMIT 5;"))
        for row in result.mappings().all():
            print(dict(row))

        # OverallScore
        result = conn.execute(text("SELECT * FROM OverallScore;"))
        for row in result.mappings().all():
            print(dict(row))

        # PieChartData
        result = conn.execute(text("SELECT * FROM PieChartData;"))
        for row in result.mappings().all():
            print(dict(row))

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

