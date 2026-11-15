from typing import Protocol
from uuid import UUID

from app.model.tasks import TasjOut, TaskGreate, TaskReplace, taskUpdate


class TaskRepositoryProtocol(Protocol):
    """Contract required by task business logic."""

    def create(self, task: TaskGreate) -> TasjOut:
        """Persist and return a task."""
        ...

    def list(self, limit: int = 20, offset: int = 0) -> list[TasjOut]:
        """Return a page of tasks."""
        ...

    def get_by_id(self, task_id: UUID) -> TasjOut | None:
        """Return a task by UUID when it exists."""
        ...

    def update(
        self,
        task_id: UUID,
        changes: TaskReplace | taskUpdate,
    ) -> TasjOut | None:
        """Apply task changes when the task exists."""
        ...

    def delete(self, task_id: UUID) -> bool:
        """Delete a task and report whether it existed."""
        ...
