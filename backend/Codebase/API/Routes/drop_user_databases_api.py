# backend/Codebase/API/Routes/test_api.py

from fastapi import APIRouter

from backend.Codebase.API.Tools.drop_user_databases import drop_user_databases

router = APIRouter()

@router.post("/drop_user_databases_api/")
def drop_user_databases_api():
    print("API called: Dropping user databases")

    dropped_dbs = drop_user_databases()

    return {
        "message": "Databases dropped successfully.",
        "dropped_databases": dropped_dbs
    }
