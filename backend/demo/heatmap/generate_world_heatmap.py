import os
import plotly.express as px
import pandas as pd
from backend.Codebase.API.config import get_engine
from backend.demo.heatmap.country_code_to_name import country_code_to_name
import webbrowser

os.makedirs("charts_output", exist_ok=True)

def generate_world_heatmap(db_name, score_type="carbon"):
    engine = get_engine(db_name)

    # Step 1: Run SQL query
    query = f"""
    SELECT
        Plant.country_code,
        SUM(PieChartData.{score_type}_percent) AS total
    FROM PieChartData
    JOIN Plant ON PieChartData.plant_id = Plant.plant_id
    GROUP BY Plant.country_code
    """
    df = pd.read_sql(query, con=engine)

    # Step 2: Map to full country names
    df["country_name"] = df["country_code"].apply(country_code_to_name)
    df = df.dropna(subset=["country_name"])  # Remove any unmapped

    # Step 3: Plot
    fig = px.choropleth(
        df,
        locations="country_name",
        locationmode="country names",  # ✅ this works with full names
        color="total",
        hover_name="country_name",
        color_continuous_scale="YlOrRd",
        title=f"{score_type.capitalize()} Impact by Country"
    )

    fig.update_layout(geo=dict(showframe=False, showcoastlines=True))
    output_path = f"charts_output/{db_name}_{score_type}_heatmap.html"
    fig.write_html(output_path)
    print(f"🌍 Saved heatmap: {output_path}")
    webbrowser.open(f"file://{os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_world_heatmap("pcb_user-2023-01-01_00-00", score_type="carbon")
    generate_world_heatmap("pcb_user-2023-01-01_00-00", score_type="water")
