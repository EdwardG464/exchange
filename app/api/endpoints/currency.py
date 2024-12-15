from fastapi import APIRouter, Depends

from app.api.schemas.currency import CurrencyExchange, CurrencyExchangeResponse, ListOfCurrencies
from app.core.security import get_user_from_token
from app.utils.external_api import convert_currency, get_list_currencies


currency_router = APIRouter(prefix="/currency", tags=['Currency'])

@currency_router.post("/exchange/")
async def exchange_currency(exchange: CurrencyExchange, sub: str = Depends(get_user_from_token)):
    return CurrencyExchangeResponse(result=await convert_currency(exchange))


@currency_router.get("/list/", response_model=ListOfCurrencies)
async def list_currencies(sub: str = Depends(get_user_from_token)):
    return ListOfCurrencies(currencies=await get_list_currencies())