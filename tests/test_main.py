import os
os.environ["TESTING"] = "1"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def signup_and_login(username="tester", password="testpass123"):
    """Helper: creates a user and returns an auth token for them."""
    client.post("/signup", json={"username": username, "password": password})
    response = client.post(
        "/login",
        data={"username": username, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_signup_and_login():
    headers = signup_and_login("alice", "alicepass123")
    assert "Authorization" in headers


def test_cannot_access_tasks_without_token():
    resp = client.get("/tasks")
    assert resp.status_code == 401


def test_create_and_list_task():
    headers = signup_and_login("bob", "bobpass123")

    resp = client.post("/tasks", json={"title": "Learn Docker"}, headers=headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Learn Docker"
    assert body["done"] is False

    resp = client.get("/tasks", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_users_cannot_see_each_others_tasks():
    headers_carol = signup_and_login("carol", "carolpass123")
    headers_dave = signup_and_login("dave", "davepass123")

    client.post("/tasks", json={"title": "Carol's task"}, headers=headers_carol)

    resp = client.get("/tasks", headers=headers_dave)
    assert resp.status_code == 200
    assert len(resp.json()) == 0


def test_update_task():
    headers = signup_and_login("erin", "erinpass123")
    create = client.post("/tasks", json={"title": "Learn Git"}, headers=headers)
    task_id = create.json()["id"]

    update = client.put(
        f"/tasks/{task_id}",
        json={"title": "Learn Git", "done": True},
        headers=headers,
    )
    assert update.status_code == 200
    assert update.json()["done"] is True


def test_delete_task():
    headers = signup_and_login("frank", "frankpass123")
    create = client.post("/tasks", json={"title": "Temp task"}, headers=headers)
    task_id = create.json()["id"]

    delete = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete.status_code == 204

    get_again = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_again.status_code == 404