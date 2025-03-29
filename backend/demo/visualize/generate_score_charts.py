from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
import os

from backend.Codebase.API.config import get_engine

THEMES = ["pcb", "trucking", "insurance"]
THEME_BASE_TIMES = {
    "pcb": datetime(2023, 1, 1, 0, 0),
    "trucking": datetime(2023, 2, 1, 0, 0),
    "insurance": datetime(2023, 3, 1, 0, 0)
}
NUM_SETS = 4
OUTPUT_DIR = "charts_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_overall_score(df, theme, set_num):
    fig, ax = plt.subplots()
    ax.bar(["Carbon", "Water"], [df["carbon_score"], df["water_score"]], color=["green", "blue"])
    ax.set_title(f"{theme.capitalize()} Set {set_num}: Overall Score")
    ax.set_ylabel("Score")
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, f"{theme}_set_{set_num}_overall.png")
    print(f"Saving chart to: {save_path}")
    plt.savefig(save_path)
    print(f"Saved: {os.path.exists(save_path)}")
    plt.close()

def plot_overall_trends(score_data, theme):
    df = pd.DataFrame(score_data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d_%H-%M")
    df = df.sort_values("timestamp")

    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["carbon_score"], label="Carbon", marker="o", color="green")
    ax.plot(df["timestamp"], df["water_score"], label="Water", marker="o", color="blue")

    ax.set_title(f"{theme.capitalize()} Sustainability Trend")
    ax.set_xlabel("Time")
    ax.set_ylabel("Score")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    save_path = os.path.join(OUTPUT_DIR, f"trend_{theme}.png")
    plt.savefig(save_path)
    print(f"Saved trend chart: {save_path}")
    plt.close()



def plot_pie_charts(df, theme, set_num):
    for _, row in df.iterrows():
        fig, ax = plt.subplots()
        ax.pie([row["carbon_percent"], row["water_percent"]],
               labels=["Carbon", "Water"],
               autopct="%1.1f%%",
               colors=["green", "blue"])
        ax.set_title(f"{theme.capitalize()} Set {set_num} - Plant {row['plant_id']}")
        plt.savefig(f"{OUTPUT_DIR}/{theme}_set_{set_num}_plant_{row['plant_id']}_pie.png")
        plt.close()

def fetch_and_visualize(theme, set_num, timestamp_str):
    db_name = f"{theme}_user-{timestamp_str}"
    print(f"Connecting to {db_name}")
    try:
        engine = get_engine(db_name)

        # Show tables in the DB
        tables = pd.read_sql("SHOW TABLES", con=engine)
        print(f"Tables in {db_name}: {[t[0] for t in tables.values]}")

        # Fetch OverallScore
        overall_df = pd.read_sql("SELECT * FROM OverallScore", con=engine)
        print(f"OverallScore rows: {len(overall_df)}")
        if not overall_df.empty:
            print(f"Plotting OverallScore: {overall_df.iloc[0].to_dict()}")
            plot_overall_score(overall_df.iloc[0], theme, set_num)

        # Fetch PieChartData
        pie_df = pd.read_sql("SELECT * FROM PieChartData", con=engine)
        print(f"PieChartData rows: {len(pie_df)}")
        if not pie_df.empty:
            plot_pie_charts(pie_df, theme, set_num)

    except Exception as e:
        print(f"Failed for {db_name}: {e}")


def main():
    for theme in THEMES:
        base_time = THEME_BASE_TIMES[theme]
        trend_data = []

        for i in range(1, NUM_SETS + 1):
            t = base_time + relativedelta(months=(i - 1) * 7)
            timestamp_str = t.strftime("%Y-%m-%d_%H-%M")
            db_name = f"{theme}_user-{timestamp_str}"
            print(f"Connecting to {db_name}")

            try:
                engine = get_engine(db_name)

                overall_df = pd.read_sql("SELECT * FROM OverallScore", con=engine)
                if not overall_df.empty:
                    row = overall_df.iloc[0]
                    trend_data.append({
                        "timestamp": timestamp_str,
                        "carbon_score": row["carbon_score"],
                        "water_score": row["water_score"]
                    })
                    plot_overall_score(row, theme, i)

                pie_df = pd.read_sql("SELECT * FROM PieChartData", con=engine)
                if not pie_df.empty:
                    plot_pie_charts(pie_df, theme, i)

            except Exception as e:
                print(f"Failed for {db_name}: {e}")

        # After looping through sets, plot trend
        if trend_data:
            plot_overall_trends(trend_data, theme)

if __name__ == "__main__":
    main()
