from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.task_routes import get_task_service, router
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    """Provide an isolated API app and temporary SQLite repository."""
    app = FastAPI()
    app.include_router(router)

    service = TaskService(
        repository=TaskRepository(tmp_path / "route-tests.sqlite3"),
        priority_advisor=PriorityAdvisor(),
    )
    app.dependency_overrides[get_task_service] = lambda: service

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


def test_task_crud_returns_expected_success_status_codes(
    client: TestClient,
) -> None:
    created = client.post(
        "/tasks",
        json={"title": "Prepare release", "description": None, "completed": False},
    )
    assert created.status_code == 201
    task_id = created.json()["id"]

    listed = client.get("/tasks")
    assert listed.status_code == 200
    assert any(task["id"] == task_id for task in listed.json())

    retrieved = client.get(f"/tasks/{task_id}")
    assert retrieved.status_code == 200
    assert retrieved.json()["title"] == "Prepare release"

    updated = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Release prepared",
            "description": "Ready to ship",
            "completed": True,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Release prepared"
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 204
    assert deleted.content == b""


def test_missing_task_returns_404(client: TestClient) -> None:
    missing_id = "00000000-0000-0000-0000-000000000001"

    response = client.get(f"/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found."


def test_health_endpoint_returns_ok_and_utc_timestamp() -> None:
    """Expose the health check with a UTC timestamp."""
    from datetime import datetime, timedelta

    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    timestamp = datetime.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))
    assert timestamp.utcoffset() == timedelta(0)
