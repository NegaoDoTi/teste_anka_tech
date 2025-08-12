from fastapi.responses import JSONResponse
from schemas.upload_schemas import UploadResponse
from fastapi import status
from controllers.upload_controller import UploadController

class UploadView:
    def __init__(self):
        self.__controller = UploadController()
        
    async def save_upload_csv(self, file_data:bytes, file_name:str) -> JSONResponse:
        
        type_file = file_name.split(".")[-1]
        
        if "csv" != type_file:
            return JSONResponse(UploadResponse(
                    message="Só é aceito arquivos do tipo CSV"
                ).model_dump(), 
                status.HTTP_400_BAD_REQUEST
            )
        try:
            await self.__controller.read_save_file(file_data)
        except Exception as e:
            message = e.args[0]
            return JSONResponse(
                UploadResponse(message=message).model_dump(),
                status.HTTP_400_BAD_REQUEST
            )
        
        return JSONResponse(
            UploadResponse(
                message="Sucesso, arquivo enviado para fila, a extração de dados começará em breve"
            ).model_dump(),
            status.HTTP_201_CREATED
        )
        
         
         