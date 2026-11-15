import sqlite3
from contextlib import closing
from pathlib import Path
from uuid import UUID

from app.model.tasks import TasjOut, TaskGreate, TaskReplace, taskUpdate


class TaskRepository:
    """Persist tasks in a SQLite database."""

    def __init__(self, database_path: str | Path = "tasks.db") -> None:
        self._use_uri = str(database_path) == ":memory:"
        self._anchor_connection: sqlite3.Connection | None = None
        if self._use_uri:
            self._database_path = f"file:tasks_{id(self)}?mode=memory&cache=shared"
            self._anchor_connection = sqlite3.connect(
                self._database_path,
                uri=True,
            )
        else:
            self._database_path = str(database_path)
            Path(self._database_path).parent.mkdir(parents=True, exist_ok=True)
        self._create_table()

    def _connect(self) -> sqlite3.Connection:
        """Open a database connection with named row access."""
        connection = sqlite3.connect(self._database_path, uri=self._use_uri)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_table(self) -> None:
        """Create the tasks table when it does not exist."""
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    completed INTEGER NOT NULL
                )
                """
            )

    @staticmethod
    def _to_task(row: sqlite3.Row) -> TasjOut:
        """Convert a database row to a task model."""
        return TasjOut(
            id=UUID(row["id"]),
            title=row["title"],
            description=row["description"],
            completed=bool(row["completed"]),
        )

    def create(self, task: TaskGreate) -> TasjOut:
        """Create and return a task with a generated UUID."""
        created = TasjOut(**task.model_dump())
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                INSERT INTO tasks (id, title, description, completed)
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(created.id),
                    created.title,
                    created.description,
                    int(created.completed),
                ),
            )
        return created

    def list(self, limit: int = 20, offset: int = 0) -> list[TasjOut]:
        """Return a page of tasks in UUID order."""
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT id, title, description, completed
                FROM tasks
                ORDER BY id ASC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            ).fetchall()
        return [self._to_task(row) for row in rows]

    def get_by_id(self, task_id: UUID) -> TasjOut | None:
        """Return a task by UUID, or None if it does not exist."""
        with closing(self._connect()) as connection:
            row = connection.execute(
                """
                SELECT id, title, description, completed
                FROM tasks
                WHERE id = ?
                """,
                (str(task_id),),
            ).fetchone()
        return self._to_task(row) if row is not None else None

    def update(
        self,
        task_id: UUID,
        changes: TaskReplace | taskUpdate,
    ) -> TasjOut | None:
        """Update supplied fields, or return None if the task is missing."""
        current = self.get_by_id(task_id)
        if current is None:
            return None

        updated = TasjOut.model_validate(
            {
                **current.model_dump(),
                **changes.model_dump(exclude_unset=True),
            }
        )
        with closing(self._connect()) as connection, connection:
            connection.execute(
                """
                UPDATE tasks
                SET title = ?, description = ?, completed = ?
                WHERE id = ?
                """,
                (
                    updated.title,
                    updated.description,
                    int(updated.completed),
                    str(updated.id),
                ),
            )
        return updated

    def delete(self, task_id: UUID) -> bool:
        """Delete a task and report whether it existed."""
        with closing(self._connect()) as connection, connection:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (str(task_id),),
            )
            return cursor.rowcount > 0
