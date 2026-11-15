import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError

from pydantic import ValidationError

from app.api.task_routes import get_task_service
from app.model.tasks import TasjOut, TaskGreate, TaskReplace, taskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskService


def asgi_request(app, method: str, target: str, payload: dict | None = None):
    """Send one JSON request to an ASGI app without external test packages."""
    body = json.dumps(payload).encode("utf-8") if payload is not None else b""
    path, _, query = target.partition("?")
    sent_request = False
    messages: list[dict] = []

    async def receive() -> dict:
        nonlocal sent_request
        if not sent_request:
            sent_request = True
            return {"type": "http.request", "body": body, "more_body": False}
        return {"type": "http.disconnect"}

    async def send(message: dict) -> None:
        messages.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode("ascii"),
        "query_string": query.encode("ascii"),
        "root_path": "",
        "headers": [
            (b"host", b"testserver"),
            (b"content-type", b"application/json"),
        ],
        "client": ("testclient", 123),
        "server": ("testserver", 80),
    }
    asyncio.run(app(scope, receive, send))
    start = next(message for message in messages if message["type"] == "http.response.start")
    response_body = b"".join(
        message.get("body", b"")
        for message in messages
        if message["type"] == "http.response.body"
    )
    decoded = json.loads(response_body) if response_body else None
    return start["status"], decoded


class CoreApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "tasks.db"

    def tearDown(self) -> None:
        from app.main import app

        app.dependency_overrides.clear()
        self.temp_dir.cleanup()

    def test_http_crud_statuses_and_route_mount(self) -> None:
        from app.main import app

        service = TaskService(
            repository=TaskRepository(self.database_path),
            priority_advisor=PriorityAdvisor(),
        )
        app.dependency_overrides[get_task_service] = lambda: service

        status_code, created = asgi_request(
            app,
            "POST",
            "/tasks",
            {"title": "Review release", "description": None, "completed": False},
        )
        self.assertEqual(status_code, 201)
        task_id = created["id"]

        status_code, items = asgi_request(app, "GET", "/tasks")
        self.assertEqual(status_code, 200)
        self.assertEqual(len(items), 1)

        status_code, item = asgi_request(app, "GET", f"/tasks/{task_id}")
        self.assertEqual(status_code, 200)
        self.assertEqual(item["id"], task_id)

        status_code, updated = asgi_request(
            app,
            "PUT",
            f"/tasks/{task_id}",
            {"title": "Release reviewed", "description": "Ready", "completed": True},
        )
        self.assertEqual(status_code, 200)
        self.assertTrue(updated["completed"])

        status_code, body = asgi_request(app, "DELETE", f"/tasks/{task_id}")
        self.assertEqual(status_code, 204)
        self.assertIsNone(body)

        status_code, _ = asgi_request(app, "GET", f"/tasks/{task_id}")
        self.assertEqual(status_code, 404)
        status_code, _ = asgi_request(app, "GET", "/tasks/not-a-uuid")
        self.assertEqual(status_code, 422)
        status_code, _ = asgi_request(app, "GET", "/tasks?limit=101")
        self.assertEqual(status_code, 422)
        status_code, _ = asgi_request(app, "GET", "/tasks?offset=-1")
        self.assertEqual(status_code, 422)

    def test_model_validation_and_update_semantics(self) -> None:
        self.assertEqual(TaskGreate(title="  Fix incident  ").title, "Fix incident")
        with self.assertRaises(ValidationError):
            TaskGreate(title="   ")
        with self.assertRaises(ValidationError):
            TaskGreate(title="x" * 201)
        with self.assertRaises(ValidationError):
            TaskGreate(title="Valid", description="x" * 2001)
        with self.assertRaises(ValidationError):
            TaskReplace(title="Replacement", completed=True)
        with self.assertRaises(ValidationError):
            taskUpdate()
        with self.assertRaises(ValidationError):
            taskUpdate(title=None)
        with self.assertRaises(ValidationError):
            taskUpdate(completed=None)
        self.assertIsNone(taskUpdate(description=None).description)

    def test_sqlite_persistence_pagination_and_memory_database(self) -> None:
        repository = TaskRepository(self.database_path)
        for index in range(5):
            repository.create(TaskGreate(title=f"Task {index}"))

        reopened_repository = TaskRepository(self.database_path)
        self.assertEqual(len(reopened_repository.list()), 5)
        self.assertEqual(len(reopened_repository.list(limit=2, offset=1)), 2)

        memory_repository = TaskRepository(":memory:")
        memory_repository.create(TaskGreate(title="In memory test"))
        self.assertEqual(len(memory_repository.list()), 1)

    def test_local_advisor_does_not_make_network_calls_without_key(self) -> None:
        task = TasjOut(title="Incidente urgente", completed=False)
        with patch.dict(os.environ, {"OPENAI_API_KEY": "", "OPEAN_API_KEY": ""}, clear=True):
            with patch(
                "app.services.priority_advisor.urlopen",
                side_effect=AssertionError("network call should not happen"),
            ):
                suggestion = PriorityAdvisor().suggest_priority(task)
        self.assertEqual(suggestion.priority, "alta")

    def test_llm_advisor_uses_structured_output_and_falls_back_on_failure(self) -> None:
        task = TasjOut(title="Routine documentation", completed=False)
        api_response = {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps(
                                {"priority": "baixa", "justification": "Pode aguardar."}
                            ),
                        }
                    ],
                }
            ]
        }
        response_context = MagicMock()
        response_context.__enter__.return_value = response_context
        response_context.read.return_value = json.dumps(api_response).encode("utf-8")

        with patch.dict(os.environ, {"OPEAN_API_KEY": "test-key"}, clear=True):
            with patch(
                "app.services.priority_advisor.urlopen",
                return_value=response_context,
            ) as open_url:
                suggestion = PriorityAdvisor().suggest_priority(task)
            self.assertEqual(suggestion.priority, "baixa")
            self.assertEqual(open_url.call_args.kwargs["timeout"], 5)
            request = open_url.call_args.args[0]
            payload = json.loads(request.data.decode("utf-8"))
            self.assertEqual(payload["text"]["format"]["type"], "json_schema")
            self.assertTrue(payload["text"]["format"]["strict"])

            with patch(
                "app.services.priority_advisor.urlopen",
                side_effect=URLError("simulated outage"),
            ):
                fallback = PriorityAdvisor().suggest_priority(task)
        self.assertEqual(fallback.priority, "media")


if __name__ == "__main__":
    unittest.main()
