from pydantic import BaseModel
from fastapi import File

class UploadResponse(BaseModel):
    message: str
    