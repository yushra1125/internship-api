import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.session import UserSession
from app.models.task import Task
from app.security import hash_password


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()
    teacher = User(
        name="Test Teacher",
        email="teacher-test@example.com",
        phone="9876543210",
        password_hash=hash_password("TestTeacher@123"),
        role="teacher",
        status="active",
    )
    db.add(teacher)
    db.commit()
    db.close()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def teacher_token(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "teacher-test@example.com",
            "password": "TestTeacher@123",
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]
