from datetime import datetime
import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.db.database import database
from app.schemas.dataset import DatasetResponse

router = APIRouter(prefix="/datasets", tags=["datasets"])

datasets_collection = database["datasets"]

DATASETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../datasets"))
os.makedirs(DATASETS_DIR, exist_ok=True)

from fastapi import Form

@router.post("", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    project_id: str = Form(...)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    save_path = os.path.join(DATASETS_DIR, file.filename)
    # Ensure unique filename
    counter = 1
    orig_name = file.filename
    while os.path.exists(save_path):
        name, ext = os.path.splitext(orig_name)
        file.filename = f"{name}_{counter}{ext}"
        save_path = os.path.join(DATASETS_DIR, file.filename)
        counter += 1

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    upload_time = datetime.utcnow()
    doc = {
        "project_id": project_id,
        "filename": file.filename,
        "upload_time": upload_time
    }
    result = await datasets_collection.insert_one(doc)

    return DatasetResponse(id=str(result.inserted_id), filename=file.filename, upload_time=upload_time)

@router.get("/projects/{project_id}/datasets", response_model=list[DatasetResponse])
async def list_datasets_by_project(project_id: str):
    cursor = datasets_collection.find({"project_id": project_id})
    datasets: list[DatasetResponse] = []
    async for doc in cursor:
        datasets.append(
            DatasetResponse(
                id=str(doc["_id"]),
                filename=doc.get("filename", ""),
                upload_time=doc.get("upload_time"),
            )
        )
    return datasets