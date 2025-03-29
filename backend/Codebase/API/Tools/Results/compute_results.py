# Results/compute_results.py

import os
from sqlalchemy import text

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

