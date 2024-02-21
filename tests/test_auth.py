from sqlalchemy import insert, select

from src.auth.models import role
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
        "password": "stringst1", # тут вставил 1, потому что по валидации нужно хотя бы одну цифру
        "confirm_password": "stringst1"
    })

    assert response.status_code == 201