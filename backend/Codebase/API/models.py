# app/models.py
from pydantic import BaseModel

class HistoryInput(BaseModel):
    googleID: str
    timeInstance: str


class SearchInput(BaseModel):
    pass
