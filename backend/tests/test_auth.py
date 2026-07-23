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


def test_logs_in_a_registered_user_and_returns_a_bearer_token(client: TestClient) -> None:
    payload = {"email": "buyer@example.com", "password": "secure-password-123"}
    client.post("/api/auth/register", json=payload)

    response = client.post("/api/auth/login", json=payload)

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_rejects_login_with_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": "buyer@example.com", "password": "incorrect-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
