import datetime

import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy import insert, select

from src.auth.models import historical_events
from src.calendar.functions import get_historical_event_by_id
from tests.conftest import async_session_maker


@pytest.mark.run(order=28)
async def test_add_historical_events():
    async with async_session_maker() as session:
        historical_events_data = [
            {"id": 1, "name": "Великая французская революция", "event_date": datetime.date(1111, 7, 14),
             "event_description": "test event_description 1"},
            {"id": 2, "name": "Основание Парижа римлянами", "event_date": datetime.date(1112, 7, 14),
             "event_description": "test event_description 2"},
            {"id": 3, "name": "Осада Парижа", "event_date": datetime.date(1113, 7, 14),
             "event_description": "test event_description 3"},
            {"id": 4, "name": "Постройка Эйфелевой башни", "event_date": datetime.date(1114, 7, 14),
             "event_description": "test event_description 4"},
            {"id": 5, "name": "Взятие Парижа во время Столетней войны", "event_date": datetime.date(1115, 7, 14),
             "event_description": "test event_description 5"},
            {"id": 6, "name": "Революция 1830 года в Париже", "event_date": datetime.date(1116, 7, 14),
             "event_description": "test event_description 6"},
            {"id": 7, "name": "Парижская коммуна", "event_date": datetime.date(1117, 7, 14),
             "event_description": "test event_description 7"},
            {"id": 8, "name": "Строительство Лувра", "event_date": datetime.date(1118, 7, 14),
             "event_description": "test event_description 8"},
            {"id": 9, "name": "Первый международный фестиваль кино в Париже", "event_date": datetime.date(1119, 7, 14),
             "event_description": "test event_description 9"},
            {"id": 10, "name": "Битва при Турской площади", "event_date": datetime.date(1110, 7, 14),
             "event_description": "test event_description 10"},
            {"id": 11, "name": "Освобождение Парижа во время Второй мировой войны",
             "event_date": datetime.date(1111, 7, 14),
             "event_description": "test event_description 11"},
        ]

        for data in historical_events_data:
            stmt = insert(historical_events).values(**data)
            await session.execute(stmt)
        await session.commit()

        query = select(historical_events)
        result = await session.execute(query)
        historical_events_records = result.all()

        assert len(historical_events_records) == 11, "Неверное количество вопросов добавлено"


@pytest.mark.run(order=29)
async def test_short_events(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    response = await ac.get("/calendar/events", headers={
        "Authorization": response_data["access_token"]
    })

    assert response.status_code == 200


@pytest.mark.run(order=30)
async def test_event_by_id(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    access_token = response_data["access_token"]
    event_id = 2

    response = await ac.get(f"/calendar/events/{event_id}", headers={
        "Authorization": access_token
    })

    assert response.status_code == 200
