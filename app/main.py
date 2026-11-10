from datetime import UTC, datetime
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]
    timestamp: datetime


app = FastAPI()


@app.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(UTC))
