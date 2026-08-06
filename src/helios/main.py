from datetime import UTC, datetime

from fastapi import FastAPI

from helios.events import Event, EventLog, EventType
from helios.models import InferenceRequest
from helios.policy import SingleWorkerPolicy


async def process_inference(
    request: InferenceRequest,
    request_id: str,
    policy: SingleWorkerPolicy,
    event_log: EventLog,
) -> str:
    event_log.record(
        Event(
            event_type=EventType.REQUEST_RECEIVED,
            timestamp=datetime.now(UTC),
            request_id=request_id,
        )
    )
    worker = policy.select_worker()
    event_log.record(
        Event(
            event_type=EventType.WORKER_SELECTED,
            timestamp=datetime.now(UTC),
            request_id=request_id,
            worker_id=worker.worker_id,
        )
    )
    event_log.record(
        Event(
            event_type=EventType.EXECUTION_STARTED,
            timestamp=datetime.now(UTC),
            request_id=request_id,
            worker_id=worker.worker_id,
        )
    )
    result = await worker.execute(request)
    event_log.record(
        Event(
            event_type=EventType.EXECUTION_COMPLETED,
            timestamp=datetime.now(UTC),
            request_id=request_id,
            worker_id=worker.worker_id,
        )
    )
    return result
app = FastAPI(
    title="Helios",
    version="0.1.0",
)