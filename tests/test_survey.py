import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from src.auth.models import survey
from tests.conftest import async_session_maker


@pytest.mark.run(order=11)
async def test_add_survey():
    async with async_session_maker() as session:
        survey_data = [
            {"id": 1, "category": "Литература и поэзия"},
            {"id": 2, "category": "Кинематограф"},
            {"id": 3, "category": "Мода"},
            {"id": 4, "category": "Прогулки под луной"},
            {"id": 5, "category": "Музыка"},
            {"id": 6, "category": "Живопись и архитектура"},
            {"id": 7, "category": "Детективы"},
            {"id": 8, "category": "Наука"},
            {"id": 9, "category": "История"},
            {"id": 10, "category": "Войны"},
        ]

        for data in survey_data:
            stmt = insert(survey).values(**data)
            await session.execute(stmt)
        await session.commit()

        query = select(survey)
        result = await session.execute(query)
        survey_records = result.all()

        assert len(survey_records) == 10, "Неверное количество опросов добавлено"
        for data, record in zip(survey_data, survey_records):
            assert record == (data["id"], data["category"]), f"Ошибка в записи опроса {data['id']}"


@pytest.mark.run(order=12)
async def test_question_handler(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "looooooool1"
    })

    response_data = response_auth.json()

    response = await ac.get("/survey/questions", headers={
        "Authorization": response_data["access_token"]
    })

    assert response.status_code == 200

    assert response.headers["Content-Type"] == "application/json"

    questions = response.json()
    assert len(questions) == 10


@pytest.mark.run(order=13)
async def test_submit_survey_response(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "looooooool1"
    })

    response_data = response_auth.json()

    response = await ac.post("/survey/submit-response", headers={
        "Authorization": response_data["access_token"]
    }, json={
        "survey_id": [
            1, 5, 7
        ]
    })

    assert response.status_code == 200
