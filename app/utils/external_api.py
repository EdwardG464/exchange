import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.api.schemas.currency import CurrencyExchange, CurrencyExchangeResponse


def get_list_currencies() -> dict[str, str]:
    headers = {"apikey": settings.currency_data_api_key}
    res = httpx.get(url='https://api.apilayer.com/currency_data/list', headers=headers)
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="We have failed to process your request.")
    currencies_dict = res.json()
    return currencies_dict['currencies']


def convert_currency(cur_exchange: CurrencyExchange):
    headers = {'apikey': settings.currency_data_api_key}
    params = {"amount": cur_exchange.amount,
              "from": cur_exchange.from_currency,
              "to": cur_exchange.to_currency}

    res = httpx.get(url='https://api.apilayer.com/currency_data/convert',
                    headers=headers, params=params)

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail="We have failed to process your request.")

    res_dict = res.json()

    if res_dict['success'] is False:
        raise HTTPException(status_code=res_dict['error']['code'],
                            detail=res_dict['error']['info'])

    return res_dict['result']