from datetime import datetime, timedelta, timezone
import jwt
from app.security import SECRET_KEY, ALGORITHM
def test_login_success(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "teacher-test@example.com",
            "password": "TestTeacher@123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_wrong_password(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "teacher-test@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401


def test_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code in (401, 403)


def test_me_with_valid_token(client, teacher_token):
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )

    assert response.status_code == 200
    assert response.json()["role"] == "teacher"


def test_logout_revokes_access_token(client):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "teacher-test@example.com",
            "password": "TestTeacher@123"
        }
    )

    tokens = login_response.json()

    logout_response = client.post(
        "/auth/logout",
        json={"refresh_token": tokens["refresh_token"]}
    )

    assert logout_response.status_code == 200

    me_response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}"
        }
    )

    assert me_response.status_code == 401


def test_refresh_after_logout_fails(client):
    login_response = client.post(
        "/auth/login",
        json={
            "email": "teacher-test@example.com",
            "password": "TestTeacher@123"
        }
    )

    refresh_token = login_response.json()["refresh_token"]

    client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token}
    )

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )

    assert response.status_code == 401
def test_expired_access_token_rejected(client):
    expired_token = jwt.encode(
        {
            "sub": "1",
            "sid": 1,
            "type": "access",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    assert response.status_code == 401


def test_expired_refresh_token_rejected(client):
    expired_token = jwt.encode(
        {
            "sub": "1",
            "sid": 1,
            "type": "refresh",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": expired_token}
    )

    assert response.status_code == 401
