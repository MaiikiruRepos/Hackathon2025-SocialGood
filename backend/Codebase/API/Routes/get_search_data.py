from fastapi import APIRouter
from sqlalchemy import text
from ..config import get_engine
from ..models import SearchInput

router = APIRouter()

@router.post("/search_data/")
def search_data(input_data: SearchInput):
    google_id = str(input_data.googleID)
    time_instance = input_data.timeInstance
    search_term = input_data.searchBarData.lower()
    plant_filter = input_data.plantFilter
    start = input_data.returnStartNum
    end = input_data.returnEndNum
    db_name = f"{google_id}-{time_instance}"

    result = {"plant": {}}

    try:
        with get_engine(db_name).connect() as conn:
            # Build base query to get plant_id and sku_id
            query = """
                SELECT pq.plant_id, pq.sku_id
                FROM PlantSKUQuantity pq
                JOIN Item i ON pq.sku_id = i.sku_id
            """
            conditions = []
            if plant_filter:
                plant_ids = ",".join(str(pid) for pid in plant_filter)
                conditions.append(f"pq.plant_id IN ({plant_ids})")
            if search_term:
                conditions.append(f"LOWER(i.name) LIKE :search_term")
            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " GROUP BY pq.plant_id, pq.sku_id"

            rows = conn.execute(
                text(query),
                {"search_term": f"%{search_term}%"} if search_term else {}
            ).fetchall()

            # Build mapping of plant → skus
            plant_sku_map = {}
            unique_sku_ids = set()
            for plant_id, sku_id in rows:
                plant_sku_map.setdefault(plant_id, set()).add(sku_id)
                unique_sku_ids.add(sku_id)

            # Pagination on SKU IDs
            all_sku_ids = list(unique_sku_ids)
            paginated_sku_ids = all_sku_ids[start - 1:end]

            if not paginated_sku_ids:
                return {"plant": {}}

            sku_id_placeholders = ",".join(str(sid) for sid in paginated_sku_ids)

            # Fetch SKU details
            sku_rows = conn.execute(text(f"""
                SELECT i.sku_id, i.name, ss.carbonScore, ss.waterScore
                FROM Item i
                LEFT JOIN SkuScore ss ON i.sku_id = ss.sku_id
                WHERE i.sku_id IN ({sku_id_placeholders})
            """)).fetchall()

            sku_data = {
                row[0]: {
                    "Description": row[1],
                    "CarbonLB": str(row[2]) if row[2] is not None else "0",
                    "WaterGal": str(row[3]) if row[3] is not None else "0"
                } for row in sku_rows
            }

            # Build final response
            for plant_id, sku_ids in plant_sku_map.items():
                plant_key = str(plant_id).zfill(5)
                result["plant"][plant_key] = {"sku": {}}
                for sku_id in sku_ids:
                    if sku_id in paginated_sku_ids and sku_id in sku_data:
                        sku_key = str(sku_id).zfill(3)
                        result["plant"][plant_key]["sku"][sku_key] = sku_data[sku_id]

    except Exception as e:
        result = {"error": f"Failed to query database {db_name}: {str(e)}"}

    return result
