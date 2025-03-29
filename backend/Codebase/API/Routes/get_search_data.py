from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..config import get_engine

router = APIRouter()

class DBRequest(BaseModel):
    database: str

@router.post("/search_data/")
def search_data(payload: DBRequest):
    try:
        engine = get_engine(payload.database)

        with engine.connect() as conn:
            query = text("""
                SELECT 
                    psq.plant_id,
                    psq.sku_id,
                    s.sku_name AS description,
                    pcd.carbon_percent,
                    pcd.water_percent
                FROM PlantSKUQuantity psq
                JOIN Sku s ON psq.sku_id = s.sku_id
                LEFT JOIN PieChartData pcd ON psq.plant_id = pcd.plant_id
            """)
            result = conn.execute(query)
            rows = [dict(row._mapping) for row in result]  # ✅ Safe conversion
            return {"data": rows}
    except SQLAlchemyError as e:
        return {"error": str(e)}
