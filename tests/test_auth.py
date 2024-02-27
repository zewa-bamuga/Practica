import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from src.auth.jwt import verify_jwt_token
from src.auth.models import role, password_reset_code
from src.auth.schemas import UserBase
from tests.conftest import client, async_session_maker


@pytest.mark.run(order=1)
async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="user", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'user', None)], "Роль не добавилась"


@pytest.mark.run(order=2)
def test_register():
    response = client.post("/authentication/registration", json={
        "email": "user@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })

    assert response.status_code == 201

@pytest.mark.run(order=2)
def test_register_email_already():
    response = client.post("/authentication/registration", json={
        "email": "user@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })

    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Пользователь с этой электронной почтой уже существует!"

@pytest.mark.run(order=3)
def test_register_password_mismatch():
    response = client.post("/authentication/registration", json={
        "email": "user@example.com",
        "password": "Password123!",
        "confirm_password": "assword123!"
    })

    assert response.status_code == 422


@pytest.mark.run(order=4)
def test_register_password_сonditions_violated():
    response = client.post("/authentication/registration", json={
        "email": "user@example.com",
        "password": "Password",
        "confirm_password": "Password"
    })

    assert response.status_code == 422


@pytest.mark.run(order=5)
async def test_password_reset_request(ac: AsyncClient):
    response = await ac.post("/authentication/password/reset/request", json={
        "email": "user@example.com"
    })
    assert response.status_code == 200


@pytest.mark.run(order=6)
async def test_password_reset_confirm(ac: AsyncClient):
    async with async_session_maker() as session:
        query = select(password_reset_code).filter_by(id=1)
        result = await session.execute(query)
        added_code = result.fetchall()

        assert added_code, "Код не найден в базе данных"

        added_code = added_code[0][2]

        response = await ac.post("/authentication/password/reset/confirm", json={
            "email": "user@example.com",
            "code": added_code,
            "new_password": "looooooool1"
        })

        assert response.status_code == 200


@pytest.mark.run(order=7)
async def test_authenticate_user(ac: AsyncClient):
    response_get = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "looooooool1"
    })

    assert response_get.status_code == 200

    response_data = response_get.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.run(order=8)
async def test_invalid_email_validation(ac: AsyncClient):
    response = await ac.post("/authentication/authentification", json={
        "email": "#tikhonov.igor2028@yandex.ru",
        "password": "looooooool1"
    })

    assert response.status_code == 422

    response_json = response.json()
    assert any(detail['msg'] == 'Value error, Введены неверные значения' for detail in response_json['detail'])


@pytest.mark.run(order=9)
async def test_invalid_authentication():
    auth_data = {
        "email": "nonexistent_user@example.com",
        "password": "invalid_password"
    }
    response = client.post("/authentication/authentification", json=auth_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Неверное имя пользователя или пароль"


@pytest.mark.run(order=10)
async def test_invalid_authentication2():
    auth_data = {
        "email": "user@example.com",
        "password": "testtttttt"
    }
    response = client.post("/authentication/authentification", json=auth_data)
    assert response.status_code == 422
    error_msg = response.json()["detail"][0]["msg"]
    assert "Пароль должен содержать по крайней мере одну букву и одну цифру или специальный символ" in error_msg
