import os
from sqlalchemy import text
from datetime import datetime

def compute_results(engine, theme=None, timeinstance=None):
    result_dir = os.path.dirname(__file__)  # This folder (Results/)
    print("Running sustainability metrics...\n")

    with engine.begin() as conn:
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
                    print(f"Executing SQL: {stmt[:80]}...")  # Preview the query
                    conn.execute(text(stmt))

        def get_decrease_factor(base_date_str, current_str, months_per_step=7, decrease_rate=0.9):
            base_date = datetime.strptime(base_date_str, "%Y-%m-%d_%H-%M")
            current_date = datetime.strptime(current_str, "%Y-%m-%d_%H-%M")
            delta_months = (current_date.year - base_date.year) * 12 + (current_date.month - base_date.month)
            steps = delta_months // months_per_step
            return decrease_rate ** steps

        if theme and timeinstance:
            base_start_dates = {
                "pcb": "2023-01-01_00-00",
                "trucking": "2023-02-01_00-00",
                "insurance": "2023-03-01_00-00"
            }
            base = base_start_dates.get(theme.lower())
            if base:
                factor = get_decrease_factor(base, timeinstance)
                print(f"Applying sustainability improvement factor: {factor:.3f}")

                conn.execute(text(f"""
                    UPDATE OverallScore
                    SET carbon_score = ROUND(carbon_score * {factor}, 2),
                        water_score = ROUND(water_score * {factor}, 2)
                """))

                conn.execute(text(f"""
                    UPDATE PieChartData
                    SET carbon_percent = ROUND(carbon_percent * {factor}, 2),
                        water_percent = ROUND(water_percent * {factor}, 2)
                """))

                conn.execute(text(f"""
                    UPDATE SkuScore
                    SET carbon_score = ROUND(carbon_score * {factor}, 2),
                        water_score = ROUND(water_score * {factor}, 2)
                """))

        print("\nMetrics updated successfully.\n")

        # Print sample results
        result = conn.execute(text("SELECT * FROM SkuScore LIMIT 5;"))
        for row in result.mappings().all():
            print(dict(row))

        result = conn.execute(text("SELECT * FROM OverallScore;"))
        for row in result.mappings().all():
            print(dict(row))

        result = conn.execute(text("SELECT * FROM PieChartData;"))
        for row in result.mappings().all():
            print(dict(row))
