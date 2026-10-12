import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_dashboard_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_products_page_loads(client):
    response = client.get("/products")

    assert response.status_code == 200


def test_add_product_page_loads(client):
    response = client.get("/products/add")

    assert response.status_code == 200


def test_product_can_be_added(client):
    response = client.post(
        "/products/add",
        data={
            "name": "Test Laptop",
            "category": "Electronics",
            "price": "50000",
            "quantity": "10",
            "threshold": "5"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Test Laptop" in response.data