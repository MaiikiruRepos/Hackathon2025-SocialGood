from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
import uuid
import os

router = APIRouter()

@router.post("/generate_config/")
async def generate_config(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    upload_dir = f"temp_uploads/{session_id}"
    os.makedirs(upload_dir, exist_ok=True)
    temp_path = os.path.join(upload_dir, "uploaded_bom.xlsx")

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    xl = pd.ExcelFile(temp_path)
    sheet_summaries = {}

    # Read each sheet's first few rows
    for sheet in xl.sheet_names:
        try:
            df = xl.parse(sheet, nrows=5)
            sheet_summaries[sheet] = df.columns.tolist()
        except Exception as e:
            sheet_summaries[sheet] = f"Error: {str(e)}"

    # Auto-config based on common BOM formats
    suggested_config = {
        "item": {
            "sheet": auto_pick(sheet_summaries, ["Material", "Finished", "Item"]),
            "columns": {
                "sku_id": guess_column(sheet_summaries, ["Component Part Number", "Part Number"]),
                "name": guess_column(sheet_summaries, ["Description", "Item Name"])
            },
            "default": {
                "subSKUID": None,
                "processID": None
            }
        },
        "plant": {
            "sheet": auto_pick(sheet_summaries, ["Source", "BOM", "Site"]),
            "columns": {
                "location": None,  # rarely present in the sheet, can default
                "skuID": guess_column(sheet_summaries, ["Part Number", "Component Part Number"])
            },
            "default": {
                "location": "MONTERREY, MX"
            }
        },
        "processes": {
            "sheet": auto_pick(sheet_summaries, ["Labor", "Overhead", "Process"]),
            "columns": {
                "processName": guess_column(sheet_summaries, ["Description", "Name"]),
                "employeeCount": guess_column(sheet_summaries, ["Total IDL Minutes Unit"]),
                "electricCount": guess_column(sheet_summaries, ["Scenario MFG Other Unit"]),
                "GasCount": guess_column(sheet_summaries, ["Scenario MFG Other Unit"])  # can be changed
            }
        },
        "plant_sku_quantity": {
            "sheet": auto_pick(sheet_summaries, ["Source", "BOM"]),
            "columns": {
                "plant_id": guess_column(sheet_summaries, ["Site Code"]),
                "sku_id": guess_column(sheet_summaries, ["Part Number", "Component Part Number"]),
                "quantity": guess_column(sheet_summaries, ["Part Qty", "Ext Qty"])
            },
            "default": {
                "plant_id": 1
            }
        },
        "item_process": {
            "from_sheets": [
                auto_pick(sheet_summaries, ["Labor", "Overhead", "Process"])
            ],
            "link_by": "sku_id"
        }
    }

    return JSONResponse({
        "sheet_overview": sheet_summaries,
        "suggested_config": suggested_config
    })


def auto_pick(summaries, keywords):
    for sheet, cols in summaries.items():
        if isinstance(cols, list):
            if any(keyword.lower() in sheet.lower() for keyword in keywords):
                return sheet
    return list(summaries.keys())[0] if summaries else None


def guess_column(summaries, keywords):
    for sheet, cols in summaries.items():
        if isinstance(cols, list):
            for col in cols:
                if any(keyword.lower() in col.lower() for keyword in keywords):
                    return col
    return None
