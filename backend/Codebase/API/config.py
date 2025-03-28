# app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine

env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_USER_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")

def get_engine(db_name="information_schema"):
    return create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{db_name}")
