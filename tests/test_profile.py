import pytest
from httpx import AsyncClient

from tests.conftest import client


@pytest.mark.run(order=14)
async def test_get_me(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "looooooool1"
    })

    response_data = response_auth.json()

    response = await ac.get("/profile/get-me", headers={
        "Authorization": response_data["access_token"]
    })

    assert response.status_code == 200
    assert response.json().get("email") == "user@example.com"


# Хоть всё работает, но покрытие не делается
@pytest.mark.run(order=15)
async def test_fail_change_password(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "looooooool1"
    })

    response_data = response_auth.json()

    response = await ac.post("/profile/change-password", headers={
        "Authorization": response_data["access_token"]
    }, json={
        "old_password": "sddbebet3",
        "new_password": "!ntrntr43"
    })

    assert response.status_code == 400

    response_data = response.json()
    assert response_data["detail"] == "Неправильный старый пароль"


@pytest.mark.run(order=16)
async def test_change_password(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "looooooool1"
    })

    response_data = response_auth.json()

    response = await ac.post("/profile/change-password", headers={
        "Authorization": response_data["access_token"]
    }, json={
        "old_password": "looooooool1",
        "new_password": "!321Password"
    })

    assert response.status_code == 200


@pytest.mark.run(order=17)
async def test_leave_feedback(ac: AsyncClient):
    response_auth = await ac.post("/authentication/authentification", json={
        "email": "user@example.com",
        "password": "!321Password"
    })

    response_data = response_auth.json()

    response = await ac.post("/profile/leave-feedback", headers={
        "Authorization": response_data["access_token"]
    }, json={
        "text": "test leave_feedback",
        "deviceName": "DESKTOP-769RBJ3",
        "osVersion": "Windows 10",
        "appVersion": "1.0.0"
    })

    assert response.status_code == 200

    feedback_data = response.json()
    assert "text" in feedback_data
    assert feedback_data["text"] == "test leave_feedback"


@pytest.mark.run(order=18)
async def test_leave_feedback_Unauthorized(ac: AsyncClient):
    response_Unauthorized = await ac.post("/profile/leave-feedback", headers={
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0aWtob25vdi5pZ29yMjAyOEB5YW5kZXgucnUiLCJleHAiOjE3MDg4NzcxODN9.uYiiWzWaup0cIO2N5yy0GiF5LZdhfpC67JDyeU7eReY"},
                                          json={
                                              "text": "test leave_feedback",
                                              "deviceName": "DESKTOP-769RBJ3",
                                              "osVersion": "Windows 10",
                                              "appVersion": "1.0.0"
                                          })

    assert response_Unauthorized.status_code == 401
    response_data = response_Unauthorized.json()
    assert response_data["detail"] == "Неверный токен или истек срок действия"


@pytest.mark.run(order=19)
async def test_leave_feedback_un():
    response_un = client.post("/profile/leave-feedback",
                                json={
                                    "text": "test leave_feedback",
                                    "deviceName": "DESKTOP-769RBJ3",
                                    "osVersion": "Windows 10",
                                    "appVersion": "1.0.0"
                                })

    assert response_un.status_code == 403
    response_data = response_un.json()
    assert response_data["detail"] == "Not authenticated"
