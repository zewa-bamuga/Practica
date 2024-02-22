from httpx import AsyncClient
from sqlalchemy import insert, select
from src.auth.models import role, password_reset_code
from tests.conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], "Роль не добавилась"


def test_register():
    response = client.post("/authentication/registration", json={
        "email": "user@example.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })

    assert response.status_code == 201


async def test_authenticate_user():
    response = client.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "Password123!"
    })

    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"


async def test_invalid_authentication():
    auth_data = {
        "email": "nonexistent_user@example.com",
        "password": "invalid_password"
    }
    response = client.post("/authentication/authentification", json=auth_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Неверное имя пользователя или пароль"


async def test_password_reset_request(ac: AsyncClient):
    response = await ac.post("/authentication/password/reset/request", json={
        "email": "user@example.com"
    })
    assert response.status_code == 200


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
