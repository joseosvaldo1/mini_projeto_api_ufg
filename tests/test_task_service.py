from pathlib import Path
from uuid import UUID, uuid4

import pytest

from app.model.tasks import TaskGreate, taskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskNotFoundError, TaskService


@pytest.fixture
def task_service(tmp_path: Path) -> TaskService:
    """Provide a service backed by an isolated temporary SQLite database."""
    repository = TaskRepository(tmp_path / "tasks.sqlite3")
    return TaskService(
        repository=repository,
        priority_advisor=PriorityAdvisor(),
    )


def test_create_task_returns_and_persists_task(task_service: TaskService) -> None:
    created = task_service.create_task(TaskGreate(title="Prepare release"))

    assert isinstance(created.id, UUID)
    assert created.title == "Prepare release"
    assert created.completed is False
    assert task_service.get_task(created.id) == created


def test_list_tasks_returns_all_created_tasks(task_service: TaskService) -> None:
    first = task_service.create_task(TaskGreate(title="Write documentation"))
    second = task_service.create_task(TaskGreate(title="Review changes"))

    listed = task_service.list_tasks()

    assert {task.id for task in listed} == {first.id, second.id}
    assert len(listed) == 2


def test_update_task_changes_supplied_fields(task_service: TaskService) -> None:
    created = task_service.create_task(
        TaskGreate(title="Draft plan", description="Initial notes")
    )

    updated = task_service.update_task(
        created.id,
        taskUpdate(title="Finalize plan", completed=True),
    )

    assert updated.id == created.id
    assert updated.title == "Finalize plan"
    assert updated.description == "Initial notes"
    assert updated.completed is True


def test_delete_task_removes_existing_task(task_service: TaskService) -> None:
    created = task_service.create_task(TaskGreate(title="Temporary task"))

    task_service.delete_task(created.id)

    with pytest.raises(TaskNotFoundError):
        task_service.get_task(created.id)


@pytest.mark.parametrize("operation", ["get", "update", "delete"])
def test_operations_on_missing_id_raise_not_found(
    task_service: TaskService,
    operation: str,
) -> None:
    missing_id = uuid4()

    with pytest.raises(TaskNotFoundError):
        if operation == "get":
            task_service.get_task(missing_id)
        elif operation == "update":
            task_service.update_task(
                missing_id,
                taskUpdate(title="Updated title"),
            )
        else:
            task_service.delete_task(missing_id)
