# app/main.py
from fastapi import FastAPI
from app.routes import history_graph, upload_zip

app = FastAPI()

app.include_router(history_graph.router)
app.include_router(upload_zip.router)