from uuid import UUID, uuid4
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


PriorityLevel = Literal["baixa", "media", "alta"]


class PrioritySuggestion(BaseModel):
    """Priority recommendation returned to the caller."""

    model_config = ConfigDict(frozen=True)

    priority: PriorityLevel
    justification: str = Field(min_length=1, max_length=300)


def _strip_title(value: object) -> object:
    """Trim title whitespace before applying field constraints."""
    return value.strip() if isinstance(value, str) else value


class TaskGreate(BaseModel):
    """Fields required to create a task."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, strict=True)

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: object) -> object:
        return _strip_title(value)


class TaskReplace(BaseModel):
    """Complete set of editable fields used to replace a task."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(max_length=2000)
    completed: bool = Field(strict=True)

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: object) -> object:
        return _strip_title(value)


class taskUpdate(BaseModel):
    """Optional fields used to update a task."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool | None = Field(default=None, strict=True)

    @field_validator("title", mode="before")
    @classmethod
    def normalize_title(cls, value: object) -> object:
        if value is None:
            raise ValueError("title cannot be null")
        return _strip_title(value)

    @field_validator("completed", mode="before")
    @classmethod
    def completed_cannot_be_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("completed cannot be null")
        return value

    @model_validator(mode="after")
    def require_at_least_one_change(self) -> "taskUpdate":
        if not self.model_fields_set:
            raise ValueError("At least one task field must be provided")
        return self


class TasjOut(BaseModel):
    """Task returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str | None = None
    completed: bool
