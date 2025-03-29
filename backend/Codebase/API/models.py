# app/models.py
from pydantic import BaseModel



class GoogleTime(BaseModel):
    """
    This wrapper class gets a single googleid-timeinstance pair.
    """
    googleID: str
    timeInstance: str

class OnlyGoogle(BaseModel):
    googleID: str


class SearchInput(BaseModel):
    googleID: str
    timeInstance: str
    searchBarData: str
    plantFilter: list[int]
    returnStartNum: int
    returnEndNum: int
