from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test User"


def test_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "invalidemail",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False


def test_user_not_found():
    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["success"] is False
def test_missing_email():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False
def test_wrong_phone_type():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "phone": 9876543210
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False
def test_name_too_long():
    response = client.post(
        "/users",
        json={
            "name": "A" * 51,
            "email": "testuser@gmail.com",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False