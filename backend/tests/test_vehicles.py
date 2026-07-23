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


def authorization_header(database, role: str = "user") -> dict[str, str]:
    user_id = database.users.insert_one(
        {"email": f"{role}@example.com", "password_hash": "not-used", "role": role}
    ).inserted_id
    token = create_access_token(str(user_id), role)
    return {"Authorization": f"Bearer {token}"}


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
    response = client.post(
        "/api/vehicles",
        headers=authorization_header(database),
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


def test_lists_all_vehicles_for_an_authenticated_user(database, client: TestClient) -> None:
    database.vehicles.insert_many(
        [
            {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 4},
            {"make": "Honda", "model": "CR-V", "category": "SUV", "price": 35000, "quantity": 0},
        ]
    )

    response = client.get("/api/vehicles", headers=authorization_header(database))

    assert response.status_code == 200
    assert [vehicle["model"] for vehicle in response.json()] == ["Camry", "CR-V"]


@pytest.mark.parametrize(
    ("query", "expected_models"),
    [
        ("make=Toyota", ["Camry", "RAV4"]),
        ("model=Civic", ["Civic"]),
        ("category=SUV", ["RAV4"]),
        ("min_price=25000&max_price=30000", ["Camry"]),
    ],
)
def test_searches_vehicles_by_supported_filters(
    database, client: TestClient, query: str, expected_models: list[str]
) -> None:
    database.vehicles.insert_many(
        [
            {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 4},
            {"make": "Toyota", "model": "RAV4", "category": "SUV", "price": 38000, "quantity": 3},
            {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 24000, "quantity": 2},
        ]
    )

    response = client.get(f"/api/vehicles/search?{query}", headers=authorization_header(database))

    assert response.status_code == 200
    assert [vehicle["model"] for vehicle in response.json()] == expected_models


def test_updates_a_vehicle_for_an_authenticated_user(database, client: TestClient) -> None:
    vehicle_id = database.vehicles.insert_one(
        {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 4}
    ).inserted_id

    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        headers=authorization_header(database),
        json={"price": 29500, "quantity": 3},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(vehicle_id),
        "make": "Toyota",
        "model": "Camry",
        "category": "Sedan",
        "price": 29500.0,
        "quantity": 3,
    }


def test_rejects_vehicle_deletion_for_a_regular_user(database, client: TestClient) -> None:
    vehicle_id = database.vehicles.insert_one(
        {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 4}
    ).inserted_id

    response = client.delete(f"/api/vehicles/{vehicle_id}", headers=authorization_header(database))

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


def test_deletes_a_vehicle_for_an_admin(database, client: TestClient) -> None:
    vehicle_id = database.vehicles.insert_one(
        {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28000, "quantity": 4}
    ).inserted_id

    response = client.delete(
        f"/api/vehicles/{vehicle_id}", headers=authorization_header(database, role="admin")
    )

    assert response.status_code == 204
    assert database.vehicles.find_one({"_id": vehicle_id}) is None
