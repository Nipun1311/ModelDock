from datetime import datetime

from pydantic import BaseModel


class DatasetCreate(BaseModel):
    filename: str


class DatasetResponse(BaseModel):
    id: str
    filename: str
    upload_time: datetime

