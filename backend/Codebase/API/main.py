# app/main.py
from fastapi import FastAPI
from Routes import get_history_graph, upload_zip

app = FastAPI()

app.include_router(get_history_graph.router)
app.include_router(upload_zip.router)