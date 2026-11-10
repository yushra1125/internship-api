def test_create_user(client, teacher_token):
    response = client.post(
        "/users",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test User"


def test_invalid_email(client, teacher_token):
    response = client.post(
        "/users",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "name": "Test User",
            "email": "invalidemail",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False


def test_user_not_found(client, teacher_token):
    response = client.get(
        "/users/999999",
        headers={"Authorization": f"Bearer {teacher_token}"}
    )

    assert response.status_code == 404
    assert response.json()["success"] is False


def test_missing_email(client, teacher_token):
    response = client.post(
        "/users",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "name": "Test User",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False


def test_wrong_phone_type(client, teacher_token):
    response = client.post(
        "/users",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "name": "Test User",
            "email": "testuser@gmail.com",
            "phone": 9876543210
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False


def test_name_too_long(client, teacher_token):
    response = client.post(
        "/users",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "name": "A" * 51,
            "email": "testuser@gmail.com",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 422
    assert response.json()["success"] is False
def test_student_can_update_own_profile(client, student_token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "name": "Updated Student",
            "phone": "9123456789"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Student"
    assert response.json()["phone"] == "9123456789"


def test_student_cannot_use_duplicate_email(client, student_token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"email": "teacher-test@example.com"}
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_teacher_cannot_use_student_profile_endpoint(client, teacher_token):
    response = client.patch(
        "/users/me",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={"name": "Updated Teacher"}
    )

    assert response.status_code == 403
