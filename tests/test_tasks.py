import pytest


@pytest.fixture
def student_user(client):
    client.post(
        "/auth/register",
        json={
            "name": "Test Student",
            "email": "student-test@example.com",
            "phone": "9876543211",
            "password": "TestStudent@123"
        }
    )

    login = client.post(
        "/auth/login",
        json={
            "email": "student-test@example.com",
            "password": "TestStudent@123"
        }
    )

    assert login.status_code == 200

    token = login.json()["access_token"]
    me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    return {
        "id": me.json()["id"],
        "token": token
    }


def create_task(client, teacher_token, user_id):
    return client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "title": "Complete Python Assignment",
            "description": "Finish the API assignment",
            "status": "pending",
            "user_id": user_id
        }
    )


def test_student_can_view_own_tasks(client, teacher_token, student_user):
    created = create_task(client, teacher_token, student_user["id"])
    assert created.status_code == 201

    response = client.get(
        "/tasks/my",
        headers={"Authorization": f"Bearer {student_user['token']}"}
    )

    assert response.status_code == 200
    assert any(task["id"] == created.json()["id"] for task in response.json())


def test_student_can_update_own_task(client, teacher_token, student_user):
    created = create_task(client, teacher_token, student_user["id"])
    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}/work",
        headers={"Authorization": f"Bearer {student_user['token']}"},
        json={
            "status": "in_progress",
            "work_note": "Assignment started"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_student_cannot_create_task(client, student_user):
    response = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {student_user['token']}"},
        json={
            "title": "Unauthorized task",
            "description": "Should not be created",
            "status": "pending",
            "user_id": student_user["id"]
        }
    )

    assert response.status_code == 403


def test_student_cannot_delete_own_task(client, teacher_token, student_user):
    created = create_task(client, teacher_token, student_user["id"])
    task_id = created.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {student_user['token']}"}
    )

    assert response.status_code == 403


def test_student_cannot_access_another_students_task(
    client, teacher_token, student_user
):
    client.post(
        "/auth/register",
        json={
            "name": "Another Student",
            "email": "another-student@example.com",
            "phone": "9876543212",
            "password": "AnotherStudent@123"
        }
    )

    other_login = client.post(
        "/auth/login",
        json={
            "email": "another-student@example.com",
            "password": "AnotherStudent@123"
        }
    )

    other_token = other_login.json()["access_token"]

    other_me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {other_token}"}
    )

    created = create_task(client, teacher_token, other_me.json()["id"])
    task_id = created.json()["id"]

    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {student_user['token']}"}
    )

    assert response.status_code == 403

def test_teacher_can_update_and_delete_task(client, teacher_token, student_user):
    created = create_task(client, teacher_token, student_user["id"])
    assert created.status_code == 201

    task_id = created.json()["id"]
    headers = {"Authorization": f"Bearer {teacher_token}"}

    updated = client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={
            "title": "Updated Assignment",
            "description": "Updated by teacher",
            "status": "pending",
            "user_id": student_user["id"]
        }
    )

    assert updated.status_code == 200
    assert updated.json()["title"] == "Updated Assignment"

    deleted = client.delete(
        f"/tasks/{task_id}",
        headers=headers
    )

    assert deleted.status_code == 200
def test_student_cannot_update_another_students_task(
    client, teacher_token, student_user
):
    client.post(
        "/auth/register",
        json={
            "name": "Another Student",
            "email": "another-student@example.com",
            "phone": "9876543212",
            "password": "AnotherStudent@123"
        }
    )

    other_login = client.post(
        "/auth/login",
        json={
            "email": "another-student@example.com",
            "password": "AnotherStudent@123"
        }
    )

    other_token = other_login.json()["access_token"]

    other_me = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {other_token}"}
    )

    created = create_task(client, teacher_token, other_me.json()["id"])

    response = client.patch(
        f"/tasks/{created.json()['id']}/work",
        headers={"Authorization": f"Bearer {student_user['token']}"},
        json={
            "status": "done",
            "work_note": "Unauthorized update"
        }
    )

    assert response.status_code == 404


def test_teacher_cannot_assign_task_to_invalid_student(
    client, teacher_token
):
    response = client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {teacher_token}"},
        json={
            "title": "Invalid Assignment",
            "description": "Testing invalid student",
            "status": "pending",
            "user_id": 99999
        }
    )

    assert response.status_code == 404
