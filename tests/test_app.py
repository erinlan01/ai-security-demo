import sqlite3

import pytest

from app import app, open_catalog


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_index_warns_against_deployment(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Do not deploy" in response.get_json()["warning"]


def test_catalog_returns_only_synthetic_records(client):
    response = client.get("/catalog")
    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "name": "Paper Moon", "category": "books"},
        {"id": 2, "name": "Cloud Atlas Puzzle", "category": "games"},
        {"id": 3, "name": "The Imaginary Garden", "category": "books"},
    ]


@pytest.mark.parametrize(
    ("category", "expected_ids"),
    [("books", [1, 3]), ("games", [2]), ("unknown", []), ("", [1, 2, 3])],
)
def test_benign_category_filter(client, category, expected_ids):
    response = client.get("/catalog", query_string={"category": category})
    assert response.status_code == 200
    assert [row["id"] for row in response.get_json()] == expected_ids


def test_catalog_is_read_only_after_seeding():
    connection = open_catalog()
    try:
        assert connection.execute("PRAGMA query_only").fetchone()[0] == 1
        with pytest.raises(sqlite3.OperationalError, match="readonly"):
            connection.execute("DELETE FROM catalog")
    finally:
        connection.close()


def test_requests_do_not_change_the_catalog(client):
    before = client.get("/catalog").get_json()
    client.get("/catalog", query_string={"category": "books"})
    assert client.get("/catalog").get_json() == before
