from fastapi import APIRouter, UploadFile
from views.upload_view import UploadView
from fastapi.responses import JSONResponse

upload_route = APIRouter()

"""Rota de upload """
@upload_route.post("/upload", response_class=JSONResponse)
async def upload_csv(file: UploadFile) -> JSONResponse:
    file_data = await file.read()
    return await UploadView().save_upload_csv(file_data=file_data, file_name=file.filename)