import os
import re
import plotly.express as px
import pandas as pd
from collections import defaultdict
from backend.Codebase.API.config import get_engine
from backend.demo.heatmap.country_code_to_name import country_code_to_name
import webbrowser

os.makedirs("charts_output", exist_ok=True)

def get_all_db_names_for_year(target_year: str) -> list:
    engine = get_engine("information_schema")
    query = "SELECT SCHEMA_NAME FROM schemata"
    df = pd.read_sql(query, engine)
    col_name = df.columns[0]  # Dynamically get column name
    all_dbs = df[col_name].tolist()

    pattern = re.compile(r".*-(\d{4})")
    return [db for db in all_dbs if (match := pattern.match(db)) and match.group(1) == target_year]

def collect_country_scores(db_names, score_type):
    country_totals = defaultdict(float)
    country_counts = defaultdict(int)

    for db_name in db_names:
        try:
            engine = get_engine(db_name)
            query = f"""
            SELECT
                Plant.country_code,
                SUM(PieChartData.{score_type}_percent) AS total
            FROM PieChartData
            JOIN Plant ON PieChartData.plant_id = Plant.plant_id
            GROUP BY Plant.country_code
            """
            df = pd.read_sql(query, con=engine)
            for _, row in df.iterrows():
                code = row["country_code"]
                country_totals[code] += row["total"]
                country_counts[code] += 1
        except Exception as e:
            print(f"Skipping {db_name}: {e}")

    # Compute averages
    averaged = {
        code: total / country_counts[code]
        for code, total in country_totals.items()
    }

    return averaged

def generate_world_heatmap(score_data: dict, score_type: str, year: str):
    df = pd.DataFrame(list(score_data.items()), columns=["country_code", "total"])
    df["country_name"] = df["country_code"].apply(country_code_to_name)
    df = df.dropna(subset=["country_name"])

    fig = px.choropleth(
        df,
        locations="country_name",
        locationmode="country names",
        color="total",
        hover_name="country_name",
        color_continuous_scale="YlGnBu" if score_type == "water" else "YlOrRd",
        title=f"Average {score_type.capitalize()} Impact by Country ({year})"
    )

    fig.update_layout(geo=dict(showframe=False, showcoastlines=True))
    output_path = f"charts_output/{score_type}_heatmap_{year}.html"
    fig.write_html(output_path)
    print(f"Saved heatmap: {output_path}")
    webbrowser.open(f"file://{os.path.abspath(output_path)}")

def generate_world_heatmaps_for_year(year: str):
    db_names = get_all_db_names_for_year(year)

    for score_type in ["carbon", "water"]:
        data = collect_country_scores(db_names, score_type)
        generate_world_heatmap(data, score_type, year)


if __name__ == "__main__":
    target_year = "2023"
    db_names = get_all_db_names_for_year(target_year)

    for score_type in ["carbon", "water"]:
        data = collect_country_scores(db_names, score_type)
        generate_world_heatmap(data, score_type, target_year)
