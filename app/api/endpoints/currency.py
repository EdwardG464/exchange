from fastapi import APIRouter, Depends

from app.core.security import get_user_from_token
from app.utils.external_api import get_list_currencies, convert_currency
from ..schemas.currency import CurrencyExchange, CurrencyExchangeResponse, ListOfCurrencies

currency_router = APIRouter(prefix="/currency", tags=['Currency'])


@currency_router.post("/exchange/")
def exchange_currency(exchange: CurrencyExchange, sub: str = Depends(get_user_from_token)):
    return CurrencyExchangeResponse(result=convert_currency(exchange))


@currency_router.get("/list/", response_model=ListOfCurrencies)
def list_currencies(sub: str = Depends(get_user_from_token)):
    return ListOfCurrencies(currencies=get_list_currencies())