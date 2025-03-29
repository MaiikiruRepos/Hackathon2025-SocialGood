# app/main.py
from fastapi import FastAPI
from .Routes import (get_history_graph, upload_zip, get_ratings,
                     get_plant_list, get_plant_carbon, get_plant_water,
                     get_search_data, convert_bom, generate_config,
                     drop_user_databases_api, print_db_contents_api,
                     test_api, get_all_timestamps)



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_history_graph.router)
app.include_router(upload_zip.router)
app.include_router(get_ratings.router)
app.include_router(get_plant_list.router)
app.include_router(get_plant_carbon.router)
app.include_router(get_plant_water.router)
app.include_router(get_search_data.router)
app.include_router(convert_bom.router)
app.include_router(generate_config.router)
app.include_router(drop_user_databases_api.router)
app.include_router(print_db_contents_api.router)

app.include_router(test_api.router)

app.include_router(get_all_timestamps.router)