from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI

from helios.events import Event, EventLog, EventType
from helios.models import InferenceRequest, InferenceResponse
from helios.policy import SingleWorkerPolicy
from helios.worker import MockWorker


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


worker = MockWorker(
    worker_id="worker-1",
    base_latency_ms=50,
    capacity=1,
    healthy=True,
)
policy = SingleWorkerPolicy(worker)
event_log = EventLog()
app = FastAPI(
    title="Helios",
    version="0.1.0",
)


@app.post("/inference", response_model=InferenceResponse)
async def create_inference(request: InferenceRequest) -> InferenceResponse:
    request_id = str(uuid4())
    result = await process_inference(
        request=request,
        request_id=request_id,
        policy=policy,
        event_log=event_log,
    )
    response = InferenceResponse(
        request_id=request_id,
        worker_id=worker.worker_id,
        result=result,
    )
    return response
