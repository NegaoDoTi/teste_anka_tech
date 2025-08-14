from fastapi import APIRouter
from fastapi.responses import JSONResponse
from views.usage_view import UsageView

usage_route = APIRouter()

"""Rota de usage/today e metodos aceitos """
@usage_route.get("/usage/today", response_class=JSONResponse)
async def get_usage_today() -> JSONResponse:
    return await UsageView().get_all_usage_today()

@usage_route.post("/usage/today", response_class=JSONResponse)
async def rescrape() -> JSONResponse:
    return await UsageView().rescrape_last_companies_today()