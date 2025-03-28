# app/models.py
from pydantic import BaseModel

class HistoryInput(BaseModel):
    googleID: int
