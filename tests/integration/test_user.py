from uuid import uuid4
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    unique_id = uuid4().hex[:8]

    response = client.post("/users/", json={
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == f"testuser_{unique_id}"
    assert data["email"] == f"testuser_{unique_id}@example.com"
    assert "password_hash" not in data
    assert "id" in data
    assert "created_at" in data