from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class EventType(str, Enum):
    REQUEST_RECEIVED = "REQUEST_RECEIVED"
    WORKER_SELECTED = "WORKER_SELECTED"
    EXECUTION_STARTED = "EXECUTION_STARTED"
    EXECUTION_COMPLETED = "EXECUTION_COMPLETED"


class Event(BaseModel):
    event_type: EventType
    timestamp: datetime
    request_id: str = Field(min_length=1)
    worker_id: str | None = None


class EventLog:
    def __init__(self) -> None:
        self._events: list[Event] = []

    def record(self, event: Event) -> None:
        self._events.append(event)

    def get_events(self) -> list[Event]:
        return self._events