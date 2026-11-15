from typing import Protocol
from uuid import UUID

from app.model.tasks import PrioritySuggestion, TasjOut, TaskGreate, TaskReplace, taskUpdate
from app.repositories.protocols import TaskRepositoryProtocol


class PriorityAdvisorProtocol(Protocol):
    """Contract for components that recommend task priorities."""

    def suggest_priority(self, task: TasjOut) -> PrioritySuggestion:
        """Return a priority recommendation for a task."""
        ...


class TaskNotFoundError(LookupError):
    """Raised when a requested task does not exist."""


class TaskService:
    """Apply task business rules using a repository and an optional advisor."""

    def __init__(
        self,
        repository: TaskRepositoryProtocol,
        priority_advisor: PriorityAdvisorProtocol,
    ) -> None:
        self._repository = repository
        self._priority_advisor = priority_advisor

    def create_task(self, task: TaskGreate) -> TasjOut:
        """Create a task through the repository."""
        return self._repository.create(task)

    def list_tasks(self, limit: int = 20, offset: int = 0) -> list[TasjOut]:
        """Return a page of stored tasks."""
        return self._repository.list(limit=limit, offset=offset)

    def get_task(self, task_id: UUID) -> TasjOut:
        """Return a task or raise an error if it does not exist."""
        task = self._repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} was not found.")
        return task

    def update_task(
        self,
        task_id: UUID,
        changes: TaskReplace | taskUpdate,
    ) -> TasjOut:
        """Update a task or raise an error if it does not exist."""
        task = self._repository.update(task_id, changes)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} was not found.")
        return task

    def delete_task(self, task_id: UUID) -> None:
        """Delete a task or raise an error if it does not exist."""
        if not self._repository.delete(task_id):
            raise TaskNotFoundError(f"Task {task_id} was not found.")

    def suggest_priority(self, task_id: UUID) -> PrioritySuggestion:
        """Return a recommendation without changing the stored task."""
        task = self.get_task(task_id)
        return self._priority_advisor.suggest_priority(task)
