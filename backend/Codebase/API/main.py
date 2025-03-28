# app/main.py
from fastapi import FastAPI
from Routes import (get_history_graph, upload_zip, get_ratings,
                    get_plant_list, get_plant_carbon, get_plant_water,
                    get_search_data, convert_bom, generate_config)

app = FastAPI()

app.include_router(get_history_graph.router)
app.include_router(upload_zip.router)
app.include_router(get_ratings.router)
app.include_router(get_plant_list.router)
app.include_router(get_plant_carbon.router)
app.include_router(get_plant_water.router)
app.include_router(get_search_data.router)
app.include_router(convert_bom.router)
app.include_router(generate_config.router)