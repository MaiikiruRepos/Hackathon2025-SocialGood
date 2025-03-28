from fastapi import APIRouter

router = APIRouter()

@router.post("/test_api/")
def test_api():
    # Simulate extracting values

    print("API return")

    # Instead of DB logic, just return a dummy response
    return {
        "message": f"API Return"
    }
