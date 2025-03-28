from fastapi import APIRouter, Query

from backend.Codebase.API.Tools.print_db_contents import print_db_contents

router = APIRouter()

@router.get("/print_db_contents_api/")
def print_db_contents_api(db_name: str = Query(..., description="The name of the database to inspect")):
    print(f"API called: Printing contents of database '{db_name}'")

    try:
        print_db_contents(db_name)
        return {
            "message": f"Database '{db_name}' printed to console successfully."
        }
    except Exception as e:
        return {
            "error": str(e)
        }
