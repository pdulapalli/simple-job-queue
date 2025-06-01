import json
from pydantic import BaseModel, field_serializer, field_validator
from datetime import datetime
from enum import StrEnum
from typing import Any


class JobStatus(StrEnum):
    PENDING = "pending"

    IN_PROGRESS = "in_progress"

    COMPLETED = "completed"

    FAILED = "failed"


class JobData(BaseModel):
    id: str
    status: JobStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    payload: dict[str, Any]

    @field_serializer("payload", when_used="json")
    def serialize_payload(self, payload: dict[str, Any]):
        return json.dumps(payload)

    @field_validator("payload", mode="before")
    def deserialize_payload(cls, value: str | dict[str, Any]):
        if isinstance(value, str):
            return json.loads(value)

        return value
