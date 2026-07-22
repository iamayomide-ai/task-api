from fastapi.testclient import TestClient
from app.main import app, tasks

client = TestClient(app)


def setup_function():
    """Reset in-memory data before each test."""
    tasks.clear()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_and_list_task():
    resp = client.post("/tasks", json={"title": "Learn Docker"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Learn Docker"
    assert body["done"] is False

    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_get_task_not_found():
    resp = client.get("/tasks/does-not-exist")
    assert resp.status_code == 404


def test_update_task():
    create = client.post("/tasks", json={"title": "Learn Git"})
    task_id = create.json()["id"]

    update = client.put(f"/tasks/{task_id}", json={"title": "Learn Git", "done": True})
    assert update.status_code == 200
    assert update.json()["done"] is True


def test_delete_task():
    create = client.post("/tasks", json={"title": "Temp task"})
    task_id = create.json()["id"]

    delete = client.delete(f"/tasks/{task_id}")
    assert delete.status_code == 204

    get_again = client.get(f"/tasks/{task_id}")
    assert get_again.status_code == 404
