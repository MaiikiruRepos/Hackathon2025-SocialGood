# app/models.py
from pydantic import BaseModel

class HistoryInput(BaseModel):
    googleID: str
    timeInstance: list[str]

class SingleInput(BaseModel):
    """
    This wrapper class gets a single googleid-timeinstance pair.
    """
    googleID: str
    timeInstance: str



class SearchInput(BaseModel):
    pass
