# app/models.py
from pydantic import BaseModel

class HistoryInput(BaseModel):
    googleID: str

class SingleInput(BaseModel):
    googleID: str
    timeInstance: str

class SearchInput(BaseModel):
    googleID: str
    timeInstance: str
    searchBarData: str
    plantFilter: list[int]
    returnStartNum: int
    returnEndNum: int
