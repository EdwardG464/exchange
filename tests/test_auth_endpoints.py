import pytest
from fastapi.testclient import TestClient

from app.db.database import Base, get_db
from main import app
from .config import override_get_db, engine


Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(scope='module')
def overrides_get_db():
    app.dependency_overrides[get_db] = override_get_db
    yield app
    del app.dependency_overrides[get_db]


def test_reg_user(overrides_get_db):
    # reg new user
    response = client.post(
        url="/auth/register/",
        json={"username": "username_test", "password": "qwerty123"}
    )
    assert response.status_code == 200
    data_json = response.json()
    assert data_json == {"message": "User successfully created"}

    # reg user with existing username
    response = client.post(
        url="/auth/register/",
        json={"username": "username_test", "password": "qwerty123"}
    )
    assert response.status_code == 400
    data_json = response.json()
    assert data_json == {"detail": "User with username already exists"}


def test_login(overrides_get_db):
    # correct user data
    response = client.post(
        url="/auth/login/",
        data={"username": "username_test", "password": "qwerty123"}
    )
    assert response.status_code == 200
    data_json = response.json()
    assert "access_token" in data_json and "token_type" in data_json

    # incorrect user data
    response = client.post(
        url="/auth/login/",
        data={"username": "username_test", "password": "123"}
    )
    assert response.status_code == 401
    data_json = response.json()
    assert data_json['detail'] == 'Invalid credentials'
    assert response.headers['WWW-Authenticate'] == "Bearer"


def test_about_me(overrides_get_db):
    response = client.post(
        url="/auth/login/",
        data={"username": "username_test", "password": "qwerty123"}
    )
    jwt = response.json()['access_token']

    headers = {"Authorization": f"Bearer {jwt}"}
    response = client.get(
        url="/auth/about_me/",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()['username'] == "username_test"