from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from ..config import get_engine
from ..models import SearchInput

router = APIRouter()


@router.post("/search_data/")
def search_data(input_data: SearchInput):
    google_id = str(input_data.googleID)

    # Other fields omitted for brevity...
    # time_instance, search_term, plant_filter, start, end...

    # Example query...
    try:
        with get_engine().connect() as conn:
            result_proxy = conn.execute(text("""
                SELECT s.sku_id, s.sku_name, sc.plant_id, sc.carbon_score, sc.water_score
                FROM Sku s
                LEFT JOIN SkuScore sc ON s.sku_id = sc.sku_id
            """))

            # This returns each row as a dict-like object (RowMapping):
            mapped_rows = result_proxy.mappings().all()

            # Now convert each RowMapping to a normal Python dict:
            rows = [dict(r) for r in mapped_rows]

            return {"data": rows}
    except SQLAlchemyError as e:
        return {"error": str(e)}
