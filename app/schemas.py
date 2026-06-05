from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict

class JobStatusEnum(str, Enum):
    queued = "queued"
    processing = "processing"
    done = "done"
    failed = "failed"

class JobCreate(BaseModel):
    type: str
    payload: dict[str, Any]

class JobRead(BaseModel):
    id: int
    type: str
    status: JobStatusEnum
    payload: dict[str, Any]
    error: str | None = None
    result: dict[str, Any] | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobList(BaseModel):
    jobs: list[JobRead]

