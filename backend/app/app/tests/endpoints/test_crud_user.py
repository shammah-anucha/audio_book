from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.app.db.base_class import Base
from backend.app.app.main import app
from backend.app.app.api.deps import get_db
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

user_db = {
    "email": "test@example.com",
    "Firstname": "John",
    "Lastname": "Doe",
    "country_of_residence": "USA",
    "password": "secretpassword",
}


def test_create_user():
    response = client.post("/api/v1/users/", json=user_db)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "user_id" in data


def test_read_user():
    user_id = 1  # Replace with the actual user ID you want to retrieve

    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["user_id"] == user_id


@pytest.mark.parametrize(
    "params, expected_length",
    [
        ("/api/v1/users/", None),  # No parameters, expect a list
        ("/api/v1/users/?skip=1&limit=5", 5),  # Skip and limit parameters
        (
            "/api/v1/users/?skip=-1&limit=0",
            0,
        ),  # Invalid parameters, expect an empty list
        (
            "/api/v1/users/?limit=1000",
            1000,
        ),  # Large limit, expect a list with length <= 1000
    ],
)
def test_read_users(params, expected_length):
    response = client.get(params)
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    if expected_length is not None:
        assert len(data) <= expected_length


@pytest.mark.parametrize(
    "user_id, status_code, detail",
    [
        (1, 200, "Delete Successful"),  # Valid user ID, expect successful deletion
        (999, 404, "User not found"),  # Invalid user ID, expect 404 error
    ],
)
def test_delete_user(user_id, status_code, detail):
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == status_code, response.text
    data = response.json()
    if status_code == 200:
        assert data == detail
    else:
        assert data["detail"] == detail
