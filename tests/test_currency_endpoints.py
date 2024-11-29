import pytest
from fastapi.testclient import TestClient

from app.core.security import get_user_from_token
from main import app


def override_get_user_from_token():
    return "username"


client = TestClient(app)


@pytest.fixture(scope='module')
def overrides_get_user():
    app.dependency_overrides[get_user_from_token] = override_get_user_from_token
    yield app
    del app.dependency_overrides[get_user_from_token]


def test_currencies_list(overrides_get_user):
    response = client.get("/currency/list")
    assert response.status_code == 200
    assert 'currencies' in response.json()


def test_exchange_currency(overrides_get_user):
    # correct request
    response = client.post(
        url="/currency/exchange",
        json={'from_currency': "USD",
              'to_currency': "RUB",
              'amount': 1000}
    )
    assert response.status_code == 200
    assert 'result' in response.json()

    # incorrect code currency
    response = client.post(
        url="/currency/exchange",
        json={'from_currency': "XXX",
              'to_currency': "USD",
              'amount': 1000}
    )
    assert response != 200
    assert response.json()['detail'] == "You have entered an invalid \"from\" property. [Example: from=EUR]"