from datetime import UTC, datetime
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from app.api.task_routes import router as task_router

class HealthResponse(BaseModel):
    status: Literal["ok"]
    timestamp: datetime


app = FastAPI()
app.include_router(task_router)


@app.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(UTC))
