import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from backend.Codebase.API.Tools.convert_bom import convert_bom

router = APIRouter()

@router.post("/convert_bom/")
async def convert_bom_route(
    excel: UploadFile = File(...),
    config: UploadFile = File(None)
):
    session_id = str(uuid.uuid4())
    session_dir = os.path.join("temp_uploads", session_id)
    os.makedirs(session_dir, exist_ok=True)

    excel_path = os.path.join(session_dir, "bom.xlsx")
    config_path = os.path.join(session_dir, "config.yaml")
    output_dir = os.path.join(session_dir, "output")

    # Save uploaded Excel
    with open(excel_path, "wb") as f:
        f.write(await excel.read())

    # Save config or fallback to default
    if config:
        with open(config_path, "wb") as f:
            f.write(await config.read())
    else:
        config_path = "config.yaml"  # fallback to your default template

    # Run the conversion
    convert_bom(excel_path, config_path, output_dir)

    # Zip the output
    zip_path = f"{output_dir}.zip"
    shutil.make_archive(output_dir, 'zip', output_dir)

    return FileResponse(zip_path, filename="converted_bom.zip", media_type="application/zip")
