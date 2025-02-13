import pytest
from httpx import AsyncClient, ASGITransport
from main import app

payload = {"username": "username_test3", "password": "qwerty122"}

@pytest.mark.asyncio
async def test_register_user():
    """Тест создания нового пользователя."""

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/register", json=payload)
        assert response.status_code == 200
        resp_json = response.json()
        assert resp_json == {"message": "User successfully created"}

        


@pytest.mark.asyncio
async def test_login_and_about_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/login", data=payload)
        assert response.status_code == 200
        resp_json = response.json()
        assert "access_token" in resp_json

        headers ={
            "Authorization": f"Bearer {resp_json['access_token']}"
        }
        resp_about = await ac.get("auth/about_me", headers=headers)
        assert resp_about.status_code == 200
        resp_about_json = resp_about.json()
        assert 'id' in resp_about_json