from controllers.usage_controller import UsageController
from fastapi.responses import JSONResponse
from schemas.usage_schemas import UsageResponse, UsageResponseFail, UsageRescrapeResponse
from fastapi import status
from traceback import format_exc
import logging

class UsageView:
    
    def __init__(self):
        self.__controller = UsageController()
        
    async def get_all_usage_today(self) -> JSONResponse:
        """Metodo responsavel por buscar e mostar todos Usages do dia atual

        Returns:
            JSONResponse: Resposta no formato JSON
        """
        try:
            result = await self.__controller.get_all_usage_today()
            if len(result) == 0:
                return JSONResponse(
                    UsageResponseFail(message="Não houve usos de tokens hoje!").model_dump(), 
                    status.HTTP_400_BAD_REQUEST
                )
            
            return JSONResponse(
                UsageResponse(data={"usage" : result}).model_dump(),
                status.HTTP_200_OK
            )
            
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                    UsageResponseFail(message="Erro inesperado contate o Administrador!").model_dump(), 
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
    async def rescrape_last_companies_today(self) -> JSONResponse:
        """Metodo responsavel por iniciar o rescraping da ultimas 5 cidades

        Returns:
            JSONResponse: Resposta no formato JSON
        """
        
        try:
            result = await self.__controller.rescrape_last_companies_today()
            
            if not result:
                return JSONResponse(
                    UsageRescrapeResponse(message="Não há cidades para fazer scraping novamente hoje!").model_dump(),
                    status.HTTP_400_BAD_REQUEST
                )
                
            
            return JSONResponse(
                UsageRescrapeResponse(message="Sucesso").model_dump(),
                status.HTTP_200_OK
            )
        
        except Exception:
            logging.error(format_exc())
            
            return JSONResponse(
                    UsageResponseFail(message="Erro inesperado contate o Administrador!").model_dump(), 
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                )