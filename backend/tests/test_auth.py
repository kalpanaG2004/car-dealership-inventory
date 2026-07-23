import mongomock
import pytest
from fastapi.testclient import TestClient

from app.database import get_database
from app.main import app


@pytest.fixture
def client() -> TestClient:
    database = mongomock.MongoClient().car_dealership_inventory_test
    app.dependency_overrides[get_database] = lambda: database

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_registers_a_new_user(client: TestClient) -> None:
    response = client.post(
        "/api/auth/register",
        json={
            "email": "buyer@example.com",
            "password": "secure-password-123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "buyer@example.com"
    assert response.json()["role"] == "user"
    assert "id" in response.json()
    assert "password" not in response.json()


def test_rejects_registration_with_an_existing_email(client: TestClient) -> None:
    payload = {"email": "buyer@example.com", "password": "secure-password-123"}
    client.post("/api/auth/register", json=payload)

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "An account with this email already exists"
