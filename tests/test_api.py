import pytest
from fastapi.testclient import TestClient

from orderlab.api import create_app


@pytest.fixture
def client():
    with TestClient(create_app()) as client:
        yield client


def test_create_and_read_order(client):
    order = {"price": 3_200, "quantity": 3}
    expected = {"id": 1, "subtotal": 9_600}

    created = client.post("/orders", json=order)
    assert created.status_code == 201
    assert created.json() == expected

    saved = client.get("/orders/1")
    assert saved.status_code == 200
    assert saved.json() == expected


def test_read_order_from_empty_store(client):
    response = client.get("/orders/1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


@pytest.mark.parametrize(
    "order, invalid_field",
    [
        ({"price": -500, "quantity": 2}, "price"),
        ({"price": 4_700, "quantity": 0}, "quantity"),
    ],
)
def test_invalid_order(client, order, invalid_field):
    response = client.post("/orders", json=order)

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", invalid_field]
