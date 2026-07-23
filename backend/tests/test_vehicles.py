import mongomock
import pytest
from fastapi.testclient import TestClient

from app.database import get_database
from app.main import app
from app.security import create_access_token


@pytest.fixture
def database():
    return mongomock.MongoClient().car_dealership_inventory_test


@pytest.fixture
def client(database) -> TestClient:
    app.dependency_overrides[get_database] = lambda: database

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_rejects_vehicle_creation_without_a_token(client: TestClient) -> None:
    response = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 28000,
            "quantity": 4,
        },
    )

    assert response.status_code == 401


def test_creates_a_vehicle_for_an_authenticated_user(database, client: TestClient) -> None:
    user_id = database.users.insert_one(
        {"email": "buyer@example.com", "password_hash": "not-used", "role": "user"}
    ).inserted_id
    token = create_access_token(str(user_id), "user")

    response = client.post(
        "/api/vehicles",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 28000,
            "quantity": 4,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": response.json()["id"],
        "make": "Toyota",
        "model": "Camry",
        "category": "Sedan",
        "price": 28000.0,
        "quantity": 4,
    }
