import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from src.auth.models import question
from tests.conftest import async_session_maker


@pytest.mark.run(order=20)
async def test_add_questions():
    async with async_session_maker() as session:
        question_data = [
            {"id": 1, "title": "Хемингуэй", "description": "test all_description 1",
             "short_description": "test short_description 1",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\1.jpg",
             "points": 1, "distance": 10, "time": 10, "price": 0,
             "survey_id": 1},
            {"id": 2, "title": "Три мушкетера", "description": "test all_description 2",
             "short_description": "test short_description 2",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\2.jpg",
             "points": 2, "distance": 20, "time": 10, "price": 0,
             "survey_id": 1},
            {"id": 3, "title": "Русские писатели в Париже", "description": "test all_description 3",
             "short_description": "test short_description 3",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\3.jpg",
             "points": 3, "distance": 30, "time": 10, "price": 0,
             "survey_id": 1},
            {"id": 4, "title": "Париж в стихах", "description": "test all_description 4",
             "short_description": "test short_description 4",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\4.jpg",
             "points": 4, "distance": 40, "time": 10, "price": 0,
             "survey_id": 1},
            {"id": 5, "title": "Париж «»Кода да Винчи", "description": "test all_description 5",
             "short_description": "test short_description 5",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\5.jpg",
             "points": 5, "distance": 50, "time": 10, "price": 0,
             "survey_id": 1},
            {"id": 6, "title": "Россия (Наши в городе)", "description": "test all_description 6",
             "short_description": "test short_description 6",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\6.jpg",
             "points": 6, "distance": 60, "time": 10, "price": 0,
             "survey_id": 1},
            {"id": 7, "title": "Камера, мотор! Париж кинофильмов", "description": "test all_description 7",
             "short_description": "test short_description 7",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\7.jpg",
             "points": 7, "distance": 70, "time": 10, "price": 0,
             "survey_id": 2},
            {"id": 8, "title": "Прогулка с Амели", "description": "test all_description 8",
             "short_description": "test short_description 8",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\8.jpg",
             "points": 8, "distance": 80, "time": 10, "price": 0,
             "survey_id": 2},
            {"id": 9, "title": "Париж актеров", "description": "test all_description 9",
             "short_description": "test short_description 9",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\9.jpg",
             "points": 9, "distance": 90, "time": 10, "price": 0,
             "survey_id": 2},
            {"id": 10, "title": "Париж «»Кода да Винчи", "description": "test all_description 10",
             "short_description": "test short_description 10",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\10.jpg",
             "points": 10, "distance": 100, "time": 10, "price": 0,
             "survey_id": 2},
            {"id": 11, "title": "Россия (Наши в городе)", "description": "test all_description 11",
             "short_description": "test short_description 11",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\11.jpg",
             "points": 11, "distance": 110, "time": 10, "price": 0,
             "survey_id": 2},
            {"id": 12, "title": "Модный Париж", "description": "test all_description 12",
             "short_description": "test short_description 12",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\12.jpg",
             "points": 12, "distance": 210, "time": 10, "price": 0,
             "survey_id": 3},
            {"id": 13, "title": "Полночь в Париже", "description": "test all_description 13",
             "short_description": "test short_description 13",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\13.jpg",
             "points": 13, "distance": 310, "time": 10, "price": 0,
             "survey_id": 4},
            {"id": 14, "title": "Пикантный Париж 18+", "description": "test all_description 14",
             "short_description": "test short_description 14",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\14.jpg",
             "points": 14, "distance": 310, "time": 10, "price": 0,
             "survey_id": 4},
            {"id": 15, "title": "Россия (Наши в городе)", "description": "test all_description 15",
             "short_description": "test short_description 15",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\15.jpg",
             "points": 15, "distance": 410, "time": 10, "price": 0,
             "survey_id": 5},
            {"id": 16, "title": "Париж музыкальный", "description": "test all_description 16",
             "short_description": "test short_description 16",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\16.jpg",
             "points": 16, "distance": 510, "time": 10, "price": 0,
             "survey_id": 5},
            {"id": 17, "title": "Париж художников", "description": "test all_description 17",
             "short_description": "test short_description 17",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\17.jpg",
             "points": 17, "distance": 610, "time": 10, "price": 0,
             "survey_id": 6},
            {"id": 18, "title": "Россия Eye candy", "description": "test all_description 18",
             "short_description": "test short_description 18",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\18.jpg",
             "points": 18, "distance": 710, "time": 10, "price": 0,
             "survey_id": 6},
            {"id": 19, "title": "Россия (Наши в городе)", "description": "test all_description 19",
             "short_description": "test short_description 19",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\19.jpg",
             "points": 19, "distance": 810, "time": 10, "price": 0,
             "survey_id": 6},
            {"id": 20, "title": "Париж шпионов", "description": "test all_description 20",
             "short_description": "test short_description 20",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\20.jpg",
             "points": 20, "distance": 910, "time": 10, "price": 0,
             "survey_id": 7},
            {"id": 21, "title": "Париж писателей", "description": "test all_description 21",
             "short_description": "test short_description 21",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\21.jpg",
             "points": 21, "distance": 1010, "time": 10, "price": 0,
             "survey_id": 7},
            {"id": 22, "title": "Париж преступников и преступлений", "description": "test all_description 22",
             "short_description": "test short_description 22",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\22.jpg",
             "points": 22, "distance": 1110, "time": 10, "price": 0,
             "survey_id": 7},
            {"id": 23, "title": "Париж научный", "description": "test all_description 23",
             "short_description": "test short_description 23",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\23.jpg",
             "points": 23, "distance": 1210, "time": 10, "price": 0,
             "survey_id": 8},
            {"id": 24, "title": "Россия (Наши в городе)", "description": "test all_description 24",
             "short_description": "test short_description 24",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\24.jpg",
             "points": 24, "distance": 1310, "time": 10, "price": 0,
             "survey_id": 8},
            {"id": 25, "title": "Ленин и Троцкий", "description": "test all_description 25",
             "short_description": "test short_description 25",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\25.jpg",
             "points": 25, "distance": 1410, "time": 10, "price": 0,
             "survey_id": 9},
            {"id": 26, "title": "Париж Петра Первого", "description": "test all_description 26",
             "short_description": "test short_description 26",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\26.jpg",
             "points": 26, "distance": 1510, "time": 10, "price": 0,
             "survey_id": 9},
            {"id": 27, "title": "Легенды Парижа", "description": "test all_description 27",
             "short_description": "test short_description 27",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\27.jpg",
             "points": 27, "distance": 1610, "time": 10, "price": 0,
             "survey_id": 9},
            {"id": 28, "title": "Париж Наполеона", "description": "test all_description 28",
             "short_description": "test short_description 28",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\28.jpg",
             "points": 28, "distance": 1710, "time": 10, "price": 0,
             "survey_id": 9},
            {"id": 29, "title": "Россия (Наши в городе)", "description": "test all_description 29",
             "short_description": "test short_description 29",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\29.jpg",
             "points": 29, "distance": 1810, "time": 10, "price": 0,
             "survey_id": 9},
            {"id": 30, "title": "Париж в оккупации", "description": "test all_description 30",
             "short_description": "test short_description 30",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\30.jpg",
             "points": 30, "distance": 1910, "time": 10, "price": 0,
             "survey_id": 10},
            {"id": 31, "title": "Париж Наполеона", "description": "test all_description 31",
             "short_description": "test short_description 31",
             "image_path": r"C:\Users\TikhonovIB\PycharmProjects\Practica\images\31.jpg",
             "points": 31, "distance": 2010, "time": 10, "price": 0,
             "survey_id": 10},
        ]

        for data in question_data:
            stmt = insert(question).values(**data)
            await session.execute(stmt)
        await session.commit()

        query = select(question)
        result = await session.execute(query)
        question_records = result.all()

        assert len(question_records) == 31, "Неверное количество вопросов добавлено"


@pytest.mark.run(order=21)
async def test_user_questions(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    response = await ac.get("/walk/user-questions", headers={
        "Authorization": response_data["access_token"]
    })

    assert response.status_code == 200

    assert response.headers["Content-Type"] == "application/json"

    questions = response.json()
    assert len(questions) == 10, "Неверное количество вопросов для пользователя"


@pytest.mark.run(order=22)
async def test_fail_question_by_id(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    access_token = response_data["access_token"]
    question_id = 100

    response = await ac.get(f"/walk/questions/{question_id}", headers={
        "Authorization": access_token
    })

    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Вы не выбрали категорию для этого запроса"

@pytest.mark.run(order=23)
async def test_question_by_id(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    access_token = response_data["access_token"]
    question_id = 2

    response = await ac.get(f"/walk/questions/{question_id}", headers={
        "Authorization": access_token
    })

    assert response.status_code == 200


@pytest.mark.run(order=24)
async def test_create_rating(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    response = await ac.post("/walk/route-rating", headers={
        "Authorization": response_data["access_token"]
    }, json={
        "question_id": 2,
        "rating": 4.5
    })

    assert response.status_code == 200


@pytest.mark.run(order=25)
async def test_add_to_favorites(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    response = await ac.post("/walk/add-to-favorites", headers={
        "Authorization": response_data["access_token"]
    }, json={
        "question_id": 2
    })

    assert response.status_code == 200

@pytest.mark.run(order=26)
async def test_fail_add_to_favorites(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    response = await ac.post("/walk/add-to-favorites", headers={
        "Authorization": response_data["access_token"]
    }, json={
        "question_id": 2
    })

    assert response.status_code == 400
    response_json = response.json()
    assert response_json["detail"] == "Прогулка уже добавлена в избранное"


@pytest.mark.run(order=26)
async def test_favorite(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    response = await ac.get("/walk/favorite-routes", headers={
        "Authorization": response_data["access_token"]
    })

    assert response.status_code == 200


@pytest.mark.run(order=27)
async def test_remove_from_favorites_route(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })
    assert response_auth.status_code == 200
    response_data = response_auth.json()
    access_token = response_data["access_token"]

    response_add_to_favorites = await ac.post("/walk/add-to-favorites", json={
        "question_id": 3
    }, headers={"Authorization": access_token})
    assert response_add_to_favorites.status_code == 200

    response_remove_from_favorites = await ac.delete(f"/walk/remove-from-favorites/{3}",
                                                     headers={"Authorization": access_token})
    assert response_remove_from_favorites.status_code == 200

    response_check_favorites = await ac.get("/walk/favorite-routes", headers={"Authorization": access_token})
    assert response_check_favorites.status_code == 200
    assert 3 not in response_check_favorites.json()
