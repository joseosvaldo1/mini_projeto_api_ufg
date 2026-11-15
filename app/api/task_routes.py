from functools import lru_cache
from typing import NoReturn
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.model.tasks import TasjOut, TaskGreate, TaskReplace
from app.repositories.task_repository import TaskRepository
from app.services.priority_advisor import PriorityAdvisor
from app.services.task_service import TaskNotFoundError, TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])


@lru_cache(maxsize=1)
def get_task_service() -> TaskService:
    """Build the shared service with concrete application dependencies."""
    return TaskService(
        repository=TaskRepository(),
        priority_advisor=PriorityAdvisor(),
    )


def _raise_not_found(error: TaskNotFoundError) -> NoReturn:
    """Translate a missing task into an HTTP 404 response."""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found.",
    ) from error


@router.post(
    "",
    response_model=TasjOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: TaskGreate,
    service: TaskService = Depends(get_task_service),
) -> TasjOut:
    """Create a task."""
    return service.create_task(task)


@router.get("", response_model=list[TasjOut])
def list_tasks(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_task_service),
) -> list[TasjOut]:
    """List a bounded page of tasks."""
    return service.list_tasks(limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TasjOut)
def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> TasjOut:
    """Return a task by UUID."""
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as error:
        _raise_not_found(error)


@router.put("/{task_id}", response_model=TasjOut)
def update_task(
    task_id: UUID,
    changes: TaskReplace,
    service: TaskService = Depends(get_task_service),
) -> TasjOut:
    """Update a task."""
    try:
        return service.update_task(task_id, changes)
    except TaskNotFoundError as error:
        _raise_not_found(error)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
) -> Response:
    """Delete a task."""
    try:
        service.delete_task(task_id)
    except TaskNotFoundError as error:
        _raise_not_found(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
