import random
from datetime import datetime, timedelta
from sqlalchemy import text
from backend.Codebase.API.config import get_engine
import pycountry

# Regions for carbon/water trends
REGIONAL_WEIGHTS = {
    "US": "north_america",
    "CA": "north_america",
    "CN": "asia",
    "IN": "asia",
    "JP": "asia",
    "DE": "europe",
    "FR": "europe",
    "IT": "europe",
    "GB": "europe",
    "BR": "south_america",
    "ZA": "africa",
    "AU": "oceania",
    # Fallback
    "DEFAULT": "global"
}

REGIONAL_TRENDS = {
    "north_america": {"carbon_range": (20.0, 70.0), "water_range": (30.0, 80.0)},
    "asia": {"carbon_range": (25.0, 80.0), "water_range": (20.0, 75.0)},
    "europe": {"carbon_range": (5.0, 40.0), "water_range": (10.0, 50.0)},
    "south_america": {"carbon_range": (15.0, 65.0), "water_range": (25.0, 80.0)},
    "africa": {"carbon_range": (30.0, 85.0), "water_range": (40.0, 90.0)},
    "oceania": {"carbon_range": (10.0, 50.0), "water_range": (15.0, 60.0)},
    "global": {"carbon_range": (10.0, 80.0), "water_range": (20.0, 90.0)},
}

def get_all_country_codes():
    """Return all valid ISO alpha-2 country codes, excluding Antarctica (AQ)."""
    return [c.alpha_2 for c in pycountry.countries if c.alpha_2 != "AQ"]

def get_region(country_code):
    return REGIONAL_WEIGHTS.get(country_code, REGIONAL_WEIGHTS["DEFAULT"])

def get_weighted_country_pool():
    """Return a weighted list of countries favoring high-volume ones."""
    all_codes = get_all_country_codes()  # Already excludes AQ

    high_weight = ["US", "CN", "IN"]
    med_weight = ["BR", "DE", "FR", "JP", "ZA", "GB", "AU"]
    low_weight = [c for c in all_codes if c not in high_weight + med_weight]

    pool = []
    pool += high_weight * 10
    pool += med_weight * 4
    pool += low_weight

    return pool



THEMES = ["ai", "lego", "insurance"]

def generate_user_ids(prefix: str, count: int):
    return [f"{prefix}_user_{i:03d}" for i in range(1, count + 1)]

def generate_timestamps(start_year=2022, end_year=2025, interval_months=(6, 8)):
    timestamps = []
    current = datetime(start_year, 1, 1)
    while current.year < end_year:
        timestamps.append(current.strftime("%Y-%m-%d_%H-%M"))
        step = random.randint(*interval_months)
        current += timedelta(days=30 * step)
    return timestamps

def create_fake_db(google_id, timestamp, country_pool, home_country):
    db_name = f"{google_id}-{timestamp}"

    # Step 1: Create DB
    base_engine = get_engine("information_schema")
    with base_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))

    # Step 2: Create tables
    engine = get_engine(db_name)
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Plant (
                plant_id INT AUTO_INCREMENT PRIMARY KEY,
                country_code VARCHAR(3),
                location VARCHAR(100)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS PieChartData (
                id INT AUTO_INCREMENT PRIMARY KEY,
                plant_id INT,
                carbon_percent FLOAT,
                water_percent FLOAT
            )
        """))

        # Add 1–2 home country plants first
        for _ in range(random.randint(1, 2)):
            conn.execute(
                text("INSERT INTO Plant (country_code, location) VALUES (:code, :loc)"),
                {"code": home_country, "loc": f"{home_country} HQ"}
            )

        # Add 2–5 random global plants
        for _ in range(random.randint(2, 5)):
            country = random.choice(country_pool)
            conn.execute(
                text("INSERT INTO Plant (country_code, location) VALUES (:code, :loc)"),
                {"code": country, "loc": f"{country} Plant {random.randint(1, 20)}"}
            )

        # Insert impact data based on region
        plants = conn.execute(text("SELECT plant_id, country_code FROM Plant")).fetchall()
        for plant_id, country_code in plants:
            region = get_region(country_code)
            trend = REGIONAL_TRENDS[region]

            conn.execute(
                text("""
                    INSERT INTO PieChartData (plant_id, carbon_percent, water_percent)
                    VALUES (:pid, :carbon, :water)
                """),
                {
                    "pid": plant_id,
                    "carbon": round(random.uniform(*trend["carbon_range"]), 2),
                    "water": round(random.uniform(*trend["water_range"]), 2)
                }
            )


def run_bulk_user_generation(user_count=30):
    timestamps = generate_timestamps()
    country_pool = get_weighted_country_pool()

    for theme in THEMES:
        user_ids = generate_user_ids(theme, user_count)
        print(f"▶ Generating {user_count} users for theme: {theme}")
        for user_id in user_ids:
            home_country = random.choice(country_pool)
            for ts in timestamps:
                create_fake_db(user_id, ts, country_pool, home_country)
